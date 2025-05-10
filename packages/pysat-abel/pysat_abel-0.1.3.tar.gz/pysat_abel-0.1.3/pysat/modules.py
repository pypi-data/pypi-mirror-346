import warnings
import abel

import numpy as np

from scipy.interpolate import CubicSpline, interp1d, RectBivariateSpline, RegularGridInterpolator
from scipy.integrate import quad, IntegrationWarning, simpson
from scipy.optimize import minimize

from joblib import Parallel, delayed
import psutil

from tqdm import tqdm

n_jobs = psutil.cpu_count(logical=False)
FASTER = True
N_INTEG = 40

def create_knots(R, nknots, power=1):
    """
    Creates a sequence of knots for cubic spline interpolation, with an option to skew the distribution.

    Parameters:
    - R (float): The ending radial position.
    - nknots (int): The number of knots to be created between R0 and R.
    - power (float, optional): A factor to skew the distribution of the knots. A power > 1 skews the knots towards the ending position R, and a power < 1 skews them towards the starting position R0. Default is 1, which results in uniformly spaced knots.

    Returns:
    - array-like: A sequence of knot positions between R0 and R.
    """

    # Generate uniformly spaced points between 0 and 1.
    uniform_points = np.linspace(0, 1, nknots)

    # Skew the uniform points using the given power.
    skewed_points = np.power(uniform_points, power)

    # Scale and translate the skewed points to lie between R0 and R.
    return R * skewed_points


def PreCalculateF(kappa, theta, Np, Npy = 200, n_integ = N_INTEG):

    R   = Np // 2
    xj  = np.linspace(-R, R, Np)
    yi  = np.linspace(-R, R, Npy)

    if FASTER:
        X, Y = np.meshgrid(xj, yi)
        r = np.sqrt(X**2 + Y**2)

        # up_to_detector
        u = np.linspace(0, np.sqrt(r**2 - X**2), n_integ, axis=-1)
        a = kappa(np.sqrt(u**2 + X[..., np.newaxis]**2))
        
        A = np.trapz(a, x=u)
        A[Y<0] = 0.
        
        u = np.linspace(np.sqrt(r**2 - X**2),np.sqrt(R**2 - X**2) , n_integ, axis=-1)
        b = kappa(np.sqrt(u**2 + X[..., np.newaxis]**2))
        
        B = np.trapz(b, x=u)
        
        FS = 2*A+B
        
        # from_incoming_light
        rmin = np.cos(theta) * (X + Y * np.tan(theta))
        alpha = - 1 / np.tan(theta)
        beta  = X / np.tan(theta) + Y
        
        a       = 1 + alpha**2
        b       = 2 * alpha * beta
        c       = beta**2 - R**2
        Delta   = b**2 - 4 * a * c
        Delta_  = np.clip(Delta, 0, None)
        
        xleft = (-b - np.sqrt(Delta_))/2/a
        
        xmin = np.cos(theta) * rmin
        xright = np.where(rmin > 0, X, xmin)
        u = np.linspace(xleft, xright, n_integ, axis=-1)
        a = kappa((u**2 + (alpha * u + beta[..., np.newaxis])**2)**0.5)* np.sqrt(1 + 1 / np.tan(theta)**2)
        A = np.trapz(a, x=u)

        A[rmin <= 0] = 0
        FI = A

        xright = np.where(rmin < 0, X, xmin)
        u = np.linspace(xleft, xright, n_integ, axis=-1)
        a = kappa((u**2 + (alpha * u + beta[..., np.newaxis])**2)**0.5)* np.sqrt(1 + 1 / np.tan(theta)**2)
        A = np.trapz(a, x=u)

        A[rmin > 0] = 0
        FI += A

        FI[Delta<0] = 0.

    else:    

        def up_to_detector(x, y):
            r   = np.sqrt(x**2 + y**2)
            integrand   = lambda u: kappa(np.sqrt(u**2 + x**2))
            if y >= 0:
                return 2*quad(integrand, 0, np.sqrt(r**2 - x**2))[0] + quad(integrand, np.sqrt(r**2 - x**2), np.sqrt(R**2 - x**2))[0]
            else:
                return quad(integrand, np.sqrt(r**2 - x**2), np.sqrt(R**2 - x**2))[0]
        

        def from_incoming_light(x, y):
            rmin = np.cos(theta) * (x + y * np.tan(theta))
            alpha = - 1 / np.tan(theta)
            beta  = x / np.tan(theta) + y
            
            a       = 1 + alpha**2
            b       = 2 * alpha * beta
            c       = beta**2 - R**2
            Delta   = b**2 - 4 * a * c

            integrand = lambda w: kappa((w**2 + (alpha * w + beta)**2)**0.5)* np.sqrt(1 + 1 / np.tan(theta)**2)

            if Delta >= 0:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", IntegrationWarning)
                    xleft   = (-b - np.sqrt(Delta))/2/a
                    if rmin >= 0:
                        xmin = np.cos(theta) * rmin
                        return quad(integrand, xleft, xmin)[0] + quad(integrand, xmin, x)[0]
                    else:
                        return quad(integrand, xleft, x)[0]
            else:
                return 0
        
        def calculate_values(j):
            FS_col = np.zeros(len(yi))
            FI_col = np.zeros(len(yi))
            for i in range(len(yi)):
                FS_col[i] = up_to_detector(xj[j], yi[i])
                FI_col[i] = from_incoming_light(xj[j], yi[i])
            return FS_col, FI_col


        results = Parallel(n_jobs=n_jobs)(delayed(calculate_values)(j) for j in range(len(xj)))

        FS = np.array([res[0] for res in results]).T
        FI = np.array([res[1] for res in results]).T
    FS = np.clip(FS, 0, 1)
    FI = np.clip(FI, 0, 1)
    
    return np.exp(-FS) * np.exp(-FI), np.exp(-FS), np.exp(-FI)


