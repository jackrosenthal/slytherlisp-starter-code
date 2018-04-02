"""
This module defines parsing utilities in SlytherLisp.

>>> parser = parse(tokenize('(print "Hello, World!")'))
>>> se = next(parser)
>>> se
(print "Hello, World!")
>>> type(se)
<class 'slyther.types.SExpression'>

"""

import re
from slyther.types import SExpression, Symbol, String, Quoted

__all__ = ['tokenize', 'parse']

def tokenize(code):
    r"""
    This is a *generator function* that splits a piece of code into
    lexical tokens, emitting whole tokens each time one is encountered.

    >>> list(tokenize(" (define (do-123 fun) \n (map fun '(1 2 3))) \n"))
    ...                                  # doctest: +NORMALIZE_WHITESPACE
    ['(', 'define', '(', 'do-123', 'fun', ')',
        '(', 'map', 'fun', "'(", '1', '2', '3', ')', ')', ')']

    String literals should be emitted as a whole token, unparsed:

    >>> list(tokenize(r'(print "hello \"world\"!")'))
    ['(', 'print', '"hello \\"world\\"!"', ')']
    >>> list(tokenize('(print "hello world\n!")'))
    ['(', 'print', '"hello world\n!"', ')']
    >>> list(tokenize(r'(print "hello world\n!")'))
    ['(', 'print', '"hello world\\n!"', ')']

    Since symbols cannot start with a digit, this function should separate the
    numerical literal from the symbol when things like this happen:

    >>> list(tokenize('(print 8-dogcows)'))
    ['(', 'print', '8', '-dogcows', ')']
    >>> list(tokenize('(print -8.0-dogcows)'))
    ['(', 'print', '-8.0', '-dogcows', ')']

    And since symbols can have digits and dots in the middle, make sure these
    are parsed properly:

    >>> list(tokenize('(print dogcows-8.0)'))
    ['(', 'print', 'dogcows-8.0', ')']

    Quoted things should be emitted as quoted:

    >>> list(tokenize("(print 'hello-world '4 '8.0)"))
    ['(', 'print', "'hello-world", "'4", "'8.0", ')']

    And since symbols and quoted things cannot contain quotes in the middle:

    >>> list(tokenize("(print'hello-world'4'8.0)"))
    ['(', 'print', "'hello-world", "'4", "'8.0", ')']
    >>> list(tokenize("(print'8.0-dogcows)"))
    ['(', 'print', "'8.0", '-dogcows', ')']
    >>> list(tokenize("(print'-8.0-dogcows)"))
    ['(', 'print', "'-8.0", '-dogcows', ')']

    Shebang lines **only at the front of the string, before any whitespace**
    should be ignored, and not emitted as a token:

    >>> list(tokenize("#!/usr/bin/env slyther\n(print 1)\n"))
    ['(', 'print', '1', ')']
    >>> list(tokenize("#!slyther\n(print 1)"))
    ['(', 'print', '1', ')']
    >>> list(tokenize(" #!/usr/bin/env slyther\n(print 1)\n"))
    ['#!/usr/bin/env', 'slyther', '(', 'print', '1', ')']

    Comments start at a semicolon and go until the end of line (or,
    potentially the end of the input string). Note that string literals
    might contain semicolons: these don't start a comment, beware.
    Comments should not be emitted from the tokenizer.

    >>> list(tokenize(
    ...     '(here-comes; a comment!\n "no comment ; here";comment()\n)'))
    ['(', 'here-comes', '"no comment ; here"', ')']
    >>> list(tokenize('; commments can contain ; inside them\n'))
    []

    When an error is encountered, ``SyntaxError`` should be raised:

    >>> list(tokenize("(' )"))        # what are you trying to quote?
    Traceback (most recent call last):
        ...
    SyntaxError: malformed tokens in input
    >>> list(tokenize("'"))
    Traceback (most recent call last):
        ...
    SyntaxError: malformed tokens in input
    >>> list(tokenize("(''x)"))
    Traceback (most recent call last):
        ...
    SyntaxError: malformed tokens in input
    >>> list(tokenize(r'(print "Hello, World!\")'))   # unclosed string
    Traceback (most recent call last):
        ...
    SyntaxError: malformed tokens in input

    Don't worry about handling unmatched parens, etc. This will be the
    parser's job! In other words, the tokenizer should be no smarter
    than it needs to be to do its job.

    >>> list(tokenize("((("))
    ['(', '(', '(']

    .. hint::

        Make good use of regular expression(s), and your life will be
        much easier. I was able to implement mine in only a few lines
        of code, using one giant regular expression!

    """
    raise NotImplementedError("Deliverable 2")


