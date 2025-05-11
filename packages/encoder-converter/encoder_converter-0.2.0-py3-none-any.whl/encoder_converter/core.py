import tempfile
from pathlib import Path
from typing import Any

import openvino as ov
import torch
from transformers import AutoTokenizer, T5EncoderModel

from encoder_converter.wrappers import T5EncoderModelWrapper


class CompileError(Exception): ...


class ModelFormatNotSupportedError(CompileError):
    def __init__(self, format: str):
        """Raises when the user provides a format that is not implemented.

        Args:
            format (str): Format name.
        """
        super().__init__(
            f"Unexpected compiled model format `{format}`. Supported formats are 'onnx' and 'openvino'."
        )


def generate_model_path(base_dir: Path, model_name: str, extension: str) -> str:
    """Generate model path.

    Args:
        base_dir (Path): Base directory.
        model_name (str): Model name.
        extension (str): Model extension.

    Returns:
        str: Generated model path.
    """
    return (base_dir / f"{model_name}.{extension}").as_posix()


def convert_to_onnx(
    model: T5EncoderModel,
    dummy_input: Any,
    output_dir: Path,
    model_name: str = "encoder",
) -> str:
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    model_path = generate_model_path(
        base_dir=output_dir, model_name=model_name, extension="onnx"
    )
    torch.onnx.export(
        model,
        dummy_input,
        model_path,
        input_names=["input_ids"],
        output_names=["last_hidden_state"],
        dynamic_axes={
            "input_ids": {1: "sequence_length"},
        },
    )
    return model_path


def convert_to_openvino(input_model_path: str, output_dir: Path, model_name: str):
    model = ov.convert_model(input_model_path)
    output_model_path = generate_model_path(
        base_dir=output_dir, model_name=model_name, extension="xml"
    )
    ov.save_model(model, output_model_path)
    return output_model_path


def convert_encoder(
    model_name: str, target_format: str, output_dir: str, cache_dir: str
):
    """Convert huggingface encoder model to onnx.

    Args:
        model_name (str): Huggingface model name in format <project>/<repo>.
        target_format (str): Compiled model format. Available: `openvino`, `onnx`.
        output_dir (str): Path to save compiled model.
        cache_dir (str): Path to a directory in which a downloaded pretrained model configuration should be cached while compiling.
    """
    if target_format not in ["onnx", "openvino"]:
        raise ModelFormatNotSupportedError(format=target_format)

    try:
        with tempfile.TemporaryDirectory(dir=cache_dir) as tmp_dir:
            tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=tmp_dir)
            model = T5EncoderModelWrapper.from_pretrained(model_name, cache_dir=tmp_dir)
            model.eval()

        output_model_name = model_name.split("/")[1]
        dummy_input = tokenizer(["Dummy Input"], return_tensors="pt")["input_ids"]
        if target_format == "onnx":
            _ = convert_to_onnx(
                model=model,
                dummy_input=dummy_input,
                output_dir=Path(output_dir),
                model_name=output_model_name,
            )
        elif target_format == "openvino":
            with tempfile.TemporaryDirectory(dir=cache_dir) as tmp_dir:
                onnx_model_path = convert_to_onnx(
                    model=model,
                    dummy_input=dummy_input,
                    output_dir=Path(tmp_dir),
                    model_name=output_model_name,
                )
                convert_to_openvino(
                    input_model_path=onnx_model_path,
                    output_dir=Path(output_dir),
                    model_name=output_model_name,
                )

        tokenizer.save_pretrained(output_dir)
    except Exception as exc:
        raise CompileError(f"An error occured while compiling: {str(exc)}")
