# Travelling Tournament Problem

Scripts to solve the [Travelling Tournament Problem](http://repository.cmu.edu/cgi/viewcontent.cgi?article=1509&context=tepper).

1. AA is [Westphal's Approximation Algorithm](https://link.springer.com/article/10.1007/s10479-012-1061-1) (AA), written in Java. It uses a Local Search method to solve the TSP and then generates the TTP schedule.
2. AA + LKH is the same AA, but written in Python. It uses the solver LKH to solve the TSP and then generates the TTP schedule.
3. SA is the Simulated Annealing (SA) approach proposed by [Anagnostopoulos](http://aris.me/pubs/ttp.pdf), implemented in Python.
4. AA + SA combines the SA approach with the AA.

Benchmark datasets are available [here](http://mat.tepper.cmu.edu/TOURN/).
