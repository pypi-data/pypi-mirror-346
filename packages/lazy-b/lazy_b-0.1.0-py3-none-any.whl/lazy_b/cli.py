import argparse
import signal
import sys
import time
from typing import NoReturn, List, Optional

from .main import LazyB


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Keep Slack/Teams active by simulating shift key presses at regular intervals."
    )

    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        default=60,
        help="Interval between key presses in seconds (default: 60)",
    )

    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Run in quiet mode (no output)"
    )

    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> NoReturn:
    """Main entry point for the CLI."""
    parsed_args = parse_args(args)

    lazy_b = LazyB(interval=parsed_args.interval)

    def signal_handler(sig, frame) -> None:
        """Handle Ctrl+C to gracefully shut down."""
        print("\nShutting down LazyB...")
        lazy_b.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    def print_status(message: str) -> None:
        """Print status messages if not in quiet mode."""
        if not parsed_args.quiet:
            print(message)

    lazy_b.start(callback=print_status)

    try:
        print_status(f"LazyB is keeping you active (press Ctrl+C to stop)")
        print_status(f"Pressing Shift key every {parsed_args.interval} seconds")

        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

    return sys.exit(0)


if __name__ == "__main__":
    main()
