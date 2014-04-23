import unittest

from caching import Cache

class Simplest(unittest.TestCase):

  def setUp(self):
    pass

  def testFactorial(self):
    cache = Cache()
    invocations = [] # args of actual invocations

    @cache.keep
    def fact(n):
      invocations.append(n)
      if n == 1:
        return 1
      return n * fact(n - 1)
    fact(5)
    f6 = fact(6)
    self.assertEquals(720, f6)
    self.assertEquals([5, 4, 3, 2, 1, 6], invocations)

  def testListArgs(self):
    cache = Cache()
    invocations = [] # args of actual invocations

    @cache.keep
    def sum_(numbers):
      invocations.append(True)
      return sum(numbers)

    v1 = sum_(list(range(10)))
    v2 = sum_([0, 1, 2, 3, 4] + [5, 6, 7, 8, 9])
    self.assertEquals(45, v1)
    self.assertEquals(45, v2)
    self.assertEquals(1, len(invocations))

  def testDictListArgs(self):
    cache = Cache()
    invocations = [] # args of actual invocations

    @cache.keep
    def sum_(num_dict):
      invocations.append(True)
      num_lists = num_dict.values()
      nums = []
      for nl in num_lists:
        nums.extend(nl)  # can't call mu directly! :)
      return sum(nums)

    v1 = sum_({'a': [1,2,3], 'b': [4,5,6]})
    v2 = sum_({'b': ([4,5] + [6]), 'a': [1,2,3]})
    self.assertEquals(21, v1)
    self.assertEquals(21, v2)
    self.assertEquals(1, len(invocations))

if __name__ == '__main__':
  unittest.main()
