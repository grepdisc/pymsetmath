"""A module to perform efficient calculations using multisets.

:Author: Hy Carrinski

"""

__docformat__ = 'restructuredtext'

from collections import defaultdict
from itertools import groupby
from operator import itemgetter

def is_nonneg_int(number):
    """Return True for a non-negative integer."""
    try:
        num = int(number)
        return 0 <= num and num == number
    except TypeError:
        return False

class Multiset(object):

    """Support math using multisets. Compute multinomial coefficient.

    """

    def __init__(self, n=0):
        self._data = {0: 1}
        if n > 0:
            self._update_factorial(n)

    def _update_factorial(self, n):
        """Increment cache of computed factorials."""
        for val in xrange(len(self._data), n + 1):
            self._data[val] = val * self._data[val - 1]

    def clear(self):
        """Re-initialize Multiset instance."""
        self._data.clear()
        self._data[0] = 1

    def factorial(self, n):
        """Return factorial from cache, updating cache as needed."""
        try:
            result = self._data[n]
        except KeyError:
            if not is_nonneg_int(n):
                print "Factorial supports only non-negative integers."""
                raise ValueError
            self._update_factorial(n)
            result = self._data[n]
        return result

    def multinomial_coeff(self, iterable):
        """Calculate a multinomial coefficient.

        Inputs
          :grouping: iterable of one or more non-negative integers

        Output
          :coefficient: number of ways to arrange a grouping of categories

        Example
            Given a triplet ``(a, b, c)`` representing a vector of length
            ``a + b + c``, this function returns the number of ways to order
            ``a`` 0's, ``b`` 1's and ``c`` 2's. This is the product of the binomial
            coefficients::

                (a, b, c)! = (a + b + c, a)! * (b + c, b)! * (c, c)!
                           = (a + b + c)! / (a! * b! * c!)

            ::

                >>> mset = Multiset()
                >>> mset.multinomial_coeff((1, 2, 3))
                60

        """

        try:
            iter(iterable)
        except TypeError:
            print "Multinomial coefficient requires an iterable."
            raise
        if not iterable:
            raise ValueError
        total, denominator = 0, 1
        for val in iterable:
            total += val
            denominator *= self.factorial(val)
        return self.factorial(total) // denominator

    def number_of_arrangements(self, iterable):
        """Calculate the number of distinct permutations of a multiset.

        Inputs
          :iterable: a non-ascending sequence of non-negative integers

        Output
          :ways: the number of distinct ways to order the input sequence

        Explanation
           A multiset is an unordered collection (e.g., a bag) which
           may contain repeated elements. The number of arrangements is
           the number of ways the elements can be ordered into distinct
           sequences containing all of the elements.

        """

        try:
            iter(iterable)
        except TypeError:
            print "Number of arrangements requires an iterable."
            raise
        if not iterable:
            print "Number of arrangements requires an iterable of integers."
            raise ValueError
        freq = defaultdict(int)
        for cnt in iterable:
            freq[cnt] += 1
        return self.multinomial_coeff(freq.values())

    def uniq_msets(self, total, length):
        """Yields every multisets of a given size that sum to a given value.

        Yields each and every multiset with a fixed sum by iterating
        through each non-ascending fixed-length sequence of non-negative
        integers in lexicographic order.

        Input
            :total: sum of each multiset to be returned
            :length: maximum length of each multiset to be returned

        Yields
            :iterable: a non-ascending sequence of non-negative integers

        Implementation
            Non-ascending tuples are yielded in lexicographical order
            Yields tuples roughly similar to::

                def uniq_msets(total, length):
                    for s in combinations_with_replacement(range(total + 1), length):
                       if sum(s) == total:
                           yield s

            however, both the order of the elements within tuples and the order
            of yielded tuples are exactly reversed.

        Examples

            >>> mset = Multiset()
            >>> seq = mset.uniq_msets(4, length=4)
            >>> list(seq)
            [(1, 1, 1, 1), (2, 1, 1, 0), (2, 2, 0, 0), (3, 1, 0, 0), (4, 0, 0, 0)]

            >>> mset = Multiset()
            >>> seq = mset.uniq_msets(10, length=3)
            >>> list(seq)
            [(4, 3, 3), (4, 4, 2), (5, 3, 2), (5, 4, 1), (5, 5, 0), (6, 2, 2), (6, 3, 1), (6, 4, 0), (7, 2, 1), (7, 3, 0), (8, 1, 1), (8, 2, 0), (9, 1, 0), (10, 0, 0)]

        """

        n = int(total)
        m = int(length)
        if not (is_nonneg_int(total) and is_nonneg_int(length)):
            print "Unique multisets require non-negative integers."""
            raise ValueError
        if m == 0:
            yield ()
            raise StopIteration
        if m == 1:
            yield (n,)
            raise StopIteration

        seq = []
        (quot, rem) = divmod(n, m)
        for ix in xrange(m):
            seq.append(quot + (rem > 0))
            rem -= 1
        pool = tuple(xrange(m - 1, -1, -1))
        yield tuple(seq)
        while seq[1] != 0:
            # decrement --> shift a unit leftward --> increment --> re-flow
            for i in pool:
                if seq[i] > 0:
                    seq[i] -= 1
                    j = i - 1
                    while j > 0:
                        if seq[j] < seq[j - 1]:
                            break
                        else:
                            j -= 1
                    seq[j] += 1

                    (quot, rem) = divmod(sum(seq[j + 1:]), m - (j + 1))
                    for k in xrange(j + 1, m):
                        seq[k] = quot + (rem > 0)
                        rem -= 1

                    yield tuple(seq)
                    break
        raise StopIteration

    def num_ways(self, total, length, key_len=1):
        """Yield (key, value) where value is the number of ways.

        Inputs
          :total: sum of each multiset
          :length: length of each multiset
          :key_len: number of largest multiset element(s) to use as key

        Yields
          :ways: tuple consisting of a key that identifies a group and values
                 that are the sum of each distinct ordering of
                 results, corresponding to an arrangement of a multiset,
                 computed over all arrangements of all multisets sharing
                 that key.

        Implementation
            Yields keys sharing the same lexicographic order as uniq_msets().

        """
        if key_len == 1:
            get_key = itemgetter(0)          # very fast
        else:
            get_key = lambda x: x[:key_len]
        for (key, grp) in groupby(self.uniq_msets(total, length), get_key):
            yield key, sum(self.multinomial_coeff(g) *
                           self.number_of_arrangements(g) for g in grp)

    def num_uniq_msets(self, total, length):
        """Compute number of unordered multisets with a given length and sum.

        Input
            :total: a non-negative integer sum of each multiset
            :length: length of each returned sequence

        Output
            :num_msets: number of unordered multisets

         Implementation
             The runtime of many uses of Multiset methods is proportional
             to this value. This is the number of partitions for n
             indistinguishable elements and m indistinguishable partitions,
             which has a recurrence relation of
             ``nparts(n, m) = nparts(n - 1, m - 1) + nparts(n - m, m)``

             The result is equivalent to::

                 def num_uniq_msets(n, m):
                     return sum(1 for ms in uniq_msets(n, m))

        """

        n = int(total)
        m = int(length)
        nparts = [list([0] * (m + 1)) for row in xrange(n + 1)]
        for i in xrange(n + 1):
            nparts[i][1] = 1
            for j in xrange(2, min(m, i) + 1):
                nparts[i][j] = nparts[i - 1][j - 1] + nparts[i - j][j]
        # for (ixn, r) in (nparts):
        #    print 'n=%d %s' % (ixn, r)        # pretty table of values
        return sum(nparts[n])

    def multiset_number(self, total, length):
        """Compute multiset number.

        Input
            :total: a non-negative integer sum of each multiset
            :length: number of integers in each multiset

        Output
            :num_msets: multiset number
                the total number of sequences of non-negative integers
                corresponding to a length and sum

        Explanation
            The above definition for multiset number is based on theorem 2
            in the reference below. Multiset number has a more common
            definition as the number of sequences of non-negative integers
            corresponding to a given size set of integers and a length.

         Reference
             An Introduction to Probability Theory and Its Applications, Vol 1,
             3rd Ed. by William Feller describes a very approachable
             `Stars and Bars`_ method on pages 12 and 37-39.

             .. _`Stars and Bars`: http://en.wikipedia.org/wiki/Stars_and_bars_(probability)

         Equivalent to::

             def multiset_number(n, m):
                 return sum(number_of_arrangements(ms)
                     for ms in uniq_msets(n, m))

        """

        return self.multinomial_coeff((total, length - 1))
