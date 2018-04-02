import collections.abc as abc
from functools import partial, update_wrapper


class ConsCell:
    """
    A simple cons cell data structure:

    >>> cell = ConsCell(1, 2)
    >>> cell.car
    1
    >>> cell.cdr
    2
    >>> cell.car = 4
    >>> cell.car
    4
    """
    def __init__(self, car, cdr):
        raise NotImplementedError("Deliverable 1")

    def __eq__(self, other):
        """
        Two cons cells are equal if each of their ``car`` and
        ``cdr`` are equal:

        >>> a = ConsCell(1, 2)
        >>> b = ConsCell(2, 1)
        >>> c = ConsCell(1, 1)
        >>> d = ConsCell(1, 2)
        >>> a == a
        True
        >>> a == b
        False
        >>> b == c
        False
        >>> b == d
        False
        >>> a == d
        True
        """
        raise NotImplementedError("Deliverable 1")

    def __repr__(self):
        """
        A cons cell should ``repr`` itself in a format that would
        be parsable and evaluable to our language.

        >>> ConsCell(1, 2)
        (cons 1 2)
        >>> ConsCell(ConsCell(2, 1), 1)
        (cons (cons 2 1) 1)

        .. hint::

            The string formatting specifier ``!r`` will get you the
            ``repr`` of an object.
        """
        raise NotImplementedError("Deliverable 1")


class ConsList(ConsCell, abc.Sequence):
    """
    A ``ConsList`` inherits from a ``ConsCell``, but the ``cdr`` must
    be a ``ConsList`` or any structure which inherits from that.

    >>> cell = ConsList(1, ConsList(2, NIL))
    >>> cell.car
    1
    >>> cell.cdr.car
    2
    >>> cell = ConsList(1, 2)
    Traceback (most recent call last):
        ...
    TypeError: cdr must be a ConsList
    """
    def __init__(self, car, cdr=None):
        """
        If the ``cdr`` was not provided, assume to be ``NIL``.

        >>> cell = ConsList(1)
        >>> cell.cdr
        NIL
        """
        raise NotImplementedError("Deliverable 1")

    @classmethod
    def from_iterable(cls, it):
        """
        Create a ConsList from an iterable.

        >>> ConsList.from_iterable(iter(range(5)))
        (list 0 1 2 3 4)
        >>> ConsList.from_iterable([])
        NIL
        """
        raise NotImplementedError("Deliverable 1")

    def __getitem__(self, idx):
        """
        Get item at index ``idx``:

        >>> lst = [1, 1, 2, 3, 5, 8]
        >>> clst = ConsList.from_iterable(lst)
        >>> [lst[i] == clst[i] for i in range(len(lst))]
        [True, True, True, True, True, True]
        """
        raise NotImplementedError("Deliverable 1")

    def __iter__(self):
        """
        Iterate over the ``car`` of each cell:

        >>> lst = [1, 1, 2, 3, 5, 8]
        >>> for itm in ConsList.from_iterable(lst):
        ...     print(itm)
        1
        1
        2
        3
        5
        8

        """
        raise NotImplementedError("Deliverable 1")

    def cells(self):
        """
        Iterate over each cell (rather that the ``car`` of each):

        >>> lst = [1, 1, 2, 3, 5, 8]
        >>> for cell in ConsList.from_iterable(lst).cells():
        ...     print(cell.car, cell.cdr)
        1 (list 1 2 3 5 8)
        1 (list 2 3 5 8)
        2 (list 3 5 8)
        3 (list 5 8)
        5 (list 8)
        8 NIL
        """
        raise NotImplementedError("Deliverable 1")

    def __len__(self):
        """
        Return the number of elements in the list:

        >>> lst = [1, 1, 2, 3, 5, 8]
        >>> len(ConsList.from_iterable(lst))
        6
        """
        raise NotImplementedError("Deliverable 1")

    def __contains__(self, p):
        """
        Return ``True`` if the list contains an element ``p``,
        ``False`` otherwise:

        >>> lst = [1, 1, 2, 3, 5, 8]
        >>> clst = ConsList.from_iterable(lst)
        >>> 1 in clst
        True
        >>> 3 in clst
        True
        >>> 8 in clst
        True
        >>> NIL in clst
        False
        >>> 9 in clst
        False
        """
        raise NotImplementedError("Deliverable 1")

    def __reversed__(self):
        """
        Iterate over the elements of our list, reversed.

        >>> lst = [1, 1, 2, 3, 5, 8]
        >>> clst = ConsList.from_iterable(lst)
        >>> for x in reversed(clst):
        ...     print(x)
        8
        5
        3
        2
        1
        1
        """
        raise NotImplementedError("Deliverable 1")

    def __bool__(self):
        """ NilType overrides this to be ``False``. """
        return True

    def __eq__(self, other):
        """
        Test if two lists have the same elements in the same order.

        >>> l1, l2 = map(
        ...     ConsList.from_iterable,
        ...     ([1, 2, 10, 3, 4, 7], [1, 2, 10, 3, 4, 7]))
        >>> l1 == l2
        True
        >>> l1, l2 = map(
        ...     ConsList.from_iterable,
        ...     ([1, 2, 10, 4, 3, 7], [1, 2, 10, 3, 4, 7]))
        >>> l1 == l2
        False
        >>> l1, l2 = map(
        ...     ConsList.from_iterable,
        ...     ([1, 2, 10, 3, 4, 7], [1, 2, 10, 3, 4, 7, 1]))
        >>> l1 == l2
        False
        >>> l2 == l1
        False
        >>> l1 = NIL
        >>> l1 == l2
        False
        >>> l2 == l1
        False
        >>> SExpression.from_iterable(l2) == NIL
        False
        """
        raise NotImplementedError("Deliverable 1")

    def __repr__(self):
        """
        Represent ourselves in a format evaluable in our language.

        >>> ConsList.from_iterable([1, 2, 3])
        (list 1 2 3)
        """
        raise NotImplementedError("Deliverable 1")


