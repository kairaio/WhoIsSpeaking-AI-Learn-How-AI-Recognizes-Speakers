import sys

from app.speaker.identification import identify_speaker


def main():
    """
    Simple command-line demo.

    Usage:
        python examples/demo.py path/to/sample.wav
    """

    if len(sys.argv) != 2:
        print(
            "Usage: python examples/demo.py "
            "path/to/sample.wav"
        )
        raise SystemExit(1)

    audio_path = sys.argv[1]

    result = identify_speaker(
        audio_path
    )

    print("\nWhoIsSpeaking AI")
    print("----------------")
    print(
        f"Speaker: {result['speaker']}"
    )
    print(
        f"Best candidate: "
        f"{result.get('best_candidate')}"
    )
    print(
        f"Score: {result['score']}"
    )
    print(
        f"Threshold: "
        f"{result['threshold']}"
    )
    print(
        f"Matched: "
        f"{result['matched']}"
    )


if __name__ == "__main__":
    main()