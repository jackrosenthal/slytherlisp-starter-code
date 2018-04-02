import operator
from functools import reduce
from slyther.types import (BuiltinFunction, BuiltinMacro, Symbol,
                           UserFunction, SExpression, cons, String,
                           ConsList)
from slyther.evaluator import lisp_eval
from slyther.parser import tokenize, parse
from math import floor, ceil, sqrt


@BuiltinFunction('+')
def add(*args):
    """
    Sum each of the arguments

    >>> add(1, 2, 3, 4)
    10
    >>> add()
    0

    .. hint::

        Use ``sum`` or ``reduce``.
    """
    raise NotImplementedError("Deliverable 3")


@BuiltinFunction('-')
def sub(*args):
    """
    ``(- x y z)`` computes ``x - y - z``, but with only one argument,
    ``(- x)`` computes ``-x``.

    >>> sub(10, 1, 2)
    7
    >>> sub(10, 1)
    9
    >>> sub(10)
    -10
    >>> sub()
    0

    .. hint::

        Use ``reduce``.
    """
    raise NotImplementedError("Deliverable 3")


@BuiltinFunction('*')
def mul(*args):
    """
    Compute the product.

    >>> mul(2, 3)
    6
    >>> mul(2, 3, 3)
    18
    >>> mul(2)
    2
    >>> mul()
    1
    """
    raise NotImplementedError("Deliverable 3")


@BuiltinFunction('/')
def div(*args):
    """
    ``(/ a b c)`` computes ``a / b / c``, but ``(/ a)`` computes
    ``1 / a``.

    >>> div(1, 2)
    0.5
    >>> div(1, 2, 2)
    0.25
    >>> div(2)
    0.5
    """
    raise NotImplementedError("Deliverable 3")


@BuiltinFunction
def floordiv(*args):
    """
    Equivalent to ``div``, but uses ``operator.floordiv``.

    >>> floordiv(3, 2)
    1
    >>> floordiv(3, 2, 2)
    0
    >>> floordiv(1)
    1
    >>> floordiv(2)
    0
    """
    raise NotImplementedError("Deliverable 3")


# IO
_print = BuiltinFunction(print)
_input = BuiltinFunction(input)

# Type Constructors
_int = BuiltinFunction(int)
_float = BuiltinFunction(float)
symbol = BuiltinFunction(Symbol, 'symbol')
string = BuiltinFunction(String, 'string')


@BuiltinFunction('list')
def _list(*args):
    """
    Create a ``ConsList`` from ``args``.

    >>> _list(1, 2, 3)
    (list 1 2 3)
    >>> _list()
    NIL
    """
    raise NotImplementedError("Deliverable 3")


# Comparators
lt = BuiltinFunction(operator.lt, '<')
gt = BuiltinFunction(operator.gt, '>')
eq = BuiltinFunction(operator.eq, '=')
le = BuiltinFunction(operator.le, '<=')
ge = BuiltinFunction(operator.ge, '>=')
_not = BuiltinFunction(operator.not_, 'not')

# arithmetic
remainder = BuiltinFunction(operator.mod, 'remainder')
_floor = BuiltinFunction(floor)
_ceil = BuiltinFunction(ceil)
_sqrt = BuiltinFunction(sqrt)
_abs = BuiltinFunction(abs)
expt = BuiltinFunction(operator.pow, 'expt')

# string manipulation
_format = BuiltinFunction(str.format)
split = BuiltinFunction(str.split)

# cons cell functions
cons = BuiltinFunction(cons)


@BuiltinFunction
def car(cell):
    """
    Get the ``car`` of a cons cell.
    """
    raise NotImplementedError("Deliverable 3")


@BuiltinFunction
def cdr(cell):
    """
    Get the ``cdr`` of a cons cell.
    """
    raise NotImplementedError("Deliverable 3")