class NilType(ConsList):
    """
    The type for the global ``NIL`` object.
    """
    def __new__(cls):
        """
        If already constructed, don't make another. Just
        return our already existing instance.
        """
        if 'NIL' in globals().keys():
            return NIL
        return super().__new__(cls)

    def __init__(self):
        """
        The ``car`` and ``cdr`` of ``NIL`` are ``NIL``.
        """
        self.car = self
        self.cdr = self

    def __bool__(self):
        """
        Empty lists are implicitly falsy.
        """
        return False

    def __eq__(self, other):
        """
        There is only one ``NIL`` instance anyway...
        """
        return self is other

    def __repr__(self):
        """
        Represent ourselves in SlytherLisp evaluable format
        """
        return 'NIL'


NIL = NilType()


class Boolean:
    """
    Type for a boolean with SlytherLisp evaluable representation.
    """
    # too bad we can't subclass bool...
    class LispTrue:
        def __bool__(self):
            return True

        def __repr__(self):
            return '#t'

    class LispFalse:
        def __bool__(self):
            return False

        def __repr__(self):
            return '#f'

    t_instance = LispTrue()
    f_instance = LispFalse()

    def __new__(self, v=False):
        """
        There shall only be one true, and one false!
        """
        if v:
            return Boolean.t_instance
        return Boolean.f_instance


class SExpression(ConsList):
    """
    ConsList which we use to store s-expressions. Has an alternate
    representation.

    >>> SExpression(4)
    (4)
    """
    def __repr__(self):
        return '({})'.format(' '.join(map(repr, self)))


def cons(car, cdr):
    """
    Factory for cons cell like things. Tries to make a ``ConsList`` or
    ``SExpression`` if it can (if ``cdr`` is...), otherwise makes a
    plain old ``ConsCell``.

    >>> cons(5, ConsList(4, NIL))
    (list 5 4)
    >>> cons(5, NIL)
    (list 5)
    >>> cons(5, 4)
    (cons 5 4)
    >>> cons(5, SExpression(4, NIL))
    (5 4)
    """
    raise NotImplementedError("Deliverable 1")


class Variable:
    """
    A simple wrapper to reference an object. The reference may
    change using the ``set`` method.

    The reason for this is so that (set! ...) works, even in
    different environments. Also let's Python's garbage collection
    do the dirty work for us.
    """
    def __init__(self, value):
        self.set(value)

    def set(self, value):
        self.value = value


class LexicalVarStorage:
    """
    Storage for lexically scoped variables. Has two parts:

    * An ``environ`` part: a dictionary of the containing
      environment (closure).
    * A ``local`` part: a dictionary of the local variables
      in the function.
    """
    def __init__(self, environ):
        self.environ = environ
        self.local = {}

    def fork(self):
        """
        Return the union of the ``local`` part and the ``environ``
        part. Should not modify either part.

        >>> environ = {k: Variable(v) for k, v in (('x', 10), ('y', 11))}
        >>> stg = LexicalVarStorage(environ)
        >>> stg.put('y', 12)
        >>> stg.put('z', 13)
        >>> environ = dict(stg.environ)
        >>> local = dict(stg.local)
        >>> for k, v in stg.fork().items():
        ...     print(k, v.value)
        x 10
        y 12
        z 13
        >>> stg.environ == environ      # should not be modified
        True
        >>> stg.local == local          # should not be modified
        True
        """
        raise NotImplementedError("Deliverable 1")

    def put(self, name, value):
        """
        Put a **new** variable in the local environment, giving
        it a value ``value``.
        """
        self.local[name] = Variable(value)

    def __getitem__(self, k):
        """
        Return a Variable object, first checking the local
        environment, then checking the containing environment,
        otherwise raising a ``KeyError``.

        >>> environ = {k: Variable(v) for k, v in (('x', 10), ('y', 11))}
        >>> stg = LexicalVarStorage(environ)
        >>> stg.put('y', 12)
        >>> stg.put('z', 13)
        >>> stg['x'].value
        10
        >>> stg['y'].value
        12
        >>> stg['z'].value
        13
        >>> stg['x'].set(11)
        >>> stg['k'].value
        Traceback (most recent call last):
            ...
        KeyError: "Undefined variable 'k'"
        >>> stg['k'].set(10)
        Traceback (most recent call last):
            ...
        KeyError: "Undefined variable 'k'"
        """
        raise NotImplementedError("Deliverable 1")


