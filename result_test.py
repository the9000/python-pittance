# tests for Result class.

import unittest

from result import Result

class ValueErrorTest(unittest.TestCase):

  def test_Create_asValue(self):
    r = Result.asValue(1)
    self.assertTrue(r.has_value)
    self.assertEquals(1, r.value)
    self.assertIsNone(r.error)

  def test_Create_asError(self):
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
    self.assertEquals(ValueError, q.error.exception.__class__)

  def test_fmapExcept_RaisesUncaughtException(self):
    r = Result.asValue('foo')
    self.assertRaises(
      ValueError,
      r.fmapExcept, int, (KeyError,)
    )

class ResultizeTest(unittest.TestCase):

  def test_Resultize_ReturnsValue(self):
    r = Result.ize(int)('1')
    self.assertEquals(1, r.value)

  def test_Resultize_ReturnsError(self):
    r = Result.ize(int)('moo')
    self.assertEquals(ValueError, r.error.exception.__class__)

  def test_Resultize_DecoNoParameters(self):
    @Result.ize
    def foo(arg):
      return int(arg)
    r = foo('1')
    self.assertEquals(1, r.value)

  def test_Resultize_DecoWithParameters(self):
    @Result.ize(exceptions=(KeyError,))
    def foo(arg):
      return {'a': 1}[arg]
    r = foo('b')
    self.assertEquals(KeyError, r.error.exception.__class__)

  def test_Resultize_GivesTracebackByDefault(self):
    @Result.ize
    def foo(arg):
      return int(arg)
    r = foo('moo')
    self.assertTrue(isinstance(r.error.stacktrace, str))
    self.assertTrue('foo' in r.error.stacktrace)

  def test_Resultize_NoTracebackIfOff(self):
    @Result.ize(want_stacktrace=False)
    def foo(arg):
      return int(arg)
    r = foo('moo')
    self.assertEquals(ValueError, r.error.exception.__class__)
    self.assertTrue(r.error.stacktrace is None)


if __name__ == '__main__':
  unittest.main()
