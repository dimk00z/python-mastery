from typing import Any


class Structure:
    _fields = ()

    def __init__(self, *args) -> None:
        if len(args) != len(self._fields):
            raise TypeError("Expected %d arguments", len(self._fields))
        for name, arg in zip(self._fields, args):
            setattr(self, name, arg)

    def __repr__(self) -> str:
        return "".join(
            (
                f"{self.__class__.__name__}(",
                ", ".join((f"{getattr(self, atr)!r}" for atr in self._fields)),
                ")",
            )
        )

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name.startswith("_") or __name in self._fields:
            return super().__setattr__(  # type: ignore
                __name,
                __value,
            )
        raise AttributeError("No attribute %s" % __name)
