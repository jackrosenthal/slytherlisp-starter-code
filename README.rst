SlytherLisp
===========

.. This README is in reStructuredText format. If you have Docutils installed,
   you can validate the format and make an HTML copy by typing:
     $ rst2html README.rst >README.html

.. Replace with your own name and Mines email, keep the same format (including
   pointy brackets on the email!). The ``setup.py`` will parse this and use
   this value in various places.

:Implemented By:
   Your Name <youruser@mines.edu>
:Deliverable: 1

SlytherLisp is a lexically-scoped Scheme-like Lisp dialect for the Language
Design Project in CSCI-400. If you aren't familiar with Lisp, expressions are
written in parentheses and are called s-expressions. For example, adding 3 and
4 is written as::

    (+ 3 4)

The ``+`` is the function we are calling, and ``3`` and ``4`` are the
arguments. This language only uses prefix notation, no infix or postfix
notation is used.

In SlytherLisp, there are two kinds of things we can call by placing in the
parentheses:

:Functions: Whose arguments are evaluated, and the function returns a value to
            substitute where it was written.
:Macros:    Whose arguments are not evaluated, and the macro returns an
            expression to fill in its place.

For example, the ``define`` macro defines functions::

    (define (f x y)
        (* (+ x y) y))

In this case, we defined a function named ``f`` which takes arguments ``x`` and
``y`` and returns ``(x + y) * y``. It is necessary for ``define`` to be a macro
since it needs the arguments unevaluated to create the definition.

Further examples of SlytherLisp code can be found in the ``examples``
directory. Also, as a beginner reference to Scheme and Lisp-like languages, the
`Structure and Interpretation of Computer Programs`__ (available *free* online)
book is recommended, even though SlytherLisp is not exactly the same as Scheme.

__ https://mitpress.mit.edu/sicp/full-text/book/book.html

Getting Started with the Starter Code
-------------------------------------

1. Open this ``README.rst`` file in a text editor and make changes to the name
   and email up top. Save the file before proceeding to step 2.

2. Install an editable copy of the application::

        $ pip3 install -e . --user

   * ``pip3`` is the tool used to install Python packages. On some systems, you
     may need to use ``python3 -m pip`` instead. If that does not work, you
     will need to install ``pip``, see this__ page for instructions on Linux.

     __ https://packaging.python.org/guides/installing-using-linux-tools/

   * ``-e`` says to install an editable copy. If you omit this, you'll need to
     re-install every time you make changes.

   * ``--user`` says to install for the local user only. This way you do not
     need to use ``sudo``. The binaries should end up in something like
     ``$HOME/.local/bin``: make sure this is in your ``PATH``.

3. After installing the application, you should have access to the ``slyther``
   program anywhere on your system. Confirm you can run the ``slyther``
   command (even though it may result in a ``NotImplementedError``). Check
   ``slyther --help`` for potential command line arguments.

4. Open up the files in the ``slyther`` directory and familiarize yourself with
   their structure.

   - The ``raise NotImplementedError(...)`` lines are for you to replace with
     working code. Typically, they will state which deliverable you need to
     complete them for.

   - The functions typically have a description of how they should work at the
     top in a docstring. This docstring usually has doctests in it too: that
     is, those lines that start with ``>>>`` in the docstring are actually unit
     tests as well! You are free to change these docstrings and the tests (and
     running the tests on your code should reflect your changes), but the
     grading script will run the original (unmodified) unit tests: so make sure
     that your code works with the unit tests you were given.

   - You are free to implement helper functions, etc., as you need: in fact,
     this project would be very hard to do without doing so.

   - If you change how a particular interface works in the application, leave
     the original interface in, and have that call the modified interface. This
     is how (you, and I) can test your code even if you change the application
     structure.

5. Start coding!

Running Tests
-------------

To run the tests, type ``./run_tests.py`` from the base directory (where
``README.rst`` is located). You will need to specify at least one of four
flags: ``--d1``, ``--d2``, ``--d3``, or ``--tco``, which runs the tests for
Deliverable 1, 2, 3, or tail call optimization.

When you run the tests, if it prints nothing and returns zero, this is good
news: the tests ran as expected. If you would like to see each and every
assertion that is being made (just so you know it's doing things), you can pass
the ``--verbose`` or ``-v`` flag as well.

Style Checking
--------------

The file ``.flake8`` defines a set of style checks (PEP 8, plus a few others).
To run the style checks, type ``flake8`` from the base directory. This is the
same way that the code style will be checked when graded.

With ``flake8``, no news is good news as well. If you want to make sure it's
working, add some bad style to your code for a second and see if it errors at
you.

A note on using Git and GitHub
------------------------------

I initialized a Git repository in this directory for you so it is easy to use a
version control system as you work. If you choose to put this repository on a
shared Git-instance (such as GitHub), please **make sure the repository is
private!** This includes after you finish the course: you should not share your
implementation with others.

One advantage of using GitHub is that you can share your repository with me if
you need help with something, I can pull your code and take a look.

Using Git is optional.

Submitting your Deliverables
----------------------------

To make a ``.tar.bz2`` file for submission, type ``./make-submission.sh`` from
the same directory this README is located in. Then, submit the ``.tar.bz2``
file to Gradescope.