@BuiltinMacro
def define(se, stg):
    """
    Define a variable or a function to a value, calling ``put`` on
    the storage::

        ; variable
        (define var-name evaluate-me)

        ; lambda function
        (define func-name (lambda (args...) (body1) ... (bodyN)))

        ; SE-named function
        (define (func-name args...) (body1) ... (bodyN))

    .. note::

        If defining a function (either by ``lambda`` or by SE-named
        syntax), the definition **must** be made visible from within
        that function's ``environ``, or recursion will not work!

    >>> from slyther.types import *
    >>> name = Symbol('twirl')
    >>> args = SExpression.from_iterable(
    ...     map(Symbol, ['alpha', 'beta']))
    >>> body = SExpression.from_iterable([
    ...     SExpression.from_iterable(
    ...         map(Symbol, ['print', 'alpha'])),
    ...     SExpression.from_iterable(
    ...         map(Symbol, ['print', 'beta']))])
    >>> stg = LexicalVarStorage({})
    >>> stg.put('NIL', NIL)
    >>> stg.put('define', define) # so that you can return a define if you want
    >>> stg.put('lambda', lambda_func)
    >>> from slyther.evaluator import lisp_eval
    >>> lisp_eval(define(cons(cons(name, args), body), stg), stg)
    NIL
    >>> lisp_eval(
    ...     define(SExpression.from_iterable([Symbol('x'), 10]), stg), stg)
    NIL
    >>> stg[name].value
    (lambda (alpha beta) (print alpha) (print beta))
    >>> stg[name].value.environ['twirl'].value
    (lambda (alpha beta) (print alpha) (print beta))
    >>> stg['x'].value
    10
    >>> stg[name].value.environ['x'].value
    Traceback (most recent call last):
        ...
    KeyError: 'x'
    """
    raise NotImplementedError("Deliverable 3")


@BuiltinMacro('lambda')
def lambda_func(se, stg):
    """
    Define an anonymous function and return the ``UserFunction``
    object.

    >>> from slyther.types import *
    >>> stg = LexicalVarStorage({})
    >>> stg.put('x', 20)
    >>> f = lambda_func(
    ...     SExpression.from_iterable([
    ...         SExpression.from_iterable(map(Symbol, ['a', 'b', '.', 'c'])),
    ...         SExpression.from_iterable(map(Symbol, ['print', 'a'])),
    ...         SExpression.from_iterable(map(Symbol, ['print', 'b'])),
    ...         SExpression.from_iterable(map(Symbol, ['print', 'c']))]),
    ...     stg)
    >>> f
    (lambda (a b . c) (print a) (print b) (print c))
    >>> f.environ['x'].value
    20
    """
    raise NotImplementedError("Deliverable 3")


@BuiltinMacro('let')
def let(se, stg):
    """
    The ``let`` macro binds variables to a local scope: the expressions
    inside the macro. Like a function, a ``let`` returns the last
    expression in its body. Once the ``let`` returns, the variables are
    unbound, and cannot be accessed anymore. For example::

        (let ((a (+ f g))
              (b 11)
              (c 12))
          (+ a (- b c)))

    In the example above, ``a`` was bound to whatever ``(+ f g)``
    evaluates to, b to ``11``, and ``c`` to ``12``.

    There's a few ways to approach this, but my suggestion is to notice
    how the above was equivalent to another expression::

        ((lambda (a b c)
           (+ a (- b c))) (+ f g) 11 12)

    No unit tests for this, as you are free to implement it any way it
    works; just make sure the example code which uses ``let`` can run.
    """
    raise NotImplementedError("Deliverable 3")


