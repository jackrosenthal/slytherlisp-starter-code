from functools import partial
import slyther.builtins
from slyther.types import (BuiltinCallable, NIL, LexicalVarStorage, Variable,
                           Boolean)
from slyther.evaluator import lisp_eval
from slyther.parser import tokenize, parse


class Interpreter:
    """
    This type wraps all of the state of an intepreter.
    """
    def __init__(self):
        # load builtins out of slyther.bulitins
        builtins = {
            x.__name__: Variable(x)
            for x in map(
                partial(getattr, slyther.builtins),
                slyther.builtins.__dir__())
            if isinstance(x, BuiltinCallable)}
        # put in the default variables
        builtins.update({
            'NIL': Variable(NIL),
            'nil': Variable(NIL),
            '#t': Variable(Boolean(True)),
            '#f': Variable(Boolean(False)),
        })
        self.stg = LexicalVarStorage(builtins)

    def eval(self, expr):
        """
        Eval a single (parsed) lisp expression.
        """
        try:
            return lisp_eval(expr, self.stg)
        except RecursionError as e:
            raise RecursionError(
                "Maximum recursion depth exceeded while evaluating {!r}"
                .format(expr)) from e

    def exec(self, code):
        """
        Execute the string ``code`` on the interpreter,
        returning the result of the last evaluation.
        """
        r = NIL
        for expr in parse(tokenize(code)):
            r = self.eval(expr)
        return r
