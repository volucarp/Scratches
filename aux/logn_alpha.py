import numpy as np
from scipy.integrate import quad
from scipy.stats import norm

# Parameters
sigma = 0.16
mu = 0.07
s = 1.0
k = .38  # You can change k
eta = 38.0  # You can change eta

# Analytical solution
def analytic_integral(s, mu, sigma, k, eta):
    ln_s = np.log(s)
    A = np.exp(k * mu + 0.5 * k**2 * sigma**2)
    I1 = A * norm.cdf((ln_s - mu - k * sigma**2) / sigma)
    I2 = s**k * (1 - norm.cdf((ln_s - mu) / sigma))
    return eta * (I1 + I2)

# Numerical integration (ground truth)
def lognorm_pdf(h):
    if h <= 0:
        return 0.0
    return (1/(h * sigma * np.sqrt(2 * np.pi))) * np.exp(-(np.log(h) - mu)**2 / (2 * sigma**2))

def f(h):
    return h**k * lognorm_pdf(h)

def numerical_integral(s):
    J1, _ = quad(f, 0, s, epsabs=1e-10)
    J2, _ = quad(lognorm_pdf, s, np.inf, epsabs=1e-10)
    return eta * J1 + eta * s**k * J2

# Calculate and print
analytical = analytic_integral(s, mu, sigma, k, eta)
numerical = numerical_integral(s)

print(f"Analytical: {analytical}")
print(f"Numerical: {numerical}")