def parse(tokens):
    r"""
    This generator function takes a token generator object (from the
    ``tokenize`` function) and generates AST elements.

    >>> tokens = [
    ...     '(', 'define', '(', 'do-123', 'fun', ')',
    ...         '(', 'map', 'fun', "'(", '1', '2', '3', ')', ')', ')']
    >>> parser = parse(iter(tokens))
    >>> se = next(parser)
    >>> se
    (define (do-123 fun) (map fun '(1 2 3)))
    >>> type(se)
    <class 'slyther.types.SExpression'>
    >>> type(se.car)
    <class 'slyther.types.Symbol'>
    >>> quoted_list = se.cdr.cdr.car.cdr.cdr.car
    >>> quoted_list
    '(1 2 3)
    >>> type(quoted_list)
    <class 'slyther.types.Quoted'>
    >>> type(quoted_list.elem)
    <class 'slyther.types.SExpression'>

    Another example, showing how numerics work:

    >>> tokens = ['(', 'print', '1', "'-2", "'3.0", '-4.', ')']
    >>> parser = parse(iter(tokens))
    >>> se = next(parser)
    >>> numbers = se.cdr
    >>> numbers
    (1 '-2 '3.0 -4.0)
    >>> [type(x) for x in numbers]   # doctest: +NORMALIZE_WHITESPACE
    [<class 'int'>,
     <class 'slyther.types.Quoted'>,
     <class 'slyther.types.Quoted'>,
     <class 'float'>]

    The parser should be able to handle literals that even occur
    outside of an s-expression:

    >>> tokens = ['1', '(', '2', '3', ')', '"string lit"']
    >>> parser = parse(iter(tokens))
    >>> next(parser)
    1
    >>> next(parser)
    (2 3)
    >>> next(parser)
    "string lit"

    The parser should make use of ``parse_strlit`` to parse string
    literals:

    >>> tokens = [r'"this is my\" fancy\n\estring literal"']
    >>> parser = parse(iter(tokens))
    >>> next(parser)
    "this is my\" fancy\n\x1bstring literal"

    When an s-expression is not closed, a ``SyntaxError`` should be
    raised:

    >>> tokens = ['(', ')', '(', 'print']
    >>> parser = parse(iter(tokens))
    >>> next(parser)
    NIL
    >>> next(parser)
    Traceback (most recent call last):
        ...
    SyntaxError: s-expression not closed

    Likewise, when there's too many closing parens:

    >>> tokens = ['(', ')', ')', '(', 'print', ')']
    >>> parser = parse(iter(tokens))
    >>> next(parser)
    NIL
    >>> next(parser)
    Traceback (most recent call last):
        ...
    SyntaxError: too many closing parens

    """
    raise NotImplementedError("Deliverable 2")


def parse_strlit(tok):
    r"""
    This function is a helper method for ``parse``. It takes a string
    literal, raw output from the tokenizer, and converts it to a
    ``slyther.types.String``.

    It should support the following translations:

    +-----------------+--------------------+
    | Escape Sequence | Resulting Output   |
    +=================+====================+
    | ``\0``          | ASCII Value 0      |
    +-----------------+--------------------+
    | ``\a``          | ASCII Value 7      |
    +-----------------+--------------------+
    | ``\b``          | ASCII Value 8      |
    +-----------------+--------------------+
    | ``\e``          | ASCII Value 27     |
    +-----------------+--------------------+
    | ``\f``          | ASCII Value 12     |
    +-----------------+--------------------+
    | ``\n``          | ASCII Value 10     |
    +-----------------+--------------------+
    | ``\r``          | ASCII Value 13     |
    +-----------------+--------------------+
    | ``\t``          | ASCII Value 9      |
    +-----------------+--------------------+
    | ``\v``          | ASCII Value 11     |
    +-----------------+--------------------+
    | ``\"``          | ASCII Value 34     |
    +-----------------+--------------------+
    | ``\\``          | ASCII Value 92     |
    +-----------------+--------------------+
    | ``\x##``        | Hex value ``##``   |
    +-----------------+--------------------+
    | ``\0##``        | Octal value ``##`` |
    +-----------------+--------------------+

    >>> parse_strlit(r'"\0"')
    "\x00"
    >>> parse_strlit(r'"\e"')
    "\x1b"
    >>> parse_strlit(r'"\x41"')
    "A"
    >>> parse_strlit(r'"\x53\x6c\x79\x74\x68\x65\x72\x4C\x69\x73\x70"')
    "SlytherLisp"
    >>> parse_strlit(r'"this is my\" fancy\n\estring literal"')
    "this is my\" fancy\n\x1bstring literal"

    Patterns which do not match the translations should be left alone:

    >>> parse_strlit(r'"\c\d\xzz"')
    "\\c\\d\\xzz"

    Octal values should only expand when octal digits (0-7) are used:

    >>> parse_strlit(r'"\077"')
    "?"
    >>> parse_strlit(r'"\088"') # a \0, followed by two 8's
    "\x0088"

    Even though this is similar to Python's string literal format,
    you should not use any of Python's string literal processing
    utilities for this: tl;dr do it yourself.

    .. hint::

        Implement similar to how you tokenized and parsed the source
        code: break the string into tokens (either escape sequences
        or letters), then translate and join the tokens.

    Various other test cases follow:

    >>> import string
    >>> parse_strlit('"'
    ...     + ''.join('\\' + c for c in string.ascii_lowercase)
    ...     + '"')
    "\x07\x08\\c\\d\x1b\x0c\\g\\h\\i\\j\\k\\l\\m\n\\o\\p\\q\r\\s\t\\u\x0b\\w\\x\\y\\z"
    >>> parse_strlit('"'
    ...     + ''.join('\\' + c for c in string.ascii_uppercase)
    ...     + '"')
    "\\A\\B\\C\\D\\E\\F\\G\\H\\I\\J\\K\\L\\M\\N\\O\\P\\Q\\R\\S\\T\\U\\V\\W\\X\\Y\\Z"

    """
    raise NotImplementedError("Deliverable 2")
