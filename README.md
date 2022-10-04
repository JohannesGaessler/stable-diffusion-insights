# stable-diffusion-insights
The files in this repository are concerned with quantifying the properties of Stable Diffusion using statistical methods.
The methodology that was used to create the plots is important for their interpretation.
Please do not repost the plots without linking this repository or providing a similarly detailed discussion of the methodology and the results.

Unfortunately the overall look and feel of an image is highly subjective and cannot be measured directly.
For this reason the average pixel color values are measured instead.
The underlying assumption is that the convergence of high-level features will behave in the same way as these low-level features.
The general methodology is as follows:
data is generated for a simple prompt that specifies color, e.g. "Flowers, red, blue".
The generation is then manipulated in a well-defined way (e.g. "Flowers, [red], blue" or a variation in steps)
for the same seed and the difference in mean RGB values across the images is calculated.
The range of RGB values shown in the plots is the 8 bit uint format that ranges from 0 to 255.

Data analysis is performed using [kafe2](https://github.com/PhiLFitters/kafe2),
a framework for likelihood-based parameter estimation using nonlinear regression.
To this end data is transformed into a format that allows for a variation of the strength of any supposed effect,
e.g. the number of square brackets on the x axis and the measured strength of the effect on the y axis.

The distribution of mean RGB values across a set of images is assumed to be normally distributed.
The covariance of the mean can then be assumed to be the covariance of the RGB value distribution divided by the number of samples per data point.
Note: neglecting the covariance/correlation between data points with the same seeds leads to a vast overestimation of the data uncertainties.

The value of $\chi^2/\mathrm{NDF}$ is considered to evaluate whether the model function significantly deviates from the data.
A value close to 1 indicates that the assumptions about the uncertainties are correct and that the model accurately describes the data.
A value much greater than 1 indicates that either uncertainties were underestimated or that the model does not accurately describe the data.

Unless noted otherwise I am using [this frontend](https://github.com/JohannesGaessler/stable-diffusion-ipython-shell) for [AUTOMATIC1111 webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) to generate the data.
The CFG scale is set to 10.

## Convergence
The files in [convergence](./convergence) analyze the convergence speed of deterministic samplers.
