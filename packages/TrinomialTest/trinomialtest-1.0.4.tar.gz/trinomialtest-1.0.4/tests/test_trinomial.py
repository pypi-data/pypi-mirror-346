from TrinomialTest import TrinomialTest, MultipleTrinomialTest, trinomial_test

import pandas as pd

import numpy as np

# Tests the transformer modules
def test_trinomial():

    X = np.asarray([0 for _ in range(14)])
    result = TrinomialTest(X, alternative = "two-sided")
    assert np.isclose(result.pvalue, 1.0, rtol = 0.000001, atol = 0.000001)

    X = np.asarray([1 for _ in range(14)])
    Y = np.asarray([1 for _ in range(14)])
    result = TrinomialTest(X, Y, alternative = "two-sided")
    assert np.isclose(result.pvalue, 1.0, rtol = 0.000001, atol = 0.000001)

    X = np.asarray([1 for _ in range(14)])
    Y = np.asarray([2 for _ in range(14)])
    result = TrinomialTest(X, Y, alternative = "two-sided")
    assert np.isclose(result.pvalue, 0.0001220703124999, rtol = 0.000001, atol = 0.000001)

    X = np.asarray([1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])
    Y = np.asarray([2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])
    result = TrinomialTest(X, Y, alternative = "two-sided")
    assert np.isclose(result.pvalue, 0.0772262851453612, rtol = 0.000001, atol = 0.000001)

    X = np.asarray([1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])
    Y = np.asarray([2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3])
    result = TrinomialTest(X, Y, alternative = "two-sided")
    assert np.isclose(result.pvalue, 0.539570280277524, rtol = 0.000001, atol = 0.000001)

    X = np.asarray([1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])
    Y = np.asarray([2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])
    result = TrinomialTest(X, Y, alternative = "less")
    assert np.isclose(result.pvalue, 0.0772262851453612*0.5, rtol = 0.000001, atol = 0.000001)

    X = np.asarray([1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])
    Y = np.asarray([2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3])
    result = TrinomialTest(X, Y, alternative = "greater")
    assert np.isclose(result.pvalue, 0.539570280277524*0.5, rtol = 0.000001, atol = 0.000001)

    result = trinomial_test(2, 3, 2, "two-sided")
    assert np.isclose(result.pvalue, 0.8269521142186875, rtol = 0.000001, atol = 0.000001)


def test_multiple_trinomial():

    X = np.asarray([[1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
         [1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
         [1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
         [1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]])

    Y = np.asarray([[2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3],
        [2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3]])

    X = X.transpose()
    Y = Y.transpose()

    result = MultipleTrinomialTest(x = X, y = Y)

    assert np.isclose(float(result["p-value"].values[0]), 0.0772262851453612, rtol = 0.000001, atol = 0.000001)
    assert np.isclose(float(result["p-value"].values[1]), 0.539570280277524, rtol = 0.000001, atol = 0.000001)
    assert np.isclose(float(result["p-value"].values[2]), 0.0772262851453612, rtol = 0.000001, atol = 0.000001)
    assert np.isclose(float(result["p-value"].values[3]), 0.539570280277524, rtol = 0.000001, atol = 0.000001)

if __name__ == "__main__":

    test_trinomial()
    test_multiple_trinomial()
