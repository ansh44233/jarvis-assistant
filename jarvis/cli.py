"""Command line entry point: one-shot or interactive."""
from __future__ import annotations

import argparse
import json
import os
import sys

from .assistant import Assistant
from .store import Store, default_path

try:
    import readline  # noqa: F401
except ImportError:
    pass

EXIT_WORDS = {"quit", "exit", "bye", "q"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="jarvis", description="Your offline personal assistant.")
    parser.add_argument("command", nargs="*", help="run one command and exit")
    parser.add_argument("--db", default=None, help="path to the database file")
    parser.add_argument("--export", metavar="PATH", help="export notes, tasks, reminders and chat to JSON")
    parser.add_argument("--web", action="store_true", help="launch the local browser dashboard")
    parser.add_argument("--host", default="127.0.0.1", help="dashboard bind address (default: localhost)")
    parser.add_argument("--port", type=int, default=8765, help="dashboard port (default: 8765)")
    args = parser.parse_args(argv)

    store = Store(args.db or default_path())
    jarvis = Assistant(store, name=os.environ.get("JARVIS_NAME", "boss"))
    try:
        if args.export:
            with open(args.export, "w", encoding="utf-8") as handle:
                json.dump(store.export_data(), handle, ensure_ascii=False, indent=2)
            print(f"Exported JARVIS data to {args.export}")
            return 0
        if args.web:
            from .web import serve
            serve(jarvis, store, args.host, args.port)
            return 0
        if args.command:
            for line in jarvis.alerts():
                print(line)
            print(jarvis.handle(" ".join(args.command)))
            return 0
        return repl(jarvis)
    finally:
        store.close()


def repl(jarvis: Assistant) -> int:
    print(jarvis.handle("brief"))
    print("Type 'help' for commands.\n")
    while True:
        for line in jarvis.alerts():
            print(f"\a>> {line}")
        try:
            text = input("jarvis> ")
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if text.strip().lower() in EXIT_WORDS:
            print("Goodbye.")
            return 0
        reply = jarvis.handle(text)
        if reply:
            print(reply)


if __name__ == "__main__":
    sys.exit(main())
