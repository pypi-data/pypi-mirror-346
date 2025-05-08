import numpy as np
import pandas as pd

from typing import Union, List
from scipy.stats import multinomial

from statsmodels.stats.multitest import multipletests


class TrinomialTestResult:
    def __init__(
        self,
        statistic: float,
        n_ties: int,
        n_pos: int,
        n_neg: int,
        N: int,
        alternative: str,
        pvalue: float,
    ):
        self.statistic = statistic
        self.pvalue = pvalue
        self.alternative = alternative
        self.n_ties = n_ties
        self.n_pos = n_pos
        self.n_neg = n_neg
        self.N = N


def compute_differences(x: np.ndarray, y: Union[np.ndarray, None], rope: float):
    # User entered two arrays, difference must be computed
    if type(y) != type(None):
        # If arrays are equal, zero differences
        if np.array_equal(x, y):
            D = np.zeros(shape=(x.shape[1],), dtype=int)

        else:
            # Get number of differences
            D_vec = x - y

            D = np.where(np.abs(D_vec) > rope, D_vec, 0.0)

    else:
        if np.all(np.equal(x, x[0])):
            D = np.zeros(shape=(x.shape[1],), dtype=int)

        else:
            D = np.where(np.abs(x) > rope, x, 0.0)

    return D


def TrinomialTest(
    x: np.ndarray,
    y: Union[np.ndarray, None] = None,
    alternative: str = "two-sided",
    rope: float = 0.0,
):
    """
    The trinomial test non-parametric test which can be used to
    determine if there is a significant difference between the medians
    of two groups. This test focuses on the direction (positive or
    negative) of the differences and the number of ties.

    Details of the test can be found in:

    Bian, G., McAleer, M., Wong, W-K (2009) A trinomial test for paired
    data when there are many ties
    https://repub.eur.nl/pub/21727/EI2010-68.pdf

    Parameters
    ----------
    x : np.ndarray
        An array of floats. If only 'x' is supplied, this array must
        be the differences between two groups (eg: Group A - Group B).
    y : np.ndarray, optional
        An array of floats.
    alternative : str of either {'two-sided', 'greater', 'less'}, optional
        Indicates the alternative hypothesis. The default value is
        'two-sided'
    rope : float, optional
        The region of practical equivalence between two groups.

    Returns
    -------
    result : `TrinomialTestResult` instance
        The return value is an object with the following attributes:

        statistic : int
            The number of differences.
        pvalue : int
            The p-value of the hypothesis test.
        alternative : str
            Indicates the alternative hypothesis specified in the input
            to `binomtest`.  It will be one of ``'two-sided'``, ``'greater'``,
            or ``'less'``.
        n_ties : float
            The number of tied samples.
        n_pos : float
            The number of positive differences.
        n_neg : float
            The number of negative differences.
        N : int
            The total number of trials

    Notes
    -----
    .. versionadded:: 1.0.0

    References
    ----------
    .. [1] Bian, G., McAleer, M., Wong, W-K (2009) A trinomial test for paired
           data when there are many ties
           https://repub.eur.nl/pub/21727/EI2010-68.pdf

    .. [1] https://rdrr.io/github/douglaswhitaker/GridItemTools/src/R/TrinomialTest.R

    Examples
    --------
    >>> import numpy as np
    >>> from TrinomialTest import TrinomialTest

    >>> X = np.asarray([3, 1, 2, 0, 8, 4, 9])
    >>> Y = np.asarray([2, 3, 1, 0, 10, 4, 8])
    >>> result = TrinomialTest(X, Y, alternative = "two-sided", rope = 0.0)
    >>> result.pvalue
    0.8269521142186875

    The null hypothesis can be rejected at the 5% level of significance
    because the returned p-value is greater than the critical value of 5%.
    """

    # x - y or np.where(|x| > rope, x, 0)
    D = compute_differences(x, y, rope)

    # If the arrays are equal, p-value = 1.0
    if np.all(np.equal(x, x[0])):
        return np.asarray(1.0)

    else:
        # Calculate random variables and probabilities
        N_pos = np.where(D > 0, 1, 0).sum()
        N_neg = np.where(D < 0, 1, 0).sum()
        N_tie = np.where(D == 0, 1, 0).sum()

        N = N_pos + N_neg + N_tie

        P_tie = N_tie / N

        # Calculate test statistic, nd (abs. value because testing n+ = n-)
        nd = np.abs(N_pos - N_neg)

        nd_sign = np.sign(N_pos - N_neg)

        P_diff = 1.0 - P_tie
        P_diff = 0.5 * P_diff

        p_value = 0
        prob_same = 0

        """
        Calculate the probability mass for all areas of the trinomial distribution where Nd = z
        Bian, G., McAleer, M., Wong, W-K (2009) A trinomial test for paired data when there are many ties
        https://repub.eur.nl/pub/21727/EI2010-68.pdf
        """
        for z in range(nd, N + 1):
            for k in range(0, int((N - z) * 0.5) + 1):
                n_pos = z + k
                n_neg = k
                n_tie = N - n_pos - n_neg

                prob = multinomial.pmf(
                    [n_pos, n_neg, n_tie], N, [P_diff, P_diff, P_tie]
                )

                p_value += prob

            if z == nd:
                prob_same = p_value

        # H0: P_pos != P_neg
        if alternative == "two-sided":
            p_value_final = p_value * 2.0

            if nd == 0:
                p_value_final = p_value_final - prob_same

                # Floating point errors can occur, correct
                if p_value_final > 1.0:
                    p_value_final = np.asarray(1.0)

        # H0: P_pos < P_neg
        elif alternative == "less":
            if nd_sign < 0:
                p_value_final = p_value

            else:
                p_value_final = 1.0 - p_value + prob_same

        # H0: P_pos > P_neg
        elif alternative == "greater":
            if nd_sign < 0:
                p_value_final = 1.0 - p_value + prob_same

            else:
                p_value_final = p_value

        return TrinomialTestResult(
            statistic=nd,
            pvalue=p_value_final,
            alternative=alternative,
            n_ties=N_tie,
            n_pos=N_pos,
            n_neg=N_neg,
            N=N,
        )


