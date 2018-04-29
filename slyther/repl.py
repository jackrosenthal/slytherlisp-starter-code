def repl(interpreter):
    """
    Take an interpreter object and give a REPL on it. Should not return
    anything: just a user interface at the terminal. For example::

        $ slyther
        > (print "Hello, World!")
        Hello, World!
        NIL
        > (+ 10 10 10)
        30

    When the user presses ^D at an empty prompt, the repl should exit.

    When the user presses ^C at any prompt (whether there is text or
    not), the input should be cancelled, and the user prompted again::

        $ slyther
        > (blah bla^C
        >                   <-- ^C resulted in new prompt line

    Should be pretty easy. No unit tests for this function, but I will
    test the interface works when I grade it.
    """
    raise NotImplementedError("Deliverable 3")
