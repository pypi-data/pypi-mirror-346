import tempfile
from pathlib import Path

import torch
from transformers import AutoTokenizer

from encoder_converter.wrappers import T5EncoderModelWrapper


def convert_encoder(model_name: str, output_dir: str, cache_dir: str):
    """Convert huggingface encoder model to onnx.

    Args:
        model_name (str): Huggingface model name in format <project>/<repo>.
        output_dir (str): Path to save compiled model.
        c (str): Path to a directory in which a downloaded pretrained model configuration should be cached while compiling.
    """
    with tempfile.TemporaryDirectory(dir=cache_dir) as tmp_dir:
        tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=tmp_dir)
        model = T5EncoderModelWrapper.from_pretrained(model_name, cache_dir=tmp_dir)

    model.eval()
    dummy_input = tokenizer(["Dummy Input"], return_tensors="pt")["input_ids"]
    onnx_dir = Path(output_dir)
    if not onnx_dir.exists():
        onnx_dir.mkdir()
    torch.onnx.export(
        model,
        dummy_input,
        (onnx_dir / "t5_encoder.onnx").as_posix(),
        input_names=["input_ids"],
        output_names=["last_hidden_state"],
        dynamic_axes={
            "input_ids": {1: "sequence_length"},
        },
    )
    tokenizer.save_pretrained(output_dir)
