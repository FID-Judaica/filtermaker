import unicodedata
import collections
import re
import functools
from dataclasses import dataclass
from typing import Callable, Collection, Iterable, Concatenate, ParamSpec

P = ParamSpec("P")


@dataclass(slots=True)
class PropertyText:
    """PropertyText should be subclassed to create a class where actual
    properties are defined.

    These properties will normally be defined as methods, like so:

        @chainable
        def contains_h(text: str) -> bool:
            return "h" in text
    

    That is, the method will be decorated as `@chainable`, it will take only
    one string as an input parameter, and it will return a bool.
    

    These methods may be defined with property builders. Those provided are
    `haschars`, `hascluster`, `onlycharset` and `hasregex`.

         contains_h_p_or_s = haschars({"h", "p", "s"})
    
    further property builders can be defined with `chainable builder`.
    """
    text: str
    status: bool

    @classmethod
    def new(cls, text: str):
        return cls(unicodedata.normalize("NFC", text).lower(), True)

    def has(self, props: str):
        return all(getattr(self, p) for p in props)

    def __bool__(self):
        return self.status

    __call__ = __bool__


@dataclass(slots=True)
class chainable:
    method: Callable[[str], bool]

    def __get__(self, obj: PropertyText, objcls=PropertyText):
        if not obj.status:
            return obj

        return objcls(obj.text, self.method(obj.text))


def chainable_builder(func: Callable[Concatenate[str, P], bool]):
    @functools.wraps(func)
    def method_builder(*args: P.args, **kwargs: P.kwargs):
        @chainable
        def method(ft: PropertyText):
            return func(ft.text, *args, **kwargs)

        return method

    return method_builder


@chainable_builder
def haschars(s: str, charset: Collection[str]):
    return any(c for c in s if c in charset)


@chainable_builder
def hascluster(s: str, charset: Iterable[str]):
    return any(True for clstr in charset if clstr in s)


@chainable_builder
def onlycharset(s: str, charset: Collection[str]):
    return all(c in charset for c in s if unicodedata.category(c)[0] == "L")


@chainable_builder
def hasregex(s: str, regex: re.Pattern):
    return bool(regex.search(s))
