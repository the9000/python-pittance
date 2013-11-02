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
    r = Result.asError('ouch')
    self.assertFalse(r.has_value)
    self.assertEquals('ouch', r.error)
    self.assertIsNone(r.value)

  def test_ReprValue_scalar(self):
    r = Result.asValue(1)
    self.assertEquals('Result.asValue(1)', repr(r))

  def test_ReprValue_tuple(self):
    r = Result.asValue((1, 2))
    self.assertEquals('Result.asValue((1, 2))', repr(r))

  def test_ReprError_scalar(self):
    r = Result.asError('foo')
    self.assertEquals('Result.asError(\'foo\')', repr(r))

  def test_ReprError_list(self):
    r = Result.asError(['foo', 'bar'])
    self.assertEquals("Result.asError(['foo', 'bar'])", repr(r))


class FMapTest(unittest.TestCase):

  def test_fmapExcept_Value(self):
    r = Result.asValue('1')
    q = r.fmapExcept(int)
    self.assertTrue(q.has_value)
    self.assertEquals(1, q.value)

  def test_fmapExcept_Error(self):
    r = Result.asValue('foo')
    q = r.fmapExcept(int)
    self.assertFalse(q.has_value)
    self.assertEquals(ValueError, q.error[0])

  def test_fmapExcept_UncaughtException(self):
    r = Result.asValue('foo')
    self.assertRaises(
      ValueError,
      r.fmapExcept, int, (KeyError,)
    )

  def test_Resultize_Value(self):
    r = Result.ize(int)('1')
    self.assertEquals(1, r.value)

  def test_Resultize_Error(self):
    r = Result.ize(int)('moo')
    self.assertEquals(ValueError, r.error[0])


if __name__ == '__main__':
  unittest.main()
