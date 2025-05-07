# TrinomialTest
[![CI](https://github.com/jrudar/TrinomialTest/actions/workflows/ci.yml/badge.svg)](https://github.com/jrudar/TrinomialTest/actions/workflows/ci.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15353378.svg)](https://doi.org/10.5281/zenodo.15353378)

The trinomial test is a non-parametric statistical test for consistent differences between paired data or medians.

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

