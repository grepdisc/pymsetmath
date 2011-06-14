=====================
pymsetmath overview
=====================


Objective
----------

pymsetmath contains methods for calculations using multisets.

Usage
------
::

    >>> import pymsetmath
    >>> pymsetmath.examples.print_cumulative_prob(20, 4)

Inputs are integers. Output is printed to stdout.

Directories
------------
::

    pymsetmath/
    |-- LICENSE.txt
    |-- README.rst
    |-- setup.cfg
    |-- setup.py
    |-- pymsetmath/
    |   |-- __init__.py
    |   |-- multiset.py
    |   |-- prob_of_missing.py
    |-- tests/
    |   |-- __init__.py
    |   |-- test_pymsetmath.py

To do
-------
1. Add more to this overview
2. Add additional use case examples
3. Include support for groups of multisets which do not share a sum
4. Modify factorial to utilize memoization via a decorator
5. Annotate references including:
    * http://mathworld.wolfram.com/Partition.html
    * http://oeis.org/A008284
    * http://oeis.org/A026820
    * http://mail.python.org/pipermail/tutor/2001-August/008098.html
    * http://www.mathkb.com/Uwe/Forum.aspx/math/17470/Question-about-integer-partitions
    * http://code.activestate.com/recipes/218332/
    * http://mathworld.wolfram.com/PartitionFunctionQ.html
    * http://en.wikipedia.org/wiki/Multinomial_coefficient
    * http://en.wikipedia.org/wiki/Multiset#Counting_multisets

Future direction
------------------
While the presently solved problem uses an assumption that each worker
has an equal probability of finding a result, multiset methods
could also be used to test the validity of that assumption by
attempting to fit actual observed results by a multivariate
hypergeometric distribution.
