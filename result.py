# Encoding: utf-8

from collections import namedtuple
import traceback

# The Result, neé Either, a functional alternative to exceptions.

class Result(object):
  """An exclusive pair, Value or Error, akin to Scala's Either.

  Discriminated by .has_value.
  Immutable.
  """

  @classmethod
  def asValue(cls, payload):
    """Returns a value-carrying Result."""
    return cls(payload, True)

  @classmethod
  def asError(cls, payload):
    """Returns an error-carrying Result."""
    return cls(payload, False)

  def __init__(self, payload, has_value):
    """Must be considered private. Use .asValue or .asError classmethods."""
    self.__payload = payload
    self.__has_value = has_value

  @property
  def value(self):
    """Value payload if the Result is a value, else None."""
    if self.__has_value:
      return self.__payload

  @property
  def error(self):
    """Error payload if the Result is an error, else None."""
    if not self.__has_value:
      return self.__payload

  @property
  def has_value(self):
    """True iff the Result carries a value."""
    return self.__has_value

  def __repr__(self):
    if self.__has_value:
      return 'Result.asValue(%r)' % (self.__payload,)
    else:
      return 'Result.asError(%r)' % (self.__payload,)

  @classmethod
  def _errorFromException(cls, e, want_stacktrace):
    stacktrace = traceback.format_exc() if want_stacktrace else None
    return cls.asError(CaughtException(e, stacktrace))
          
  @classmethod
  def ize(cls, exceptions=(StandardError,), want_stacktrace=True):
    """A function decorator, makes a plain function return a Result.

    Args:
      function: a plain function that may raise excpetions.
      exceptions: a list of exception classes to turn into errors.
      want_stacktrace: if True,

    Returns:
      function wrapped in a handler that converts exceptions and return value.
      If fcunction's evaluation results in an exception,
      an Result.asError(CaughtException(...))) is returned;
      else, Result.asValue(function's return value) is returned.
    """
    def mkwrapper(func, exceptions, want_stacktrace):
      def wrapper(*args, **kwargs):
        try:
          return cls.asValue(func(*args, **kwargs))
        except exceptions as e:
          return cls._errorFromException(e, want_stacktrace)
      wrapper.__doc__ = func.__doc__
      wrapper.__name__ = 'Result.ize<' + func.__name__ + '>'
      return wrapper

    if callable(exceptions):
      # we are called without param list, as @Result.ize
      return mkwrapper(exceptions, (StandardError,), want_stacktrace)
    else:
      # we are called as @Result.ize(...)
      def deco(f):
        return mkwrapper(f, exceptions, want_stacktrace)
      return deco


  # Implement fmap for several popular types

  def fmapExcept(self, function, exceptions=(StandardError,),
                 want_stacktrace=True):
    """fmap for exceptions: Converts given exceptions into error value.

    Args:
      function: a 1-argument callable; self.value will be the argument.
      exceptions: a list of exception classes to catch.

    Returns:
      either asValue(function(self.value)) if none of exceptions was raised,
      or asError((exception class, exception message)).
    """
    if not self.has_value:
      return self
    try:
      return self.asValue(function(self.value))
    except exceptions as e:
      return self._errorFromException(e, want_stacktrace)

  def getItem(self, key):
    """Emulates doing index access, like [key]; wraps access errors.

    Args:
      key: mapping access key.

    Returns:
      if self is a value, and value[key] succeeds: Result.asValue(value[key])
      else if value[key] fails: Result.asError(the index error message)
      else if self is an error: self.
    """
    return self.fmapExcept(lambda x: x[key], (IndexError, KeyError))

  __getitem__ = getItem

  @classmethod
  def map(cls, function, sequence, exceptions=(StandardError,)):
    """Replacement for built-in map(). Wraps every invocation of function.

    Args:
      function: a callable with 1 argument; items from sequence are fed to it.
      sequence: a sequence.

    Returns:
      A list or Results of application of function to each element of sequence.
    """
    return []

  def ParseInt(self):
    """Emulates doing index acces, like [key].

    Args:
      key: mapping access key.

    Returns:
      if self is a value, and value[key] succeeds: Result.asValue(value[key])
      else if value[key] fails: Result.asError(the index error message)
      else if self is an error: self.
    """
    return self._fmap(int, (ValueError,))


CaughtException = namedtuple('CaughtException', ('exception', 'stacktrace'))



def xdec(amt):
  def mkwrapper(f, amt):
    def wrapper(*args, **kwargs):
      return f(*args, **kwargs) - amt  # 1 is the default amt
    wrapper.__doc__ = f.__doc__
    wrapper.__name__ = 'xdec.wrapper(' + f.__name__ + ')'
    return wrapper
    
  if callable(amt):
    # we are called without param list, as @dec
    return mkwrapper(amt, 1)
  else:
    # we are called as @dec(n)
    def deco(f):
      return mkwrapper(f, amt)
    return deco
    

@xdec
def foo1(x):
  return x * 2

@xdec(4)
def foo2(x):
  return x * 2
