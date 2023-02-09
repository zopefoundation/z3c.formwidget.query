import doctest
import unittest

from z3c.form import testing
from zope import component
from zope import interface
from zope import schema
from zope.testing.cleanup import cleanUp


def setUp(test):
    testing.setUp(test)
    test.globs.update(dict(
        interface=interface,
        component=component,
        schema=schema))


def tearDown(test):
    cleanUp()


def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
            'README.txt',
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
    ))
