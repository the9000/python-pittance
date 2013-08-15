"""General-purpose utility functions and classes."""

# TODO: factor out
class Result(object):
  """An exclusive pair, Value or Error, akin to Scala's Either.

  Discriminated by .has_value.
  Immutable.
  """

  @classmethod
  def AsValue(cls, payload):
    """Returns a value-carrying Result."""
    return cls(payload, None)

  @classmethod
  def AsError(cls, payload):
    """Returns an error-carrying Result."""
    return cls(None, payload)

  # pylint: disable=g-doc-args
  def __init__(self, value, error):
    """Must be considered private. Use .AsValue or .AsError classmethods."""
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
      return 'Result.AsValue(%r)' % self.__payload
    else:
      return 'Result.AsError(%r)' % self.__payload

  # a true fmap would be too anti-idiomatic, so a few special cases follow

  def _Fmap(self, function, exceptions):
    if not self.has_value:
      return self
    try:
      return self.AsValue(function())
    except exceptions as e:
      return self.AsError('%s: %s' % (e.__class__.__name__, e.message))

  def GetItem(self, key):
    """Emulates doing index acces, like [key].

    Args:
      key: mapping access key.

    Returns:
      if self is a value, and value[key] succeeds: Result.AsValue(value[key])
      else if value[key] fails: Result.AsError(the index error message)
      else if self is an error: self.
    """
    return self._fmap(lambda: self.value[key], (IndexError, KeyError))

  __getitem__ = GetItem

  def ParseInt(self):
    """Emulates doing index acces, like [key].

    Args:
      key: mapping access key.

    Returns:
      if self is a value, and value[key] succeeds: Result.AsValue(value[key])
      else if value[key] fails: Result.AsError(the index error message)
      else if self is an error: self.
    """
    return self._fmap(lambda: int(self.value), ValueError)


def OnlyOne(a_list):
  """Asserts that the list has only one element.

  Typical usage: foo = OnlyOne(db.SearchForFoos(id=foo_id))

  Args:
    a_list: an allegedly 1-element list.
  Returns:
    a_list[0], the first element.
  """
  assert len(a_list) == 1, 'Got %d items' % len(a_list)
  return a_list[0]


class Timer(object):
  """Tracks time spent since construction or the previous Yank."""
  # NOTE: we use time.time() and not time.clock() as the latter appears broken

  def __init__(self):
    self.timestamp = time.time()

  def Yank(self):
    """Read and reset the timer.

    Returns:
      number of seconds passed since last Yank() or construction,
      as a floating point per time.time(), expect microsecond resolution.
    """
    last_timestamp = self.timestamp
    self.timestamp = time.time()  # time.clock() gives terrible resolution
    return self.timestamp - last_timestamp


def Percent(value, total):
  """Shows what percent is value relative to total.

  Args:
    value: a number.
    total: a number, including 0.
  Returns:
    Percent as a float, 100 * value / number if number is not 0;
    100.0 if value = total = 0;
    inf otherwise (sign is ignored).
  """
  if total != 0:
    return 100.0 * value / total
  else:
    if value == 0:
      return 100.0  # 0 of 0 is 100%
    else:
      return float('inf')  # value/0 is infinity