def MultipleTrinomialTest(
    x: np.ndarray,
    y: Union[np.ndarray, None] = None,
    alternative: str = "two-sided",
    rope: float = 0.0,
    alpha: float = 0.05,
    correction: str = "fdr_bh",
    exp_names: Union[List[str], None] = None,
):
    """
    The trinomial test non-parametric test which can be used to
    determine if there is a significant difference between the medians
    of two groups. This test focuses on the direction (positive or
    negative) of the differences and the number of ties.

    This function will conduct multiple trinomial tests on two 2D
    arrays of the same shape.

    Parameters
    ----------
    x : np.ndarray of shame (m, n)
        An 2D array of floats with m samples and n experiments
    y : np.ndarray of shame (m, n)
        An 2D array of floats with m samples and n experiments
    alternative : str of either {'two-sided', 'greater', 'less'}, optional
        Indicates the alternative hypothesis. The default value is
        'two-sided'.
    rope : float, optional
        The region of practical equivalence between two groups.
    alpha : float
        The level of significance. The default value is 0.05
    correction: str
        The type of multiple test correction. The default value is
        'fdr_bh'.

    Returns
    -------
    result : pd.DataFrame
        A dataframe containing the summary of each experiment.
    """

    if x.shape != y.shape:
        raise ValueError("X and Y should be the same shape.")

    p_values = []
    test_statistic = []
    ties = []
    total_trials = []
    for i in range(0, x.shape[1]):
        result = TrinomialTest(x=x[:, i], y=y[:, i], alternative=alternative, rope=rope)

        test_statistic.append(result.statistic)
        ties.append(result.n_ties)
        total_trials.append(result.N)
        p_values.append(result.pvalue)

    result = multipletests(p_values, method=correction, alpha=alpha)

    if type(exp_names) == type(None):
        exp = [str(i) for i in range(x.shape[1])]

    else:
        exp = exp_names

    cols = [
        "Experiment",
        "Test Statistic",
        "N Ties",
        "N",
        "p-value",
        "adj p-value",
        "Significant",
    ]

    df = np.asarray(
        [
            exp,
            np.asarray(test_statistic),
            np.asarray(ties),
            np.asarray(total_trials),
            np.asarray(p_values),
            np.asarray(result[1]),
            np.asarray(result[0]),
        ]
    ).transpose()

    df = pd.DataFrame(df, columns=cols)

    return df


