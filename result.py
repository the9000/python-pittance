# The Either or Result, a functional alternative to exceptions.

class Result(object):
  """An exclusive pair, Value or Error, akin to Scala's Either.

  Discriminated by .has_value.
  Immutable.
  """

  @classmethod
  def asValue(cls, payload):
    """Returns a value-carrying Result."""
    return cls(payload, None)

  @classmethod
  def asError(cls, payload):
    """Returns an error-carrying Result."""
    return cls(None, payload)

  # TODO: pass __has_value explicitly
  def __init__(self, value, error):
    """Must be considered private. Use .asValue or .asError classmethods."""
    assert (value is None) ^ (error is None), 'Set either value or error'
    if error:
      self.__payload = error
      self.__has_value = False
    else:
      self.__payload = value
      self.__has_value = True

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
  def _errorFromException(cls, e):
    return cls.asError((e.__class__, e.message))
      
  @classmethod
  def ize(cls, function, exceptions=(StandardError,)):
    """A function decorator, makes a plain function return a Result.

    Args:
      function: a plain function that may raise excpetions.
      exceptions: a list of exception classes to turn into errors.

    Returns:
      function wrapped in a handler that converts exceptions and return value.
    """
    # TODO: allow stacktrace collection if desired
    def rezultizeWrapped(*args, **kwargs):
      try:
        return cls.asValue(function(*args, **kwargs))
      except exceptions as e:
        return cls._errorFromException(e)

    return rezultizeWrapped
      
      
  # Implement fmap for several popular types

  def fmapExcept(self, function, exceptions=(StandardError,)):
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
      return self._errorFromException(e)

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


