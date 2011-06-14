#!/usr/bin/env python
"""Functions to compute probability that a top result is missed.

    What is the probability that one or more top results are missed
    when performing a distributed search (e.g., via MapReduce)?

    These functions calculate the probability of missing one or more
    of the highest scoring (N) results, when returning an equal number
    of top results from each of several (m) worker nodes. If the results
    are assumed to be randomly distributed before partitioning to
    the workers, each worker is assumed to have an equal probability
    of returning a greater or lesser share than expected (N / m).
    
    The question can be restated, for a given confidence threshold, what
    is the optimal number of top results to return per-worker to ensure
    that zero top results are missed.

    The probability of a result being omitted is given analytically by
    ratio of the number of states for which a result (one or more) is
    omitted to the total number of possible states. While it may seem
    exceeding unlikely, it is possible that all of the top results
    for a query are found by a single worker. In that case, the only
    way to find all of the (N) results would be asking each worker
    for the full number of results (N). Fortunately, that is just
    one state, out of the full set of states, given by the number
    of workers raised to the power of the number of results (m ** N).

    For an example case of 2 workers returning the top 5 results,
    the probability of a specific case (e.g., the first worker
    returning 1 result and the second worker returning 4 results)
    is given by a multinomial distribution::
        
        P(1, 4) = (1/2) ** 5 * 5!/(1! * 4!) = 0.15625

    or slightly more generally::

        P(a, b) = (1/2) ** n * n!/(a! * b!)
        P(a, b, c) = (1/3) ** n * n!/(a! * b! * c!)
        ...

    Example use case::

        >>> print_cumulative_prob(5, 2)
        Probability of 3 or more of top 5 from one of 2 sets is 1.0000e+00.
        Probability of 4 or more of top 5 from one of 2 sets is 3.7500e-01.
        Probability of 5 or more of top 5 from one of 2 sets is 6.2500e-02.

    When returning a query of the top 5 results from 2 workers, at
    least one worker will return at least 3 results, but it is
    increasingly less likely that one worker will return 4 or even 5
    results. The former occurs on average in 3 of 8 queries and the
    latter in one of 16 queries. In the above example,
    ``P(1, 4) + P(4, 1) + P(5, 0) + P(0, 5) = 0.375``

"""

__docformat__ = 'restructuredtext'

from collections import defaultdict

from pymsetmath import Multiset, is_nonneg_int

def count_ways_to_obtain_largest_subpopulation(n, m):
    """Return dict of number of ways to obtain largest subpopulation.

    Inputs
      :n: total number (e.g., total number of highest scoring results)
      :m: number of non-negative integers to sum to n (e.g., number of
          workers)

    Output
      :ways: dictionary whose keys are the maximum value of a multiset
             and whose values are the sum of each distinct ordering of
             results, corresponding to an arrangement of a multiset,
             computed over all arrangements of all multisets sharing
             a maximum value.

    Implementation
        Although Multiset.uniq_msets() returns tuples in lexicographical
        order, this implementation would function regardless of order.

    """
    mset = Multiset(n)
    ways = defaultdict(int)
    for grp in mset.uniq_msets(n, m):
        ways[max(grp)] += (mset.multinomial_coeff(grp) *
                           mset.number_of_arrangements(grp))
    return ways

def compute_all_probabilities(n, m):
    """Compute probability that a result is missed.

    Inputs
      :n: total number (e.g., total number of highest scoring results)
      :m: number of non-negative integers to sum to n (e.g., number of
          workers, each returning an integer number of results)

    Output
      :stats: dict containing fields:
                  count is the number of results returned per worker
                  n is the total number of highest scoring results
                  m is the number of workers
                  p is the cumulative probability that a result is missed

    Notes
      The number of ways that each grouping contributes to the
      m ** n possible arrangements is (the number of distinct
      groupings corresponding to each sorted grouping) times (the
      number ways n elements from the m categories in each grouping
      can be arranged). The sum over all of these products is m ** n.

    """

    numerator = m ** n
    # Decimal can be exact, but float is good enough.
    denominator = float(numerator)
    stats = {'n': n, 'm': m, 'count': 0, 'p': 0}
    ways = count_ways_to_obtain_largest_subpopulation(n, m)
    for cnt in sorted(ways.keys()):
        stats['count'] = cnt
        stats['p'] = numerator / denominator
        yield stats.copy()
        numerator -= ways[cnt]

def compute_probabilities(n, m, t=()):
    """Compute probability that a result is missed.

    Inputs
      :n: total number (e.g., total number of highest scoring results)
      :m: number of non-negative integers to sum to n (e.g., number of
          workers, each returning an integer number of results)
      :t: optional threshold to short-circuit computation
          * integer t is the maximum number of results to return per worker
          * decimal t is the minimum probability to consider (to be added)
          * t=0 returns all results, and t=1 returns only results for one result per worker

    Output
      :stats: dict containing fields:
              - count is the the number of results returned per worker
              - n is the total number of highest scoring results
              - m is the number of workers
              - p is the cumulative probability that a result is missed

    """

    if not is_nonneg_int(t):
        t = ()
    numerator = m ** n
    denominator = float(numerator)
    stats = {'n': n, 'm': m, 'count': 0, 'p': 0}
    mset = Multiset(n)
    for (cnt, ways) in mset.num_ways(n, m):
        stats['count'] = cnt
        stats['p'] = numerator / denominator
        if cnt < t:
            yield stats.copy()
        elif cnt == t:
            yield stats.copy()
            raise StopIteration
        else:
            raise StopIteration
        numerator -= ways

def print_cumulative_prob(n=1, m=1, digits=4):
    """Given a number of top results n and a number of nodes m print odds.

    Inputs
      :n: total number (e.g., total number of highest scoring results)
      :m: number of non-negative integers to sum to n (e.g., # of workers)
      :digits: number of digits after decimal to print

    Output
      print the probability of a result being omitted from returned set

    Exceptions
      raises ValueError if inputs are not non-negative integers

    """

    for param in (n, m, digits):
        if not is_nonneg_int(param):
            raise ValueError

    print_template = ('Probability of %(count_str)s or more of top %(n)d' +
        ' from one of %(m)d sets is %(p_str)s.')
    formats = {'count': '%%%dd' % len(str(n)), 'p': '%%0.%se' % str(digits)}

    for stats in compute_all_probabilities(n, m):
        stats['count_str'] = formats['count'] % stats['count']
        stats['p_str'] = formats['p'] % stats['p']
        print print_template % stats

def main():
    mset = Multiset()
    n1, m1 = 20, 4
    print """\nShort example, involving %d multisets
Printing the probability of missing 1 or more results from the top %d
results, given %d workers, as a function of the number of top results
requested per worker.""" % (mset.num_uniq_msets(total=n1, length=m1),
        n1, m1)
    print_cumulative_prob(n=n1, m=m1)

    n2, m2 = 100, 10
    num_docs = 20
    num_ms = mset.num_uniq_msets(total=n2, length=m2)
    print '\ncomputing longer example, involving %d multisets ...' % num_ms
    for stats in compute_probabilities(n=n2, m=m2, t=num_docs):
        if stats['count'] == num_docs:
            print ' '.join(['Longer example\nChance of omitting documents',
                'from top %d when returning %d documents\nfrom each of',
                '%d workers is %0.10e']) % (n2, num_docs, m2, stats['p'])

if __name__ == "__main__":
    main()
