import faulthandler
import os
import sys
import unittest

from collections.abc import Iterator
from typing import Any


def getTests(suite: Any) -> Iterator[Any]:
    for test in suite:
        if unittest.suite._isnotsuite(test):  # type: ignore
            yield test
        else:
            yield from getTests(test)


def runTests(pattern: str | None) -> bool:
    faulthandler.enable()

    print(f'Running src.eyecandy\nPython version: {sys.version}')

    path = os.path.dirname(os.path.abspath(__file__))
    suite = unittest.TestLoader().discover(path)

    filtered = unittest.TestSuite()

    if pattern is not None:
        for test in getTests(suite):
            if pattern in str(test.id()):
                filtered.addTest(test)
    else:
        filtered = suite

    result = unittest.TextTestRunner(verbosity=2).run(filtered)
    return result.wasSuccessful()
