# TrinomialTest
[![CI](https://github.com/jrudar/TrinomialTest/actions/workflows/ci.yml/badge.svg)](https://github.com/jrudar/TrinomialTest/actions/workflows/ci.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15367633.svg)](https://doi.org/10.5281/zenodo.15367633)

The trinomial test is a non-parametric statistical test for consistent differences in medians or if a difference between the number of positive or negative differences between two groups. This test focuses on the direction (positive or negative) of the differences and the number of ties.

First one determines the number of positive, negative, and tied samples using the first set of equations. Note, that these describe the two-sample case. In the one sample case, the median can be used to find the number of positives, negatives, and tied samples. The test statistic, D, is then calculated by taking the absolute value of the difference between the number of positives and negatives. The number of ties, t, and the total number of trials, N, is used to calculate the probability of a tie. Following this, the multinomial distribution can be used to determine the probability associated with D or more ties, P(D).

In this package, one is also able to set a region of practical equivalence (ROPE). This increases the number of ties by setting differences to zero if the absolute value of the difference is smaller than the ROPE. This will inflate the number of ties but can be useful if one suspects that differences between groups or between each sample and the median may be random. The default value of the ROPE is 0.

$$I_{pos}$$, $$I_{neg}$$, and $$I_{tie}$$ are indicator functions that return 1 if the input to the function is positive, negative, or zero.

**Calculation of the Number of Positive, Negative, and Tied Samples in the Two-Sample Case**:

$$n_{+} = \sum_{i=1}^{N}I_{pos}\left(x_{i} - y_{i} > 0\right)$$

$$n_{-} = \sum_{i=1}^{N}I_{neg}\left(x_{i} - y_{i} < 0\right)$$

$$t = \sum_{i=1}^{N}I_{tie}\left(x_{i} - y_{i} = 0\right)$$


**Calculation of the Number of Positive, Negative, and Tied Samples in the One-Sample Case**:

$$n_{+} = \sum_{i=1}^{N}I_{pos}\left(x_{i} - median(X) > 0\right)$$

$$n_{-} = \sum_{i=1}^{N}I_{neg}\left(x_{i} - median(X) < 0\right)$$

$$t = \sum_{i=1}^{N}I_{tie}\left(x_{i} = median(X)\right)$$


**Calculation of the Test Statistic**:

$$D = |n_{+} - n_{-}|$$


**Calculate the Probability of a Tie**:

$$p_{tie} = \frac{t}{N}$$


**Calculate the p-value**:

$$P\left(D\right) = \sum_{z=D}^N\sum_{k=0}^{\frac{N-z}{2}}\frac{N!}{(n-z-2k)!(k+z)!k!}p_{tie}^{n-z-2k}\left(\frac{1-p_{tie}}{2}\right)^{z+2k}$$


### Install
From PyPI:

```bash
pip install TrinomialTest
```

From source:

```bash
git clone https://github.com/jrudar/TrinomialTest.git
cd TrinomialTest
pip install .
# or create a virtual environment
python -m venv venv
source venv/bin/activate
pip install .
```

### Usage

```bash
import numpy as np
from TrinomialTest import TrinomialTest
X = np.asarray([1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])
Y = np.asarray([2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])
result = TrinomialTest(X, Y, alternative = "two-sided")

# p-value should be 0.0772262851453612
print(result.pvalue)
```

### Citations

Rudar, J., & Lung, O. (2025). TrinomialTest. Zenodo. https://doi.org/10.5281/zenodo.15353378

Bian, Guorui & McAleer, Michael & Wong, Wing-Keung, 2011. "A trinomial test for paired data when there are many ties," Mathematics and Computers in Simulation (MATCOM), Elsevier, vol. 81(6), pages 1153-1160.

Whitaker, D., Drew, B., & Barss, J. (2021) GridItemTools: Grid item tools. R package version 0.0.12. https://github.com/douglaswhitaker/GridItemTools

Pauli Virtanen, Ralf Gommers, Travis E. Oliphant, Matt Haberland, Tyler Reddy, David Cournapeau, Evgeni Burovski, Pearu Peterson, Warren Weckesser, Jonathan Bright, Stéfan J. van der Walt, Matthew Brett, Joshua Wilson, K. Jarrod Millman, Nikolay Mayorov, Andrew R. J. Nelson, Eric Jones, Robert Kern, Eric Larson, CJ Carey, İlhan Polat, Yu Feng, Eric W. Moore, Jake VanderPlas, Denis Laxalde, Josef Perktold, Robert Cimrman, Ian Henriksen, E.A. Quintero, Charles R Harris, Anne M. Archibald, Antônio H. Ribeiro, Fabian Pedregosa, Paul van Mulbregt, and SciPy 1.0 Contributors. (2020) SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python. Nature Methods, 17(3), 261-272. DOI: 10.1038/s41592-019-0686-2.

Harris, C.R., Millman, K.J., van der Walt, S.J. et al. Array programming with NumPy. Nature 585, 357–362 (2020). DOI: 10.1038/s41586-020-2649-2.

McKinney W, others. Data structures for statistical computing in python. In: Proceedings of the 9th Python in Science Conference. 2010. p. 51–6.

Seabold S, Perktold J. statsmodels: Econometric and statistical modeling with python. In: 9th Python in Science Conference. 2010.

