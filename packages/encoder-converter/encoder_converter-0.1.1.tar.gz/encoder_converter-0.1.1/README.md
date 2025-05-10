# Encoder converter
:rocket: Easy way to convert huggingface encoder model to other formats.
## Description
Encoder converter is a package that allowes you to convert huggingface encoder model to other formats (e.g. onnx).
## Features
Unfinished features will be implemented in future versions.
- [x] Convert encoder model to onnx.
- [ ] Convert encoder model to openvino.
## Installation
```bash
pip install encoder-converter
```
## Usage
### Run
You can find the complied model at `output_dir`/t5_encoder.onnx
```bash
convertencoder --model project/repo --output-dir /my/output/dir --cache_dir /cache/dir
```
### Parameters
| Parameter      | Description                                               | Default   |
|----------------|-----------------------------------------------------------|-----------|
| `--model-name` | Huggingface model name                                    |           |
| `--output-dir` | Path to save compiled model and tokenizer artifacts.      |           |
| `--cache-dir`  | Path to a directory in which a downloaded pretrained model configuration should be cached while compiling.                                                 |  `/tmp`   |