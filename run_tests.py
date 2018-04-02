#!/usr/bin/env python3
import sys
import argparse
import doctest
import slyther.types
import slyther.parser
import slyther.interpreter
import slyther.builtins
import slyther.evaluator


def module_globals(obj):
    if isinstance(obj, type(sys)):
        pass
    elif hasattr(obj, '__module__'):
        obj = sys.modules[obj.__module__]
    else:
        raise TypeError('Input is not a module or an element with __module__')
    return {
        k: getattr(obj, k)
        for k in dir(obj)
    }


d1 = [
    slyther.types.ConsCell,
    slyther.types.ConsCell.__eq__,
    slyther.types.ConsCell.__repr__,
    slyther.types.ConsList,
    slyther.types.ConsList.__init__,
    slyther.types.ConsList.from_iterable,
    slyther.types.ConsList.__getitem__,
    slyther.types.ConsList.cells,
    slyther.types.ConsList.__len__,
    slyther.types.ConsList.__contains__,
    slyther.types.ConsList.__reversed__,
    slyther.types.ConsList.__eq__,
    slyther.types.ConsList.__repr__,
    slyther.types.SExpression,
    slyther.types.cons,
    slyther.types.LexicalVarStorage,
    slyther.types.LexicalVarStorage.fork,
    slyther.types.LexicalVarStorage.put,
    slyther.types.LexicalVarStorage.__getitem__,
]

d2 = [
    slyther.parser.tokenize,
    slyther.parser.parse,
    slyther.parser.parse_strlit,
    slyther.parser,
]

d3 = [
    slyther.evaluator,
    slyther.evaluator.lisp_eval,
    slyther.types.UserFunction,
    slyther.types.UserFunction.__init__,
    slyther.types.UserFunction.__call__,
    slyther.types.UserFunction.__repr__,
    slyther.interpreter,
    slyther.interpreter.Interpreter,
    slyther.builtins,
    slyther.builtins.add,
    slyther.builtins.sub,
    slyther.builtins.mul,
    slyther.builtins.div,
    slyther.builtins.floordiv,
    slyther.builtins._list,
    slyther.builtins.car,
    slyther.builtins.cdr,
    slyther.builtins.define,
    slyther.builtins.lambda_func,
    slyther.builtins.let,
    slyther.builtins.if_expr,
    slyther.builtins.cond,
    slyther.builtins._and,
    slyther.builtins._or,
    slyther.builtins._set,
    slyther.builtins._eval,
    slyther.builtins._parse,
]


def tco_test(code):
    """
    Test that tail call optimization works.

    >>> f = open("examples/carmichael.scm")
    >>> tco_test(f.read())      # doctest: +ELLIPSIS
    561
    1105
    1729
    2465
    ...
    >>> f.close()
    """
    import signal

    def handler(signum, frame):
        raise TimeoutError

    try:
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(240)
        interp = slyther.interpreter.Interpreter()
        interp.exec(code)
    except TimeoutError:
        return
    signal.alarm(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--d1',
        action='store_true',
        help='Run tests for D1'
    )
    parser.add_argument(
        '--d2',
        action='store_true',
        help='Run tests for D2'
    )
    parser.add_argument(
        '--d3',
        action='store_true',
        help='Run tests for D3'
    )
    parser.add_argument(
        '--tco',
        action='store_true',
        help='Run tail-call optimization tests (takes 4 minutes!)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Print all test results, not just failures'
    )
    args = parser.parse_args()

    tests = []
    if args.d1:
        tests += d1
    if args.d2:
        tests += d2
    if args.d3:
        tests += d3
    if args.tco:
        tests += [tco_test]

    if not tests:
        parser.error('You must specify at least one of --d{1,2,3} or --tco.')

    for t in tests:
        if t is tco_test:
            print("Running tail-call optimization test... "
                  "(takes 4 minutes if it works!)")
            print("Essentially, if after 4-minutes of preforming all sorts\n"
                  "of tail calls, your program does not break, call it good.")
        doctest.run_docstring_examples(
            t,
            globs=module_globals(t),
            verbose=args.verbose,
            name=getattr(t, '__name__', None) or str(t))
