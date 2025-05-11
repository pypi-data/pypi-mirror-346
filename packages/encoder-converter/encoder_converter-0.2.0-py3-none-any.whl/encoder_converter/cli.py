from encoder_converter.args import parse_args
from encoder_converter.core import convert_encoder


def main():
    args = parse_args()
    convert_encoder(
        model_name=args.model_name,
        target_format=args.format,
        output_dir=args.output_dir,
        cache_dir=args.cache_dir,
    )


if __name__ == "__main__":
    main()
