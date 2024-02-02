import scipy
import numpy as np
import matplotlib.pyplot as plt

# choose integration function to be QUADPACK quadrature
integrate = scipy.integrate.quad


def _spectral_distribution_n1(d_lambda: np.ndarray) -> np.ndarray:
    """
    Utility function that calculates `F_1`, following Eq. (2.3) in Ross (1978).
    """
    a = 1 - d_lambda
    sd = (3 / 8) * (1 + a**2)
    sd[np.abs(d_lambda) > 2] = 0
    return sd


def theta(x: np.ndarray) -> np.ndarray:
    return np.where(x > 0, 1, 0)


def _spectral_distribution(d_lambda: np.ndarray, fprev: np.ndarray) -> np.ndarray:
    """
    Utility function that does all the work integrating `F_n` from `F_{n-1}`.
    Uses the semi-analytic Eq. (2.19) in Ross (1978).

    Note: this implementation is naive and leaves _inordinate_ amounts of room
    for improvement (maybe deliberately asking for someone to do an
    Introduction to Profiling (~; (~; )
    """

    def _integrand(xi, dl: float):
        a = dl - xi - 1
        f = np.interp(xi, d_lambda, fprev)
        return f * theta(1 - np.abs(a)) * (3 / 8) * (1 + a**2)

    e_min = np.min(d_lambda)
    e_max = np.max(d_lambda)

    res = [integrate(_integrand, e_min, e_max, args=(l,))[0] for l in d_lambda]

    return np.array(res)


def spectral_distribution(d_lambda: np.ndarray, n=1) -> list[np.ndarray]:
    """
    Calculate the spectral distribution of `n` Compton scatterings using the
    modified Fokker-Planck equation of Ross (1978) in the Thompson limit.

    Takes `d_lambda`, the relative change in wavelength, as domain.

    Returns a list with the `n` spectral functions, each an `np.ndarray`.
    """

    fs = [_spectral_distribution_n1(d_lambda)]

    for _ in range(n - 1):
        fnext = _spectral_distribution(d_lambda, fs[-1])
        fs.append(fnext)

    return fs


# setup the integration domain
d_lambda = np.linspace(0, 7, 100)

# calculate n compton scatterings
fs = spectral_distribution(d_lambda, 4)

# clear anything on the current figure
plt.clf()

# loop and plot
for f in fs:
    plt.plot(d_lambda, f)

plt.show()
