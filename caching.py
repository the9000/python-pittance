"""Calculate data fewer times than a correponding function is called."""

import pickle

class Cache(object):
  NONE_OBJECT = object() # unique placeholder instead of None

  def __init__(self):
    self.storage = {}  # keyed by (func, pickled_args)

  def retrieve(self, func, args, kwargs):
    pickled_arglist = pickle.dumps((args, kwargs))
    storage_key = (func, pickled_arglist)
    value = self.storage.get(storage_key, self.NONE_OBJECT)
    if value is self.NONE_OBJECT:
      value = func(*args, **kwargs)
      self.storage[storage_key] = value
    return value

  def keep(self, func):
    """Decorator to use with functions."""
    def cachedFunc(*args, **kwargs):
      return self.retrieve(func, args, kwargs)
    cachedFunc.__name__ = func.__name__
    return cachedFunc
      