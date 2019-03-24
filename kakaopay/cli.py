import argparse
import sys

from .server.app import start_app
from .constant.constant import ExitCode


def main():
    return app()


def app():
    parser = argparse.ArgumentParser(prog='cli.py', usage=f"""
        ==========================
        server
        ==========================
        cli commands:
            start : server start
        """)

    parser.add_argument('command', type=str,
                        nargs='*',
                        choices=['start'],
                        help='server type [start]')

    args = parser.parse_args()

    if len(args.command) < 1:
        parser.print_help()
        sys.exit(ExitCode.COMMAND_IS_WRONG)

    command = args.command[0]
    if command == 'start' and len(args.command) == 1:
        result = _start()
    else:
        parser.print_help()
        result = ExitCode.COMMAND_IS_WRONG.value
    sys.exit(result)


def _start():
    start_app()
    return ExitCode.SUCCEEDED