def trinomial_test(
    n_tie: int, 
    n_pos: int, 
    n_neg: int, 
    alternative: str
):
    """
    The trinomial test non-parametric test which can be used to
    determine if there is a significant difference between the medians
    of two groups. This test focuses on the direction (positive or
    negative) of the differences and the number of ties.

    This function calculates the p-value using the number of tied,
    positive, and negative samples directly.

    Details of the test can be found in:

    Bian, G., McAleer, M., Wong, W-K (2009) A trinomial test for paired
    data when there are many ties
    https://repub.eur.nl/pub/21727/EI2010-68.pdf

    Parameters
    n_tie: int
        The number of ties.
    n_pos: int
        The number of positive differences.
    n_neg: int
        The number of negative differences.
    alternative : str of either {'two-sided', 'greater', 'less'}, optional
        Indicates the alternative hypothesis. The default value is
        'two-sided'

    Returns
    -------
    result : `TrinomialTestResult` instance
        The return value is an object with the following attributes:

        statistic : int
            The number of differences.
        pvalue : int
            The p-value of the hypothesis test.
        alternative : str
            Indicates the alternative hypothesis specified in the input
            to `binomtest`.  It will be one of ``'two-sided'``, ``'greater'``,
            or ``'less'``.
        n_ties : float
            The number of tied samples.
        n_pos : float
            The number of positive differences.
        n_neg : float
            The number of negative differences.
        N : int
            The total number of trials

    Notes
    -----
    .. versionadded:: 1.0.3

    References
    ----------
    .. [1] Bian, G., McAleer, M., Wong, W-K (2009) A trinomial test for paired
           data when there are many ties
           https://repub.eur.nl/pub/21727/EI2010-68.pdf

    .. [1] https://rdrr.io/github/douglaswhitaker/GridItemTools/src/R/TrinomialTest.R

    Examples
    --------
    >>> import numpy as np
    >>> from TrinomialTest import trinomial_test
    >>> result = trinomial_test(n_tie = 2, n_pos = 3, n_neg = 2, alternative = "two-sided")
    >>> result.pvalue
    0.8269521142186875

    The null hypothesis can be rejected at the 5% level of significance
    because the returned p-value is greater than the critical value of 5%.
    """

    # Calculate random variables and probabilities
    N_pos = n_pos
    N_neg = n_neg
    N_tie = n_tie

    N = N_pos + N_neg + N_tie

    P_tie = N_tie / N

    # Calculate test statistic, nd (abs. value because testing n+ = n-)
    nd = np.abs(N_pos - N_neg)

    nd_sign = np.sign(N_pos - N_neg)

    P_diff = 1.0 - P_tie
    P_diff = 0.5 * P_diff

    p_value = 0
    prob_same = 0

    """
    Calculate the probability mass for all areas of the trinomial distribution where Nd = z
    Bian, G., McAleer, M., Wong, W-K (2009) A trinomial test for paired data when there are many ties
    https://repub.eur.nl/pub/21727/EI2010-68.pdf
    """
    for z in range(nd, N + 1):
        for k in range(0, int((N - z) * 0.5) + 1):
            n_pos = z + k
            n_neg = k
            n_tie = N - n_pos - n_neg

            prob = multinomial.pmf(
                [n_pos, n_neg, n_tie], N, [P_diff, P_diff, P_tie]
            )

            p_value += prob

        if z == nd:
            prob_same = p_value

    # H0: P_pos != P_neg
    if alternative == "two-sided":
        p_value_final = p_value * 2.0

        if nd == 0:
            p_value_final = p_value_final - prob_same

            # Floating point errors can occur, correct
            if p_value_final > 1.0:
                p_value_final = np.asarray(1.0)

    # H0: P_pos < P_neg
    elif alternative == "less":
        if nd_sign < 0:
            p_value_final = p_value

        else:
            p_value_final = 1.0 - p_value + prob_same

    # H0: P_pos > P_neg
    elif alternative == "greater":
        if nd_sign < 0:
            p_value_final = 1.0 - p_value + prob_same

        else:
            p_value_final = p_value

    return TrinomialTestResult(
        statistic=nd,
        pvalue=p_value_final,
        alternative=alternative,
        n_ties=N_tie,
        n_pos=N_pos,
        n_neg=N_neg,
        N=N,
    )