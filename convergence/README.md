## Convergence

All deterministic (non-ancestral) samplers eventually converge against
the same image as the number of steps approaches infinity.
However, the speed of this convergence is not necessarily the same.
Unfortunately the overall look and feel of an image is highly subjective and cannot be measured directly.
For this reason the average red pixel value for images generated with the prompt "Flowers, red" is measured instead.
The underlying assumption is that the convergence of high-level features will behave in the same way as this low-level feature.

The x axis for the fit is the effective number of steps, normalized to the GPU time necessary to generate images
(on an NVIDIA GTX 1070).
The model $f(x; a, b) = a x^b$ is assumed to describe the difference in mean red pixel value to the limit at infinite steps.
Naturally this difference cannot be calculated directly.
Instead this difference is approximated by generating samples at 1000 steps and calculating
the differences relative to those samples.
To adjust for the fact that the samples presumably still have not fully converged at 1000 steps the model
is adjusted like this: $f(x; a, b) = a (x^b - 1000^b)$.
The x values at which data is collected are spaced logarithmically: 10, 14, 20, 28, 40, 56, 80, 112, 160, 226.
Because the Heun and DPM 2 samplers approximately require twice as much GPU time as the other samplers the number
of steps for those samplers was cut in half.
For Euler, Heun, DPM 2 and PLMS the seeds 0-89 were used to generate data.
For DDIM and PLMS the seeds 0-59 were used to generate data.

[Convergence](./convergence.png)

| Sampler | $a$              | $b$                    | $chi^2 / \mathrm{NDF}$ | $\chi^2$ Probability |
|---------|------------------|------------------------|------------------------|----------------------|
| Euler   | 83.6 + 9.3 - 8.3 | -0.818 + 0.044 - 0.046 | 1.547                  | 0.135                |
| Heun    | 129 + 28 - 24    | -1.189 + 0.065 - 0.065 | 1.746                  | 0.083                |
| DPM 2   | 560 + 160 - 120  | -1.635 + 0.083 - 0.086 | 0.935                  | 0.486                |
| LMS     | 178 + 31 - 27    | -1.325 + 0.057 - 0.059 | 1.459                  | 0.166                |
| DDIM    | 48.9 + 6.4 - 5.5 | -0.703 + 0.053 - 0.056 | 5.538                  | $4.99 \cdot 10^{-7}$ |
| PLMS    | 83 + 68 - 33     | -1.21 + 0.19 - 0.23    | 7.086                  | $2.07 \cdot 10^{-9}$ |

In the interval of 10 to 50 effective steps LMS is the fastest k-diffusion sampler.
Asymptotically DPM 2 seems to be faster but due to the diminishing returns at large numbers of steps this will
not be noticeable to humans.
The fit results for Euler, Heun, DPM 2, and LMS are good in terms of $\chi^2 / \mathrm{NDF}$ which indicates that
the model can accurately describe the data.
The fit results for DDIM and PLMS are bad (which is why they are not shown in the plot).
Presumably this is due to technical limitations of their implementations:
it was not possible to go beyond 500 steps so the reference images relative to which the differences are calculated
may not have sufficiently converged.
