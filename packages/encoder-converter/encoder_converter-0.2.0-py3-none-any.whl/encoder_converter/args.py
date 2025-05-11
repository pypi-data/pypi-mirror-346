import argparse


def huggingface_model_name(model_name: str):
    """Validates that the huggingface model name matches the expected <project>/<repo> format.

    Args:
        model_name (str): Huggingface model name.

    Raises:
        argparse.ArgumentTypeError: Raises when a model name is received an unexpected format.

    Returns:
        str: Validated huggingface model name.
    """
    values = model_name.split("/")
    if len(values) < 2:
        raise argparse.ArgumentTypeError(
            "Model name should be in format <project>/<repo>."
        )
    return model_name


def parse_args():
    """Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        "encoder-converter",
        description="Convert huggingface encoder to onnx format.",
    )
    parser.add_argument(
        "-m",
        "--model-name",
        help="Huggingface model name.",
        required=True,
        type=huggingface_model_name,
    )
    parser.add_argument(
        "-f",
        "--format",
        help="Compiled model format.",
        required=True,
        choices=["onnx", "openvino"],
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        help="Path to save compiled model and tokenizer artifacts.",
        required=True,
    )
    parser.add_argument(
        "-c",
        "--cache-dir",
        help="Path to a directory in which a downloaded pretrained model configuration should be cached while compiling.",
        default="/tmp",
        required=True,
    )
    return parser.parse_args()
