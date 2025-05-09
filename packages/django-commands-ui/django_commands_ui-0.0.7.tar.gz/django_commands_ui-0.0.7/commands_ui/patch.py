import builtins
import contextlib
import io
import sys
import types
import typing

import structlog


class PatchedPrint(contextlib.AbstractContextManager):
    _builtin_print = print

    def __enter__(self) -> typing.Any:
        builtins.print = self.redirected_print  # type: ignore[assignment]

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> typing.Literal[False]:
        builtins.print = self._builtin_print
        return False

    def redirected_print(self, message: typing.Any) -> None:
        raise NotImplementedError


class RedirectedPrint(PatchedPrint):
    """
    A context manager that redirects the text of any `print()` calls to the given file-like object.

    This effectively changes the default `file` keyword argument of the built-in `print()` function
    while in the context, from `sys.stdout` to the specified file-like object.  This allows logging
    to continue as normal, even if that is directed to STDOUT, whilst capturing any `print`ed text
    to either a file, an alternative system stream (such as STDERR) or an in-memory stream.
    """

    def __init__(
        self,
        destination: typing.TextIO | None = None,
        filename: str = "",
        close: bool = True,
        **open_kwargs: typing.Any,
    ) -> None:
        super().__init__()

        self.destination = destination
        self.filename = filename
        self.open_kwargs = open_kwargs
        self.close = close

        self.open_kwargs.setdefault("mode", "a+")

    def __enter__(self) -> typing.TextIO:
        self.destination = self.destination or (
            open(self.filename, **self.open_kwargs) if self.filename else io.StringIO()
        )
        super().__enter__()
        return self.destination

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> typing.Literal[False]:
        handled = super().__exit__(exc_type, exc_value, traceback)
        if self.close and self.destination:
            self.destination.close()
        return handled

    def redirected_print(self, message: typing.Any) -> None:
        self._builtin_print(message, file=self.destination)


class LoggedPrint(PatchedPrint):
    """
    A context manager that redirects the text of any `print()` calls to info logs.

    This effectively changes calls to `print()` into `logger.info()` calls.
    """

    def __init__(self, area: str = "print") -> None:
        self.logger = structlog.get_logger(f"events.{area}")

    def redirected_print(self, message: typing.Any) -> None:
        self.logger.info(message)