def forward_abel_transform(kappa, Np, F=None, n_integ=N_INTEG):
    R = Np // 2
    x = np.linspace(-R, R, Np)                   # shape (Np,)
    u_norm = np.linspace(0, 1, n_integ)           # shape (n_integ,)
    u_max = np.sqrt(R**2 - x**2)                  # shape (Np,)

    # Build the full physical-u grid U[i,j] = u_norm[j]*u_max[i]
    U = u_norm[None, :] * u_max[:, None]          # shape (Np, n_integ)
    RU = np.sqrt(x[:, None]**2 + U**2)            # shape (Np, n_integ)
    K = kappa(RU)                                 # shape (Np, n_integ)

    if F is None:
        # EXACTLY the same integral as before:
        #   P(x) = 2 * ∫₀^{u_max(x)} K(x,u) du
        return 2 * np.trapz(K, x=U, axis=1)       # trapz uses each row’s U[i,:] grid
    else:
        # …same RegularGridInterpolator‐based version as before…
        y = np.linspace(-R, R, F.shape[0])
        F_filled = np.nan_to_num(F, nan=0.0).T
        interp = RegularGridInterpolator((x, y), F_filled,
                                         bounds_error=False, fill_value=0.0)

        pts_pos = np.stack((np.broadcast_to(x[:, None], K.shape), U), axis=-1)
        pts_neg = np.stack((pts_pos[..., 0], -pts_pos[..., 1]), axis=-1)

        Fpos = interp(pts_pos.reshape(-1, 2)).reshape(K.shape)
        Fneg = interp(pts_neg.reshape(-1, 2)).reshape(K.shape)

        return np.trapz(K * (Fpos + Fneg), x=U, axis=1)


def objective(params, S_exp, r_SAT, F, lambda_):
    """
    Objective function that calculates the root mean squared error between modeled and experimental data.

    Parameters:
    - params:
    - S_exp:
    - r_SAT:
    - F:
    - lambda_:

    Returns:
    - float:
    """

    *f_vals, alpha = params
    F       = F**alpha if F is not None else F

    f_vals = np.asarray(f_vals + [0])
    
    Np  = len(S_exp)
    R   = Np // 2

    kappa = CubicSpline(r_SAT, f_vals, bc_type = 'clamped')

    S_mod = forward_abel_transform(kappa, Np, F)
    # Compute the second derivative of the cubic spline
    kappa_double_prime = kappa.derivative(nu=2)

    # Compute the penalty term by integrating the squared second derivative over r_vals
    r_eval = np.linspace(r_SAT[0], r_SAT[-1], num=100)
    kappa_double_prime = kappa(r_eval, nu=2)
    penalty = simpson(kappa_double_prime ** 2, x = r_eval)

    error      = np.sum((S_mod - S_exp)**2) / np.sum(S_exp**2)

    return error + lambda_ * penalty
    
