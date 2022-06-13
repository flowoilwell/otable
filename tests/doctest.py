"""An entry point for running the doctests."""

import manuel.codeblock
import manuel.doctest
import manuel.testing
import unittest


def test_suite():
    """Construct a Manuel-enhanced test suite for running the doctests."""
    m = manuel.doctest.Manuel()
    m += manuel.codeblock.Manuel()
    return manuel.testing.TestSuite(m, '../README.rst')


if __name__ == '__main__':  # pragma: no cover
    unittest.TextTestRunner().run(test_suite())
