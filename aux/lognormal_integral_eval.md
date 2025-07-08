# Lognormal Integral Formulation

## Problem

Given $p(h)$ as the log-normal distribution PDF and $\alpha(h) = \eta h^k$, compute

$$
I(s) = \int_0^s \alpha(h) p(h)\,dh + \alpha(s) \int_s^\infty p(h)\,dh
$$

where

$$
p(h) = \frac{1}{h\sigma \sqrt{2\pi}} \exp\left(-\frac{(\ln h - \mu)^2}{2\sigma^2}\right), \quad h>0
$$

and $\eta, \mu, \sigma, k$ are constants.

---

## Step 1: Substitute $\alpha(h)$ and $p(h)$

$$
I(s) = \eta \int_0^s h^k p(h)\,dh + \eta s^k \int_s^\infty p(h)\,dh
$$

---

## Step 2: Simplify and Change Variable $t = \ln h$

### First term:

$$
\int_0^s h^k p(h)\,dh = \int_0^s h^k \frac{1}{h\sigma \sqrt{2\pi}} \exp\left(-\frac{(\ln h - \mu)^2}{2\sigma^2}\right) dh = \frac{1}{\sigma\sqrt{2\pi}} \int_0^s h^{k-1} \exp\left(-\frac{(\ln h - \mu)^2}{2\sigma^2}\right) dh
$$

Let $t = \ln h$, $dh = e^t dt$, $h = e^t$:

$$
\int_0^s h^{k-1} \exp\left(-\frac{(\ln h - \mu)^2}{2\sigma^2}\right) dh = \int_{-\infty}^{\ln s} e^{kt} \exp\left(-\frac{(t-\mu)^2}{2\sigma^2}\right) dt
$$

---

### Second term:

$$
\int_s^\infty p(h) dh = \int_s^\infty \frac{1}{h\sigma \sqrt{2\pi}} \exp\left(-\frac{(\ln h - \mu)^2}{2\sigma^2}\right) dh = \frac{1}{\sigma\sqrt{2\pi}} \int_{\ln s}^{\infty} \exp\left(-\frac{(t-\mu)^2}{2\sigma^2}\right) dt
$$

---

## Step 3: Final Analytical Solution

Combine and complete the square in the exponent for the first term:

$$
I(s) = \frac{\eta}{\sigma \sqrt{2\pi}} \left[ \int_{-\infty}^{\ln s} \exp\left( k t - \frac{(t - \mu)^2}{2\sigma^2} \right) dt + s^k \int_{\ln s}^{\infty} \exp\left(-\frac{(t - \mu)^2}{2\sigma^2}\right) dt \right]
$$

The first integral can be rewritten as:

$$
\int_{-\infty}^{\ln s} \exp\left( k t - \frac{(t - \mu)^2}{2\sigma^2} \right) dt = e^{k\mu + \frac{1}{2} k^2 \sigma^2} \int_{-\infty}^{\ln s} \exp\left( -\frac{(t - \mu - k\sigma^2)^2}{2\sigma^2} \right) dt
$$

So,

$$
I(s) = \frac{\eta}{\sigma \sqrt{2\pi}} \left[ e^{k\mu + \frac{1}{2}k^2\sigma^2} \int_{-\infty}^{\ln s} \exp\left(-\frac{(t-\mu-k\sigma^2)^2}{2\sigma^2}\right) dt + s^k \int_{\ln s}^{\infty} \exp\left(-\frac{(t-\mu)^2}{2\sigma^2}\right) dt \right]
$$

These integrals are proportional to the CDF and complementary CDF of the normal distribution.

---

## Python code
See `Lognormal Integral Eval.py` for a Python implementation.

