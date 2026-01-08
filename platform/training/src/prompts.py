OUTPUT_MARKER = "<OUTPUT>"
OUTPUT_END = "</OUTPUT>"

def build_training_text(input_text: str, output_bundle: str) -> str:
    # Input already contains your tags. We just append output markers.
    return (
        input_text.rstrip()
        + "\n\n"
        + OUTPUT_MARKER
        + "\n"
        + output_bundle.rstrip()
        + "\n"
        + OUTPUT_END
        + "\n"
    )