@BuiltinMacro('if')
def if_expr(se, stg):
    """
    An ``if`` expression looks like this::

        (if <predicate> <consequent> <alternative>)

    If the predicate evaluates to something truthy, return the
    consequent, otherwise return the alternative. An example::

        (if (< x 10)
          (print "x is less than 10")
          (print "x is greater than or equal to 10"))

    >>> from slyther.types import *
    >>> se = SExpression.from_iterable(map(SExpression.from_iterable, [
    ...     [Symbol('<'), Symbol('x'), 10],
    ...     [Symbol('print'), String("x is less than 10")],
    ...     [Symbol('print'), String("x is greater than or equal to 10")],
    ... ]))
    >>> stg = LexicalVarStorage({})
    >>> stg.put('<', lt)
    >>> stg.put('x', 9)
    >>> if_expr(se, stg)
    (print "x is less than 10")
    >>> stg['x'].set(10)
    >>> if_expr(se, stg)
    (print "x is greater than or equal to 10")
    """
    raise NotImplementedError("Deliverable 3")


@BuiltinMacro('cond')
def cond(se, stg):
    """
    ``cond`` is similar to ``if``, but it lists a series of predicates
    and consequents, similar to how guards work in Haskell. For
    example::

        (cond
          ((< x 5) (print "x < 5"))
          ((< x 10) (print "5 <= x < 10"))
          ((< x 15) (print "10 <= x < 15"))
          (#t (print "x >= 15")))

    >>> from slyther.types import *
    >>> from slyther.parser import tokenize, parse
    >>> def test_cond(x):
    ...     expr = next(parse(tokenize('''
    ...         (cond
    ...           ((< x 5) (print "x < 5"))
    ...           ((< x 10) (print "5 <= x < 10"))
    ...           ((< x 15) (print "10 <= x < 15"))
    ...           (#t (print "x >= 15")))''')))
    ...     stg = LexicalVarStorage({})
    ...     stg.put('<', lt)
    ...     stg.put('#t', Boolean(True))
    ...     stg.put('x', x)
    ...     return cond(expr.cdr, stg)
    >>> test_cond(4)
    (print "x < 5")
    >>> test_cond(5)
    (print "5 <= x < 10")
    >>> test_cond(10)
    (print "10 <= x < 15")
    >>> test_cond(15)
    (print "x >= 15")
    """
    raise NotImplementedError("Deliverable 3")


@BuiltinMacro('and')
def _and(se, stg):
    """
    Compute an ``and`` expression, like this::

        (and (< x 10) (> y 15) (foo? z))

    Evaluate left to right, and return the first result which produces
    a falsy value. Note that the result need not be a boolean, but you
    should test its falsiness, and return the result (even if it's not
    a boolean).

    Note that you could return the last expression unevaluated if all
    the previous are truthy, as your ``lisp_eval`` should eval it for
    you. This could be useful for tail call optimization.

    No unit tests for this one, make sure it works on your own, or add
    unit tests here.
    """
    raise NotImplementedError("Deliverable 3")


@BuiltinMacro('or')
def _or(se, stg):
    """
    Similar to ``and`` above, but compute an ``or`` instead. Return
    the first truthy value rather than falsy.
    """
    raise NotImplementedError("Deliverable 3")


@BuiltinMacro('set!')
def _set(se, stg):
    """
    Danger, danger, the assigment expression::

        (set! <name> <value>)

    Should just eval ``value`` and call ``stg[name].set`` on it. Return
    ``NIL``. Again, no unit tests, write your own if you wish.
    """
    raise NotImplementedError("Deliverable 3")


@BuiltinMacro('eval')
def _eval(se, stg):
    """
    ::

        (eval <expr>)

    Evaluate ``expr``, if it produces a ``ConsList``, then upgrade
    that ``ConsList`` to an ``SExpression`` and return it. Your
    ``lisp_eval`` will take care of the rest.
    """
    raise NotImplementedError("Deliverable 3")


@BuiltinFunction('parse')
def _parse(code):
    """
    ``code`` is a ``String`` containing a single thing once parsed,
    such as an s-expression, or a symbol. Simply just tokenize it,
    parse it and return it! Woo-hoo!

    >>> from slyther.types import *
    >>> _parse(String("(print x)"))
    (list print x)

    Note that the ``BuiltinFunction`` decorator takes care of
    downgrading an ``SExpression`` to a ``ConsList`` for you.
    """
    raise NotImplementedError("Deliverable 3")
