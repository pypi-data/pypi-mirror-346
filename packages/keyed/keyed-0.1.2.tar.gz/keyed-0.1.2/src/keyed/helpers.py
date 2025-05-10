"""Miscellaneous helpers."""

from functools import wraps
from typing import Any, Callable, Protocol, TypeVar, cast, runtime_checkable

__all__ = ["Freezeable", "guard_frozen", "freeze"]


@runtime_checkable
class Freezeable(Protocol):
    """Make a class Hashable by breaking it's ability to setattr.

    When an object is not frozen, we allow it to setattr but do not allow it to hash.
    Once an object is frozen, setattr breaks but a very simple id-based hash is enabled.

    Todo:
        Remove the need for this class by writing proper hash/eq methods for all classes.
    """

    _is_frozen: bool

    def __init__(self) -> None:
        self._is_frozen = False

    def __hash__(self) -> int:
        if not self._is_frozen:
            raise TypeError("Not frozen. Need to freeze to make hashable.")
        return id(self)

    def __setattr__(self, name: str, value: "Freezeable", /) -> None:
        if hasattr(self, "_is_frozen") and self._is_frozen:
            raise ValueError("Cannot set attribute. Object has been frozen.")
        object.__setattr__(self, name, value)

    def _freeze(self) -> None:
        """Freeze the object to enable caching."""
        self._is_frozen = True


T = TypeVar("T", bound=Callable[..., Any])


def guard_frozen(method: T) -> T:
    """Check if the object is frozen before allowing method execution.

    Args:
        method: The method to be decorated.

    Returns:
        The decorated method.
    """

    @wraps(method)
    def wrapper(self: Freezeable, *args: Any, **kwargs: Any) -> Any:
        if hasattr(self, "_is_frozen") and self._is_frozen:
            raise ValueError(f"Can't call {method.__name__}. Object is frozen.")
        return method(self, *args, **kwargs)

    return cast(T, wrapper)


def freeze(method: T) -> T:
    """Call self.freeze() on the object before executing the method.

    Args:
        method: The method to be decorated.

    Returns:
        The decorated method.
    """

    @wraps(method)
    def wrapper(self: Freezeable, *args: Any, **kwargs: Any) -> Any:
        if not self._is_frozen:
            self._freeze()
        return method(self, *args, **kwargs)

    return cast(T, wrapper)
