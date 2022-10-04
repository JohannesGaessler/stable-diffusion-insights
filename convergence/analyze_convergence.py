#!/usr/bin/env python3

import os
import numpy as np
import matplotlib.pyplot as plt
import imageio as iio
from kafe2 import XYFit, Plot

SAMPLE_DIR = "data"
SAMPLERS = [
    "Euler", "Heun", "DPM2", "LMS",
    #"DDIM", "PLMS"  # bad fit results
]
STEPS = [
    np.array([10, 14, 20, 28, 40, 56, 80, 112, 160, 226, 1000]),
    np.array([5,  7,  10, 14, 20, 28, 40, 56,  80,  113,  500]),
    np.array([5,  7,  10, 14, 20, 28, 40, 56,  80,  113,  500]),
    np.array([10, 14, 20, 28, 40, 56, 80, 112, 160, 226, 1000]),
    np.array([10, 15, 20, 29, 40, 59, 84, 125, 167, 250,  500]),
    np.array([10, 15, 20, 29, 40, 59, 84, 125, 167, 250,  500]),
]
EFFECTIVE_STEP_LENGTHS = [1.0, 162/80, 156/80, 79/80, 78/80, 78/80]
DATA_LIMIT = -1

means = []
y_data = []
y_cov_mats = []
y_err_cor = []

for sampler, steps in zip(SAMPLERS, STEPS):
    means_sampler = []
    for i, num_steps in enumerate(steps):
        prompt_dir = os.path.join(SAMPLE_DIR, f"{sampler}-{num_steps:05d}")
        means_i = []
        file_list = sorted(os.listdir(prompt_dir))

        for j, filename in enumerate(file_list):
            if j == DATA_LIMIT:
                break
            if not filename.endswith(".png"):
                continue
            image = iio.v3.imread(os.path.join(prompt_dir, filename))
            red = np.mean(image[:, :, 0])
            means_i.append(red)

        means_i = np.array(means_i)
        means_sampler.append(means_i)

    means_sampler = np.array(means_sampler)
    means.append(means_sampler)
    diffs = np.abs(means_sampler[:-1] - means_sampler[-1])
    y_data.append(np.mean(diffs, axis=1))
    y_cov_mats.append(np.cov(diffs) / diffs.shape[1])
    y_err_cor.append(np.std(means_sampler[-1]) / np.sqrt(means_sampler[-1].shape[0]))


def poly_model(x, a, b, index):
    return a * (x ** b - (STEPS[index][-1] * EFFECTIVE_STEP_LENGTHS[index]) ** b)


def model_euler(x, a=1.0, b=-1.0):
    return poly_model(x, a, b, 0)


def model_heun(x, a=1.0, b=-1.0):
    return poly_model(x, a, b, 1)


def model_dpm2(x, a=1.0, b=-1.0):
    return poly_model(x, a, b, 2)


def model_lms(x, a=1.0, b=-1.0):
    return poly_model(x, a, b, 3)


def model_ddim(x, a=1.0, b=-1.0):
    return poly_model(x, a, b, 4)


def model_plms(x, a=1.0, b=-1.0):
    return poly_model(x, a, b, 5)


fits = []
models = [model_euler, model_heun, model_dpm2, model_lms, model_ddim, model_plms]

for i, sampler_i in enumerate(SAMPLERS):
    x_data = EFFECTIVE_STEP_LENGTHS[i] * (STEPS[i][:-1])
    fit = XYFit([x_data, y_data[i]], model_function=models[i])
    fit.add_matrix_error("y", y_cov_mats[i], "cov")
    fit.add_error("y", y_err_cor[i], correlation=1.0)

    fit.limit_parameter("a", 1, 1e4)
    fit.limit_parameter("b", -3, 0)

    fit.data_container.label = sampler_i
    fit.assign_model_function_latex_expression(r"{a} {x}^{b}")

    fit.do_fit()
    fit.report(asymmetric_parameter_errors=True)
    fits.append(fit)

for sampler, fit in zip(SAMPLERS, fits):
    print()
    print(f"========== {sampler} ==========")
    for par_val, (par_err_down, par_err_up) in zip(
            fit.parameter_values, fit.asymmetric_parameter_errors):
        print(f"{par_val:.3E} - {par_err_down:.3E} + {par_err_up:.3E}")
    print(fit.goodness_of_fit)
    print(fit.chi2_probability)

plot = Plot(fits)
plot.x_label = "Effective num steps (Euler)"
plot.y_label = "Mean red pixel value diff"
plot.x_scale = "log"
plot.y_scale = "log"
plot.x_range = (8, 260)
plot.customize("data", "markersize", 8)
plot.plot(fit_info=False, asymmetric_parameter_errors=True)
plot.save("convergence.png", dpi=240)


def diff_euler_lms(x, a_1, b_1, a_2, b_2):
    return model_euler(x, a_1, b_1) - model_lms(x, a_2, b_2)


plt.figure()
x_min = 10
x_max = 100
x_plot = np.linspace(start=x_min, stop=x_max, num=181)
y_plot = diff_euler_lms(x_plot, *fits[0].parameter_values, *fits[1].parameter_values)
plt.plot(x_plot, y_plot)
plt.xlim(x_min, x_max)
plt.xlabel("Effective num steps (Euler)")
plt.ylabel("Mean red pixel value diff")
plt.show()