def OP(Sext, alpha = None, kappa = None):
    N   = len(Sext)
    A   = np.zeros((N, N))

    J, K = np.indices((N, N)) + 1

    mask        = J > K
    A[mask]     = 0

    mask        = J == K
    A[mask]   = np.sqrt(J[mask]**2 - (J[mask] - 0.5)**2)

    mask        = J < K
    A[mask]    = np.sqrt(K[mask]**2 - (J[mask] - 0.5)**2) - np.sqrt((K[mask] - 1)**2 - (J[mask] - 0.5)**2)

    if alpha is None:
        return np.linalg.solve(A, Sext / 2)
    else:
        L = np.zeros((N - 1, N))
        np.fill_diagonal(L, 1)
        np.fill_diagonal(L[:, 1:], -1)

        if kappa is None:
            return np.linalg.solve(A.T@A + alpha*A@L.T@L, A.T@Sext/2)
        else:
            C   = np.zeros((N , N))
            J, K = np.indices((N, N)) + 1

            sum_terms = np.array([[np.sum(A[j, k+1:] * kappa[k+1:]) for k in range(N)] for j in range(N)])
            sum_terms_2 = np.array([[np.sum(A[j, :k] * kappa[:k]) for k in range(N)] for j in range(N)])

            mask_j_eq_k = J == K
            mask_j_lt_k = J < K
            mask_k_lt_N = K < N

            # Case 2: j = k < N
            C[mask_j_eq_k & mask_k_lt_N] = A[mask_j_eq_k & mask_k_lt_N] * np.exp(-sum_terms[mask_j_eq_k & mask_k_lt_N]) * (1 + np.exp(-A[mask_j_eq_k & mask_k_lt_N] * kappa[K[mask_j_eq_k & mask_k_lt_N] - 1]))

            # Case 3: j < k < N
            C[mask_j_lt_k & mask_k_lt_N] = A[mask_j_lt_k & mask_k_lt_N] * np.exp(-sum_terms[mask_j_lt_k & mask_k_lt_N]) * (1 + np.exp(-2 * sum_terms_2[mask_j_lt_k & mask_k_lt_N] - A[mask_j_lt_k & mask_k_lt_N] * kappa[K[mask_j_lt_k & mask_k_lt_N] - 1]))

            # Case 4: j < k = N
            C[mask_j_lt_k & ~mask_k_lt_N] = A[mask_j_lt_k & ~mask_k_lt_N] * (1 + np.exp(-2 * sum_terms_2[mask_j_lt_k & ~mask_k_lt_N] - A[mask_j_lt_k & ~mask_k_lt_N] * kappa[K[mask_j_lt_k & ~mask_k_lt_N] - 1]))

            # Case 5: j = k = N
            C[mask_j_eq_k & ~mask_k_lt_N] = A[mask_j_eq_k & ~mask_k_lt_N] * (1 + np.exp(-A[mask_j_eq_k & ~mask_k_lt_N] * kappa[K[mask_j_eq_k & ~mask_k_lt_N] - 1]))

            A_array = C.T@C + alpha*C@L.T@L
            b_array = C.T@Sext

            x_array = np.linalg.solve(A_array, b_array)
            return x_array, np.linalg.inv(C.T) @ A_array @ x_array

def get_optimized_spline(S_exp, F=None, nknots=7, power=0.5, lambda_=1e3, bounds=None, initial_alpha=1.00, Kext = None):
    """
    Optimizes and returns a cubic spline based on the provided experimental signal.

    Parameters:
    - S_exp (array): The experimental signal data to fit.
    - F (array, optional): An optional trapping array.
    - nknots (int): Number of knots to use in the spline. Default is 7.
    - power (float): Power parameter for knot creation. Default is 0.5.
    - lambda_ (float): Regularization parameter for the optimization. Default is 1e3.
    - bounds (list of tuples, optional): Bounds for the spline parameters.
    - initial_alpha (float): Initial alpha value for extinction uncertainty. Default is 1.00.

    Returns:
    - CubicSpline object: The optimized cubic spline.
    - float: The optimized alpha value.
    - array: The optimized parameters except alpha.
    """
    S_ref = max(S_exp);
    S_exp = S_exp / S_ref;

    Np  = len(S_exp)
    R   = Np // 2
    x   = np.linspace(-R, R, Np)
    
    if Kext is None:
        # Initial guess for inverse transform
        initial_guess = abel.daun.daun_transform(S_exp[x >= 0], direction='inverse', reg=('diff', lambda_/100), verbose = False)
    else:
        initial_guess = OP(S_exp[x>=0], alpha = lambda_/100, kappa = Kext)[0]
    
    # Create knots for spline
    knots = create_knots(R, nknots, power)
    
    if bounds is None:
        initial_spline = interp1d(np.linspace(0, R, len(initial_guess)), initial_guess, bounds_error=False, fill_value=0)
        spline_params = initial_spline(knots[:-1])  # Excluding the value at midpoint
        spline_params[spline_params < 0] = 0

        optimization_params = np.concatenate([spline_params, [initial_alpha]])
        bounds = [(0, None) for _ in spline_params] + [(1.00, 1.00)]
    else:
        spline_params = np.array([b for _, b in bounds])
        optimization_params = np.concatenate([spline_params, [initial_alpha]])
        bounds = bounds + [(1.00, 1.00)]

    # for i in range(1):
    #     objective(optimization_params,S_exp, knots, F, lambda_)
    # return
    # Optimization process
    optimization_result = minimize(objective, optimization_params, args=(S_exp, knots, F, lambda_), bounds=bounds, method='L-BFGS-B')
    optimization_result.x = optimization_result.x * S_ref
    return CubicSpline(knots, np.hstack([optimization_result.x[:-1], 0]), bc_type=((1, 0), (1, 0))), optimization_result.x[-1], optimization_result.x[:-1]

