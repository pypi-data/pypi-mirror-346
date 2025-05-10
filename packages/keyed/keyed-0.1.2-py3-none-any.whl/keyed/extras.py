import io
from contextlib import redirect_stdout

from .constants import EXTRAS_INSTALLED

__all__ = ["Editor", "FreeHandContext", "post_process_tokens"]

if EXTRAS_INSTALLED:
    with redirect_stdout(io.StringIO()):
        from keyed_extras import Editor, FreeHandContext, post_process_tokens  # type: ignore
else:

    def post_process_tokens(code, tokens, filename):
        """This function intentionally does nothing."""
        return tokens

    class Editor:
        def find(self, x, y, frame) -> tuple[None, float]:
            return None, float("inf")

    from .context import ContextWrapper as FreeHandContext  # noqa: F401


del EXTRAS_INSTALLED
del redirect_stdout
del io
