# Copyright 2017, Goethe University
#
# This library is free software; you can redistribute it and/or
# modify it either under the terms of:
#
#   the EUPL, Version 1.1 or – as soon they will be approved by the
#   European Commission - subsequent versions of the EUPL (the
#   "Licence"). You may obtain a copy of the Licence at:
#   https://joinup.ec.europa.eu/software/page/eupl
#
# or
#
#   the terms of the Mozilla Public License, v. 2.0. If a copy of the
#   MPL was not distributed with this file, You can obtain one at
#   http://mozilla.org/MPL/2.0/.
#
# If you do not alter this notice, a recipient may use your version of
# this file under either the MPL or the EUPL.

import unicodedata as ud
import collections
import re
from functools import wraps

_tests = {}


def register(func, name=None):
    if name:
        func.__name__ = name

    _tests[func.__name__] = func
    return func


def registrar(func):
    @wraps(func)
    def wrapped(arg, name):
        return register(func(arg), name)

    return wrapped


class Filter(collections.UserString):
    def __init__(self, line, *props):
        self.data = ud.normalize("NFC", line).lower()
        if props == ["ALL"]:
            self.props = set(k for k, v in _tests.items() if v(self))
        elif props:
            self.props = set(p for p in props if _tests[p](self))
        else:
            self.props = set()

    def has(self, *props):
        for prop in props:
            if prop in self.props:
                return True
            elif _tests[prop](self):
                self.props.add(prop)
            else:
                return False

        return True


@registrar
def haschars(charset):
    return lambda line: any(c for c in line.data if c in charset)


@registrar
def hascluster(charset):
    return lambda line: any(True for clstr in charset if clstr in line.data)


@registrar
def onlycharset(charset):
    return lambda line: all(
        c in charset for c in line.data if ud.category(c)[0] == "L"
    )


@registrar
def hasregex(regex):
    if isinstance(regex, str):
        regex = re.compile(regex)
    return lambda line: bool(regex.search(line.data))
