import os
import sys
import importlib
import argparse
import traceback
from slyther.interpreter import Interpreter


def main():
    """
    The entry point for the ``slyther`` command.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--pypy',
        action='store_true',
        help='Run using PyPy (experimental and not required to work)')
    parser.add_argument(
        '--load',
        type=argparse.FileType('r'),
        help='Source code to evaluate before dropping to a REPL')
    parser.add_argument(
        'source',
        type=argparse.FileType('r'),
        nargs='?',
        help='Source code to run')
    args = parser.parse_args()

    if args.pypy and sys.implementation.name != 'pypy':
        env = dict(os.environ)
        env['PYTHONPATH'] = os.path.dirname(os.path.dirname(
            importlib.util.find_spec('slyther').origin))
        try:
            os.execvpe('pypy3', ['pypy3', '-m', 'slyther'] + sys.argv[1:], env)
        except FileNotFoundError:
            print("The pypy3 command must be available on your system "
                  "for this feature to work.", file=sys.stderr)
            sys.exit(1)

    interp = Interpreter()
    try:
        if args.source:
            interp.exec(args.source.read())
        else:
            if args.load:
                interp.exec(args.load.read())
            from slyther.repl import repl
            repl(interp)
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        traceback.print_exc(limit=10, chain=False)


if __name__ == '__main__':
    main()