class Quoted:
    """
    A simple wrapper for a quoted element in the abstract syntax tree.
    """

    def __new__(cls, elem):
        if isinstance(elem, Quoted):
            # don't double quote!
            return elem
        return super().__new__(cls)

    def __init__(self, elem):
        self.elem = elem

    def __repr__(self):
        return "'{!r}".format(self.elem)


class Symbol(str):
    """
    A type for symbols, like a ``str``, but alternate representation.
    """
    def __repr__(self):
        return str(self)


class String(str):
    """
    A type for SlytherLisp strings, like a ``str``, but alternate
    representation: always use double quotes since SlytherLisp only
    allows double quoted strings.
    """
    def __repr__(self):
        r = super().__repr__()
        if r.startswith("'"):
            return '"{}"'.format(r[1:-1].replace('"', '\\"')
                                        .replace("\\'", "'"))
        return r


class Function(abc.Callable):
    """
    Base class for user and builtin functions. No implementation needed.
    """


class UserFunction(Function):
    """
    Type for user defined functions.

    * ``params`` is an s-expression of the parameters, like so:
      (a b c)
    * ``rest`` is where any additional arguments should be placed,
      specified by the symbol after the dot in ``params``.
    * ``body`` is an SExpression with the body of the function. The
      result of the last element in the body should be returned when
      the function is called.
    * ``environ`` is a dictionary created by calling ``.fork()`` on a
      ``LexicalVarStorage`` when the function was created.

    """
    def __init__(self, params, body, environ=None):
        """
        >>> f = UserFunction(
        ...     params=SExpression.from_iterable(
        ...         map(Symbol, ['a', 'b', 'c', '.', 'd'])),
        ...     body=SExpression.from_iterable(
        ...         [SExpression.from_iterable(
        ...             map(Symbol, ['print', 'a', 'b', 'c'])),
        ...          SExpression.from_iterable(
        ...             map(Symbol, ['print', 'd']))]),
        ...     environ={})
        >>> f
        (lambda (a b c . d) (print a b c) (print d))
        >>> f.params
        (a b c)
        >>> f.rest
        d
        >>> f.body
        ((print a b c) (print d))
        """
        raise NotImplementedError("Deliverable 3")

    def __call__(self, *args):
        """
        Call the function with arguments ``args``.

        Make use of ``lisp_eval``.
        """
        # avoid circular imports
        from slyther.evaluator import lisp_eval
        raise NotImplementedError("Deliverable 3")

    def __repr__(self):
        """
        Represent in self-evaluable form.
        """
        return "(lambda ({}{}) {})".format(
            ' '.join(self.params),
            ' . {}'.format(self.rest) if self.rest else '',
            ' '.join(repr(x) for x in self.body))


class Macro(abc.Callable):
    """
    Base class for all macros. No implementation needed.
    """


class BuiltinCallable(abc.Callable):
    """
    Base class for builtin callables (functions and macros)
    """
    py_translations = {
        bool: Boolean,
        str: String,
        list: ConsList.from_iterable,
        tuple: ConsList.from_iterable,
    }

    def __new__(cls, arg=None, name=None):
        if isinstance(arg, str):
            return partial(cls, name=arg)
        obj = super().__new__(cls)
        obj.func = arg
        update_wrapper(obj, obj.func)
        obj.__name__ = name or obj.func.__name__
        return obj

    def __call__(self, *args, **kwargs):
        result = self.func(*args, **kwargs)
        if result is None:
            return NIL
        if type(result) in self.py_translations.keys():
            return self.py_translations[type(result)](result)
        return result


class BuiltinFunction(BuiltinCallable, Function):
    """
    Builtin functions have this type. Unlike macros, functions cannot
    return s-expressions, and they should be downgraded to cons lists.
    """

    py_translations = dict(BuiltinCallable.py_translations)
    py_translations.update({SExpression: ConsList.from_iterable})


class BuiltinMacro(BuiltinCallable, Macro):
    """
    Builtin macros have this type. No implementation needed.
    """
