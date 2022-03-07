import unittest
from unittest import TestCase

import package_name


class TestFun(TestCase):
    def test_is_string(self):
        s = pyares.run()
        self.assertTrue(isinstance(s, basestring))

if __name__ == '__main__':
    unittest.main()