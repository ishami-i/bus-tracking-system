import sys


def main(argv: list[str] | None = None) -> None:
    """Main CLI entry point for the bus tracking backend.

    This function parses basic commands from argv and dispatches to
    backend logic. For now, it only supports a simple `ping` command
    as a placeholder.
    """

    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        print("Usage: python run.py <command> [options]")
        print("Available commands: ping")
        return

    command = argv[0]

    if command == "ping":
        print("pong")
    else:
        print(f"Unknown command: {command}")
        print("Available commands: ping")
