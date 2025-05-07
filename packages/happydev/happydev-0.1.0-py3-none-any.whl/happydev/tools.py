"""
This is a small collection of tools that are very useful during development. See their respective docstrings for details on each.
Use install() as a convenience function to install several tools at once.
"""

import builtins
import functools
import logging as stdlib_logging
import sys
import warnings
from contextlib import suppress


TRACEBACK_EXTRA_LINES = 1
TRACEBACK_WORD_WRAP = False
TRACEBACK_SHOW_LOCALS = False

installed_builtins = False
installed_print = False
installed_rich_logger = False
installed_traceback = False


def install_builtins():
    """
    Add several tools to the builtins module, so they can be used anywhere without importing.
    The included tools are:
        pprint() - rich pretty printer - https://rich.readthedocs.io/en/stable/introduction.html?highlight=print#quick-start
        inspect() - rich object inspector - https://rich.readthedocs.io/en/stable/introduction.html?highlight=print#rich-inspect
        ic() - icecream - https://github.com/gruns/icecream
        @snoop - poor man's debugger - https://github.com/cool-RR/PySnooper
    """
    import icecream
    import pysnooper
    import rich
    import rich.file_proxy

    global installed_builtins
    if installed_builtins:
        raise Exception("Tried to install builtin tools twice")

    builtins.pprint = rich.print
    builtins.ic = icecream.ic
    builtins.snoop = pysnooper.snoop
    builtins.inspect = functools.update_wrapper(functools.partial(rich.inspect, private=True), rich.inspect)
    rich.get_console().soft_wrap = True  # disable wrapping because it messes with file redirection. should report bug to rich

    # make ic use rich instead of its own prettyfiers
    def icecream_print(message):
        if isinstance(sys.stderr, rich.file_proxy.FileProxy):
            # this is needed because rich Console ignores the FileProxy and writes directly to the underlying stream
            # i dont quite understand why, because this breaks it's own console redirection
            sys.stderr._FileProxy__console.print(message)
        else:
            rich.print(message, file=sys.stderr)

    icecream.ic.configureOutput(
        prefix='',
        outputFunction=icecream_print,
        # argToStringFunction=rich.pretty.pretty_repr,  # not sure if this will work well, off for safety
    )
    installed_builtins = True


def install_rich_print():
    """
    Replace the default print function with Rich's formatted-and-colored print.
    The standard print is avaliable via default_print().
    """
    import rich

    global installed_print
    if installed_print:
        raise Exception("Tried to override print twice")

    builtins.default_print = builtins.print
    builtins.print = rich.print
    installed_print = True


def install_rich_logger(log_level):
    """
    DEPRECATED: Moved over to loguru, see logging_setup
    Set up Rich's pretty logging handler and bind it to stderr.
    log_level = 'off', 'all', or any of the named levels in the standard logging module.
    """
    import rich.logging

    global installed_rich_logger
    if installed_rich_logger:
        raise Exception("Tried to install rich logger twice")
    warnings.warn("Moved over to loguru, see logging_setup", DeprecationWarning, stacklevel=2)

    log_level = log_level.casefold()
    if log_level == 'off':
        log_level = 'critical'
    if log_level == 'all':
        log_level = 'notset'

    log_level_value = stdlib_logging.getLevelNamesMapping().get(log_level.upper(), None)
    if log_level_value is None:
        raise ValueError(f"Invalid logging level {log_level}")

    stderr_handler = rich.logging.RichHandler(
        level=log_level_value,
        console=rich.console.Console(stderr=True),
        log_time_format="[%X]",
        omit_repeated_times=False,
        rich_tracebacks=True,
        tracebacks_extra_lines=TRACEBACK_EXTRA_LINES,
        tracebacks_word_wrap=TRACEBACK_WORD_WRAP,
        tracebacks_show_locals=TRACEBACK_SHOW_LOCALS,
    )
    root_logger = stdlib_logging.getLogger()
    if root_logger.getEffectiveLevel() > log_level_value:
        root_logger.setLevel(log_level_value)
    stdlib_logging.getLogger().addHandler(stderr_handler)
    installed_rich_logger = True


def install_rich_traceback(force=False):
    """
    Replaces Python built-in traceback handler with Rich's pretty one.
    Set force=True to install it even if another traceback handler was already installed.
    """
    import rich.traceback
    from rich.console import Console

    global installed_traceback
    if installed_traceback:
        raise Exception("Tried to install rich traceback twice")

    def do_install():
        return rich.traceback.install(
            width=max(100, Console(stderr=True).width),
            max_frames=100,
            extra_lines=TRACEBACK_EXTRA_LINES,
            word_wrap=TRACEBACK_WORD_WRAP,
            show_locals=TRACEBACK_SHOW_LOCALS,
        )

    # special case for typer. could send them a pr to get rid of this
    # depending on the ordering, typer may override our hook. nothing we can do about it
    with suppress(ImportError):
        import typer.main

        # since typer only saves the global exception hook at import-time, we update it
        if typer.main._original_except_hook == sys.__excepthook__:
            old_excepthook = do_install()
            typer.main._original_except_hook = sys.excepthook
            sys.excepthook = old_excepthook

        # if typer already installed its exception hook, we override it
        # this is only useful if someone forgot to pass pretty_exceptions_enable=False or _TYPER_STANDARD_TRACEBACK, otherwise should be harmless
        # if these are true, typer does install an exception hook that simply calls the default exception hook, so no harm in overriding
        # probably should just set _TYPER_STANDARD_TRACEBACK
        if sys.excepthook == typer.main.except_hook:
            force = True

    # refuse to override a non-default exception hook
    if sys.excepthook != sys.__excepthook__ and not force:
        raise Exception("Tried to install rich's exception hook, but there was another exception hook already installed!")

    do_install()
    installed_traceback = True


def install(builtins=False, rich_print=False, traceback=False, logger=False):
    """
    Covenience function to install several development utilities. See their respective install functions for more details.
    rich_print: Replace print() with a formatted-and-colored alternative
    traceback: Replace the default traceback printer with a prettier one
    logger: Setup logging at the given level
    """
    if builtins:
        install_builtins()
    if rich_print:
        install_rich_print()
    if traceback:
        install_rich_traceback(force=False)
    if logger is not False:
        from . import logging_setup
        logging_setup.setup_logging(level=logger)
