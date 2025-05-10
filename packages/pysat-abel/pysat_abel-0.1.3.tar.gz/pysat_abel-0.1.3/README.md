# pySAT - Python Implementation for Spline-based Abel Transform

## Context
In combustion research, optical diagnostics often necessitate Abel inversion to deconvolve the measurements of axisymmetric flames, especially to determine local soot temperature fields from integrated flame radiative emission measurements. However, traditional Abel inversion methods can considerably amplify experimental noise, especially towards the flame centerline. Although various strategies exist to mitigate this issue, they typically do not address the correction of signal trapping within the flame. In this context, pySAT is developed as an alternative without noise amplification, capable of correcting the signal trapping effect in different flame configurations.

## Theoretical description

<!-- <img src="https://gitlab.coria-cfd.fr/littinm/pysat/-/raw/main/img/3D_Abel_Ethylene_v3.png" width="33%"/> -->

![](https://gitlab.coria-cfd.fr/littinm/pysat/-/raw/main/img/3D_Abel_Ethylene_v3.png)


The Abel integral equation is mathematically formulated as follows:
$$
S(x) = 2 \int_{x}^{\infty} \frac{\kappa(r) F(x, r)}{\sqrt{r^{2} - x^{2}}}~r dr.
$$
The line-of-sight integrated signal $S(x)$ is known and the task is the determination of the deconvoluted $\kappa(r)$. Here, $\kappa(r)$ is assumed as a cubic spline. A cubic spline is a function that is defined by $N-1$ cubic polynomials $\kappa_{i}(r)$. Knots must to me defined and may be irregularly distributed.

Due to the continuous and differentiable nature of $S(x)$, clamped condition is imposed by setting null-derivative at the endpoints, and a null value at the end of the domain. Also, as it is not possible to obtain negative reconstructions from the projected values, a non-negativity constraint is imposed at the knots.

The direct Abel transform of this spline based profile leads to a model signal $S_{mod}$. Being a cubic spline, the values of the knots $\kappa_{i}$ are determined through the following minimization problem:

$$
    \arg\min_{\kappa}
    \left[ \int \left[S_{\text{mod}}(x, \kappa_{1}, \dots, \kappa_{N}) - S_{exp}(x) \right]^{2}
    + \mu \int_{0}^{R}\kappa^{\prime \prime}(r)^{2}~dr\right]
$$

### Line-of-sight attenuation (LOSA)

In LOSA measurements, the transmissivity $S(x) = -\ln{\tau(x)}$ is measured to retrieve the extinction coefficient $\kappa(r) = \kappa_{ext}(r)$.

$$
\tau(x) = \frac{I(x)}{I_{0}(x)} = \exp{\left(-2\int_{x}^{\infty} \frac{\kappa_{ext}(r)}{\sqrt{r^{2} - x^{2}}}~rdr\right)},
$$
where $I(x)$ and $I_{0}(x)$ is the light intensity after and before passing through the sooting medium, respectively. Because attenuation is what it is measured, self-absorption has not to be corrected ($F(x, r) = 1$).

### Soot Spectral Emission (SSE)

Emission measures line-of-sight (LoS) integrated flame emission $S_{emi}(x)$ to retrieve local thermal emission rate $J(r)$:

$$
S_{emi}(x) = \int_{x}^{\infty} \frac{J(r) F(x, r)}{\sqrt{r^{2} - x^{2}}}~rdr.
$$

#### Signal trapping model
Soot particles have the ability to scatter and absorb light, leading to the attenuation of photon intensity along the LoS from the flame to the detector. When this effect is considered, a correction factor has to be defined. This one lies on the extinction profile (retrieved from LOSA). The correction $F$ has to be computed for each position in the flame:
$$
F(x_{s}, y_{s}) = \exp{-\left(\int_{D}^{\infty} \kappa_{ext}(r)~dy\right)}
$$

## Example
The synthetic transmissivity and line-of-sight integrated emission data are located in the data_test folder emulating a measurements campaign of LOSA and SSE. In the demo.ipynb file, an application of the Spline-based Abel Transform (pySAT) is performed on the synthetic data. The steps are the following:

1. Perform the Abel inversion on the transmissivity to retrieve $\kappa_{ext}$. The result of this process can be also the signal trapping factor $F$.
2. To deconvolute the line-of-sight integrated emission, the signal trapping factor $F$ could be used or not. Since the extinction is available, then the trapping is corrected.

## Installation
### Conda
If you are more familiar with conda, it is strongly recommended to create an environment to isolate this tool from any other. Even so, the package will be installed via PIP. We are working to include it in conda-forge.

To create the environment, open a terminal and run:
```
conda create --name pysat-env
```
To activate the envinroment (now and every time you want to use pySAT):
```
conda activate pysat-env
```
To install the package:
```
pip install pysat-abel
```

### PIP
It is also recomended to use a python virtualenv for your project. Open a terminal in the folder you want to work and type:
```
python -m venv pysat-env
```
You'll have to activate it (now and every time you want to use pySAT):
```
source pysat-env/bin/activate
```
To install the package:
```
pip install pysat-abel
```
