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
"""Provides a namespace for building a building filtering suits based on
characteristics of strings.

At the top level, it provides one function, `get_filterspace()`, which returns
an instance of the namespace defined in the _filterspace module.

Basically, it gives you a bunch of decorators and convinience fucntions for
registering a bunch of tests and then you get a Filter class for quickly
running those tests against a string.

for more info, consult:
https://github.com/FID-Judaica/filtermaker
"""
import importlib, sys


def get_filterspace():
    try:
        del sys.modules["_filtermaker"]
    except KeyError:
        pass
    from . import _filterspace

    return _filterspace
