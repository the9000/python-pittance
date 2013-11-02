# tests for Result class.

import unittest

from result import Result

class ValueErrorTest(unittest.TestCase):

  def testCreateValue(self):
    r = Result.asValue(1)
    self.assertTrue(r.has_value)
    self.assertEquals(1, r.value)
    self.assertIsNone(r.error)

  def testCreateError(self):
    r = Result.asError("ouch")
    self.assertFalse(r.has_value)
    self.assertEquals("ouch", r.error)
    self.assertIsNone(r.value)

  def testReprValue(self):
    r = Result.asValue(1)
    self.assertEquals("Result.asValue(1)", repr(r))

  def testReprError(self):
    r = Result.asError("foo")
    self.assertEquals("Result.asError('foo')", repr(r))


if __name__ == '__main__':
    unittest.main()