def sat(
    Sexp,
    Nknots=20,
    lambda_=1e2,
    power=0.5,
    parallel=False,
    N=None,
    center=None,
    calculate_F=False,
    Npy=100,
    res=1,
    Kext=None,
    njobs=-1
):
    """
    Performs Abel inversion on experimental data (Sexp) using optional parallel processing.

    Parameters:
        Sexp (np.ndarray): The experimental data to be adjusted. Can be either 1D or 2D array.
        Nknots (int, optional): The number of knots to use for the spline fitting. Defaults to 20.
        lambda_ (float, optional): Regularization parameter for the spline fitting. Defaults to 1e2.
        power (float, optional): Knots distribution. Defaults to 0.5 (more knots in the outer region).
        parallel (bool, optional): Whether to process the data in parallel. Defaults to False.
        N (int, optional): The number of points to consider from the center of the data. If None, uses the full width.
        center (int, optional): The center point of the data for adjustment. If None, it is set to half of the data width.
        calculate_F (bool, optional): If True, the trapping factor is calculated.
        Npy (int, optional): Number of points for the calculation of trapping factor.
        res (float, optional): Resolution in px/mm or px/m. Defaults to 1.
        trapping (np.ndarray, optional): Array for trapping correction. If None, no trapping correction is applied.
        njobs (int, optional): Number of jobs for parallel processing. Defaults to -1.

    Returns:
        np.ndarray or tuple: If `calculate_F` is False, returns the adjusted data array `K`.
                             If `calculate_F` is True, returns a tuple `(K, F_array)`.

    Notes:
        - The spline adjustment is performed using the `get_optimized_spline` function.
        - When `parallel` is set to True, parallel computing is used to speed up the process.
        - The `N` and `center` parameters allow focusing the adjustment on a specific segment of each data set.
    """
    # Ensure Sexp is a 2D array
    Sexp = np.atleast_2d(Sexp)
    num_rows, total_points = Sexp.shape

    # Set default values for N and center
    if N is None:
        N = total_points
    if center is None:
        center = total_points // 2

    # Slice Sexp to focus on the specified segment
    half_N = N // 2
    start_idx = center - half_N
    end_idx = center + half_N
    Sexp = Sexp[:, start_idx:end_idx]

    # Initialize output arrays
    K = np.zeros((num_rows, half_N))
    F_array = np.zeros((num_rows, Npy, N)) if calculate_F else None

    # Define a helper function for processing each row
    def process_single_row(index):
        S_row = Sexp[index, :]
        Kext_row = Kext[index] if Kext is not None else None

        # Obtain the optimized spline
        if Kext_row is None:
            fK, _, _ = get_optimized_spline(
                S_row,
                nknots=Nknots,
                lambda_=lambda_,
                power=power
            )
        else:
            fKext_row = CubicSpline(np.linspace(0, half_N, half_N), Kext_row)
            F_values = PreCalculateF(fKext_row, np.pi / 4, N, Npy=Npy)[1]
            fK, _, _ = get_optimized_spline(
                S_row,
                nknots=Nknots,
                lambda_=lambda_,
                power=power,
                Kext=Kext_row,
                F   = F_values,
            )

        # Compute K values
        K_values = fK(np.linspace(0, half_N, half_N))

        # Compute F values if required
        F_values = None
        if calculate_F:
            F_values = PreCalculateF(fK, np.pi / 4, N, Npy=Npy)[1]

        return K_values, F_values

    # Process the data
    if parallel:
        # Prepare arguments for parallel processing
        indices = range(num_rows)
        results = Parallel(n_jobs=njobs)(
            delayed(process_single_row)(i) for i in tqdm(indices)
        )

        # Extract results
        for i, (K_values, F_values) in enumerate(results):
            K[i] = K_values
            if calculate_F:
                F_array[i] = F_values
    else:
        # Sequential processing
        for i in tqdm(range(num_rows)):
            K_values, F_values = process_single_row(i)
            K[i] = K_values
            if calculate_F:
                F_array[i] = F_values

    # Apply resolution scaling and ensure non-negative values
    K = np.clip(K * res, a_min=0, a_max=None)

    if calculate_F:
        return K, F_array
    else:
        return K


