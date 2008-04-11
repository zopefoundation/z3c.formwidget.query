import doctest
import unittest
from zope import interface, component, schema
from zope.testing import doctestunit
from zope.app.testing import setup

def setUp(test):
    test.globs = dict(
        root=setup.placefulSetUp(True),
        pprint=doctestunit.pprint,
        interface=interface,
        component=component,
        schema=schema)
        
def tearDown(test):
    setup.placefulTearDown()

def test_suite():
    return unittest.TestSuite((
        doctestunit.DocFileSuite(
            'README.txt',
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