def abel_inversion(data: np.ndarray,
                   data_type: str = 'transmissivity',
                   nknots: int = 15,
                   power: float = 0.5,
                   lambda_: float = 1e6,
                   theta: float = np.pi/4,
                   Npy: int = 50,
                   apply_correction: bool = False,
                   kext: np.ndarray = None) -> tuple[np.ndarray, np.ndarray]:
    """
    Generic Abel inversion using the Abel–Spline Transform (SAT) for
    transmissivity, emission, or scattering data, with optional trapping correction
    based on an extinction coefficient profile.

    For data without trapping correction (apply_correction=False),
    the inversion reduces to a classical SAT inversion identical to the transmissivity case.

    Parameters
    ----------
    data : np.ndarray
        1D array containing the measured signal
        (transmissivity, emission, or scattering).
    data_type : str
        One of 'transmissivity', 'emission', or 'scattering'.
    nknots : int
        Number of spline knots (default: 15).
    power : float
        Spline power exponent (default: 0.5).
    lambda_ : float
        Regularization parameter (default: 1e6).
    theta : float
        Scattering/emission angle (radians) for trapping correction (default: π/4).
        Only used when apply_correction=True.
    Npy : int
        Number of y-points for PreCalculateF (default: 50).
    apply_correction : bool
        If True, applies trapping correction for emission/scattering data.
    kext : np.ndarray, optional
        Radial extinction coefficient array for correction.
        Required if apply_correction=True.

    Returns
    -------
    r : np.ndarray
        Radial axis (0 to half signal length).
    coef : np.ndarray
        Recovered radial coefficient (extinction, emission, or scattering).

    Raises
    ------
    ValueError
        If correction is requested without providing kext.

    Examples
    --------
    # Classical inversion (no trapping correction), same for any data type:
    r, coef = abel_inversion(Synthetic_Tau)
    r, coef = abel_inversion(Synthetic_SEmi, data_type='emission')

    # Emission with trapping correction:
    r, Jem = abel_inversion(Synthetic_SEmi,
                            data_type='emission',
                            apply_correction=True,
                            kext=kext_profile)

    # Scattering with trapping correction:
    r, ksca = abel_inversion(Synthetic_SSca,
                              data_type='scattering',
                              apply_correction=True,
                              kext=kext_profile)
    """
    # ensure 1D input
    arr = data.squeeze()
    N = arr.size

    # simple inversion when no trapping correction is applied
    if not apply_correction:
        sat, _, _ = get_optimized_spline(
            arr,
            nknots=nknots,
            power=power,
            lambda_=lambda_
        )
        r = np.linspace(0, N // 2, N // 2)
        return r, sat(r)

    # trapping correction for emission/scattering
    if data_type in ('emission', 'scattering') and apply_correction:
        if kext is None:
            raise ValueError("kext profile is required for emission/scattering correction.")
        # compute correction matrices using provided extinction
        F, Fs, _ = PreCalculateF(kext, theta=theta, Np=kext.size, Npy=Npy)
        F_corr = Fs if data_type == 'emission' else F
        # invert measured data with correction
        sat_corr, _, _ = get_optimized_spline(
            arr,
            nknots=nknots,
            power=power,
            lambda_=lambda_,
            F=F_corr
        )
        r = np.linspace(0, N // 2, N // 2)
        return r, sat_corr(r)

    # fallback to simple inversion
    sat, _, _ = get_optimized_spline(
        arr,
        nknots=nknots,
        power=power,
        lambda_=lambda_
    )
    r = np.linspace(0, N // 2, N // 2)
    return r, sat(r)