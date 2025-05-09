"""


Functions and methods
=====================

def windows(
        K: int,
        min_size: int = 1,
        density: int = 64
    ) -> int | np.ndarray:

def variance(
        y: np.ndarray,
        M: np.ndarray
    ) -> np.ndarray:

def ideal_variance(
        tau: np.ndarray,
        ks: tuple | list,
        T: float | None = None
    ) -> np.ndarray:

def noise_quantization(
        var: float,
        T: float,
        K: int
    ) -> np.ndarray:

def noise_white(
        var: float,
        T: float,
        K: int
    ) -> np.ndarray:

def noise_fogm(
        var: float,
        tau: float,
        T: float,
        K: int,
        y0: float | None = None
    ) -> np.ndarray:

def noise_brownian(
        var: float,
        T: float,
        K: int
    ) -> np.ndarray:

def noise_ramp(
        var: float,
        T: float,
        K: int
    ) -> np.ndarray:

class fit:
    def __init__(self,
            tau: np.ndarray,
            va: np.ndarray,
            T: float = 1.0,
            ks: tuple | list | None = None,
            ax: axes = None,
            truecolor: str = "tab:blue",
            fitcolor: str = "tab:orange"
        ) -> None:
"""

import math

from matplotlib import axes
from matplotlib.backend_bases import (
    CloseEvent, KeyEvent, MouseEvent, ResizeEvent)
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt

def windows(
        K: int,
        min_size: int = 1,
        density: int = 64
    ) -> int | np.ndarray:
    """
    Build an array of averaging window sizes for Allan variances analysis.

    Parameters
    ----------
    K : int
        Number of time samples.
    min_size : int, default 1
        The minimum window size.
    density : int, default 64
        Desired number of window sizes per decade.

    Returns
    -------
    M : integer np.ndarray
        Array of averaging window sizes (averaging period over sampling period).
        Each element of `M` will be an integer.

    Notes
    -----
    Because the elements of `M` should be unique and integers, it cannot be
    guaranteed that there will be exactly `density` sizes in each decade with a
    logarithmic spacing.
    """

    e_min = np.log10(min_size)
    e_max = np.log10(np.floor(K/2))
    cnt = round((e_max - e_min)*density)
    M_real = np.logspace(e_min, e_max, cnt)
    M = np.unique(np.round(M_real)).astype(int)
    return M


def variance(
        y: np.ndarray,
        M: np.ndarray
    ) -> np.ndarray:
    """
    Calculate the Allan variance of y with the array of averaging window sizes
    specified by M.

    Parameters
    ----------
    y : (K,) or (J, K) float np.ndarray
        Array of `K` values in time or matrix of rows of such arrays.
    M : (I,) integer np.ndarray
        Array of `I` averaging window sizes (averaging period over sampling
        period). Each element of `M` must be an integer.

    Returns
    -------
    v : (I,) float np.ndarray
        Array of `I` Allan variances.
    """

    if np.ndim(y) == 1:
        v = np.zeros(len(M))
        Y = np.cumsum(y)
        for n_tau, m in enumerate(M):
            Yc = Y[(2*m - 1):] # Ending integrals
            Yb = Y[(m - 1):(-m)] # Middle integrals
            Yj = Y[:(1 - 2*m)] # Beginning integrals
            yj = y[:(1 - 2*m)] # Beginning
            delta = (Yc - 2*Yb + Yj - yj)/m
            v[n_tau] = np.mean(delta**2)/2
    else:
        J = y.shape[0]
        v = np.zeros((J, len(M)))
        Y = np.cumsum(y, axis=1)
        for n_tau, m in enumerate(M):
            Yc = Y[:, (2*m - 1):] # Ending integrals
            Yb = Y[:, (m - 1):(-m)] # Middle integrals
            Yj = Y[:, :(1 - 2*m)] # Beginning integrals
            yj = y[:, :(1 - 2*m)] # Beginning
            delta = (Yc - 2*Yb + Yj - yj)/m
            v[:, n_tau] = np.mean(delta**2, axis=1)/2

    return v


def ideal_variance(
        tau: np.ndarray,
        ks: tuple | list,
        T: float | None = None
    ) -> np.ndarray:
    """
    Calculate the ideal Allan variance curve for quantization, white,
    first-order Gauss-Markov (FOGM), Brownian, or ramp noises.

    Parameters
    ----------
    tau : (I,) np.ndarray
        Array of averaging periods (s).
    ks : tuple or list
        A tuple or list or tuple or list of tuples or lists of ideal noise
        parameters. Each inner iterable is composed of the decade-per-decade
        slope of the Allan variance and the variance. In the case of FOGM noise,
        the tuple has a third element for the time constant and its slope is 0.
    T : float, default None
        Sampling period (s). This is only needed for FOGM noise. If no value is
        provided, the first value of `tau` will be used automatically.

    Returns
    -------
    va : (I,) np.ndarray
        Array of ideal Allan variance values.
    """

    # Ensure ks is a list of iterables.
    if not isinstance(ks[0], (tuple, list)):
        ks = [ks]

    # Initialize the output array.
    va = 0.0

    # Add the component Allan variances.
    for k in ks:
        # Ensure slope is an integer.
        slope = int(k[0])

        # Define the component Allan variance.
        if slope == -2:     # quantization noise
            va += k[1]*3.0/(tau*tau)
        elif slope == -1:   # white noise
            va += k[1]/tau
        elif slope ==  0:   # FOGM noise
            if T is None:
                T = tau[0]
            M = tau/T # window sample size
            q = np.exp(-T/k[2])
            va += (k[1]/M**2)*(M*(1 - q)**2 + 2*q*M*(1 - q)
                - 2*q*(1 - q**M) - q*(1 - q**M)**2)/(1 - q)**2
        elif slope ==  1:   # Brownian noise
            va += k[1]*tau/3.0
        elif slope ==  2:   # ramp noise
            va += k[1]*tau*tau/2.0

    return va


def noise_quantization(
        var: float,
        T: float,
        K: int
    ) -> np.ndarray:
    """
    Generate quantization noise as differentiated white, Gaussian noise.

    Parameters
    ----------
    var : float
        Output variance.
    T : float
        Sampling period (s).
    K : int
        Number of noise samples.

    Returns
    -------
    y : (K,) np.ndarray
        Array of noise over time.
    """

    w = np.random.randn(int(K) + 1)
    y = np.sqrt(var)*np.diff(w)/T

    return y


def noise_white(
        var: float,
        T: float,
        K: int
    ) -> np.ndarray:
    """
    Generate white noise, in terms of its random walk property when integrated.
    This distinction simply means the variance is divided by the sampling
    period.

    Parameters
    ----------
    var : float
        Output variance.
    T : float
        Sampling period (s).
    K : int
        Number of noise samples.

    Returns
    -------
    y : (K,) np.ndarray
        Array of noise over time.
    """

    w = np.random.randn(int(K))
    y = np.sqrt(var/T)*w

    return y


def noise_fogm(
        var: float,
        tau: float,
        T: float,
        K: int,
        y0: float | None = None
    ) -> np.ndarray:
    """
    Generate first-order, Gauss-Markov (FOGM) noise.

    Parameters
    ----------
    var : float
        Output variance.
    tau : float
        Time constant (s).
    T : float
        Sampling period (s).
    K : int
        Number of noise samples.
    y0 : float, default None
        Initial value of output. A value of None will result in a random value
        according to the steady-state distribution of the noise output.

    Returns
    -------
    y : (K,) np.ndarray
        Array of noise over time.

    Notes
    -----
    FOGM noise is generated in the time domain. Testing shows that FFT only
    increases the speed by 34% for one million points and only 18% for ten
    million points.

    The bias instability noise can be approximated by multiple FOGM noises in
    parallel.
    """

    # Define scaling factors.
    ka = math.exp(-T/tau)
    kb = math.sqrt(var*(1 - math.exp(-2*T/tau)))

    # Define the standard normal noise array.
    K = int(K)
    w = np.random.randn(K + 1)

    # Initialize the state.
    x = math.sqrt(var) * w[-1] if y0 is None else float(y0)

    # Process through time.
    y = np.zeros(K)
    for k in range(K):
        y[k] = x
        x = ka*x + kb*w[k]

    return y


def noise_brownian(
        var: float,
        T: float,
        K: int
    ) -> np.ndarray:
    """
    Generate Brownian (integrated white) noise.

    Parameters
    ----------
    var : float
        Output variance.
    T : float
        Sampling period (s).
    K : int
        Number of noise samples.

    Returns
    -------
    y : (K,) np.ndarray
        Array of noise over time.
    """

    w = np.random.randn(K)
    y = np.cumsum(np.sqrt(var*T)*w)

    return y


def noise_ramp(
        var: float,
        T: float,
        K: int
    ) -> np.ndarray:
    """
    Generate ramp (doubly integrated white) noise.

    Parameters
    ----------
    var : float
        Output variance.
    T : float
        Sampling period (s).
    K : int
        Number of noise samples.

    Returns
    -------
    y : (K,) np.ndarray
        Array of noise over time.

    Notes
    -----
    Doubly integrated white noise grows faster the longer the signal. Therefore,
    in order to get the Allan variance of this generated noise to match the
    expected ideal Allan variance magnitude, the amplitude of the noise signal
    is scaled according to the number of samples.

    The scaling factor for ramp noise has been empirically, not analytically,
    derived. However, given its simplicity (`sqrt(2)`) and the very small errors
    between the average Allan variance curves of 10 000 Monte-Carlo samples of
    noise and the ideal Allan variance curve, it seems correct.
    """

    eta = np.sqrt(2*var/K) * T * np.random.randn(K)
    y = np.cumsum(np.cumsum(eta))

    return y


class fit:
    """
    Display an Allan variance curve along with its fit. The fit can be
    interactively manipulated by moving, adding, or deleting its Allan variance
    components.

    Bindings
    --------
    -   Left click and drag a nearby component to move it.
    -   Shift, left click (or middle click) and drag to pan.
    -   Scroll to zoom. Hold shift to zoom faster.
    -   Hold "q", "w", "f", "b", or "r" and click to create an Allan variance
        component.
    -   Left click and hold and press "x", "delete", or "backspace" to delete an
        Allan variance component.
    -   Press "o" to optimize the magnitudes of the component variances.

    Key Attributes
    --------------
    ks : tuple or list of tuples or lists
        A list of lists, each composed of slope and variance or slope, variance,
        and a time constant. The later case is for a first-order, Gauss-Markov
        noise where the slope would be 0.
    va_fit : (I,) np.ndarray
        The fitted Allan variance curve over the range of values of `tau`.
    """

    def __init__(self,
            tau: np.ndarray,
            va: np.ndarray,
            T: float = 1.0,
            ks: tuple | list | None = None,
            ax: axes = None,
            truecolor: str = "tab:blue",
            fitcolor: str = "tab:orange"
        ) -> None:
        """
        Initialize the plot.

        Parameters
        ----------
        tau : (I,) np.ndarray
            Averaging periods (s).
        va : (I,) or (J, I) np.ndarray
            True Allan variances or matrix of J Allan variances.
        T : float, default 1.0
            Sampling period (s).
        ks : tuple or list of tuples or lists, default None
            A tuple or list of tuples or lists, each composed of slope and
            variance or slope, variance, and a time constant. The later case is
            for a first-order, Gauss-Markov noise where the slope would be 0.
        ax : axes, default None
            MatPlotLib axes object. If none is provided, one will be generated.
        truecolor : str, default "tab:blue"
            Color of the true Allan variance curve.
        fitcolor : str, default "tab:orange"
            Color of the fitted Allan variance curve.
        """

        # Save the inputs, except for ks.
        self.tau = tau
        self.va = va
        self.T = T
        self.I = len(self.tau)
        self.tp = self.va.ndim > 1 and self.va.shape[1] != self.I
        if self.tp:
            self.va = self.va.T
        self.ax = ax
        self.truecolor = truecolor
        self.fitcolor = fitcolor

        # Check if there are enough points.
        if self.I < 2:
            raise ValueError("fit: not enough data.")

        # Check and save the components list.
        self.ks = []
        self.J = 0
        if ks is not None:
            if not isinstance(ks, (tuple, list)):
                raise TypeError("fit: ks must be a tuple or list.")
            self.J = len(ks)
            if self.J == 0:
                raise ValueError("fit: ks must not be an empty tuple or list.")
            for j in range(self.J):
                k = list(ks[j])
                if len(k) < 2:
                    raise ValueError("fit: each element of ks must have "
                        "at least two values.")
                k[0] = round(k[0])
                if not (-2 <= k[0] <= 2):
                    raise ValueError("fit: the first value in any element of "
                        "ks must be a slope in the range [-2, 2].")
                if k[1] < 0:
                    raise ValueError("fit: the second value in any element of "
                        "ks must be a positive variance.")
                if k[0] == 0:
                    if len(k) < 3:
                        raise ValueError("fit: any element of ks whose first "
                            "value (slope) is zero must have three values.")
                    if k[2] < 0:
                        raise ValueError("fit: the third value in any element "
                            "of ks must be a positive time constant.")
                self.ks.append(list(k))

        # Define the component array shapes.
        self.k_shapes = np.array([
            3/(self.tau**2),    # slope -2: quantization
            1/self.tau,         # slope -1: white
            0.0*self.tau,       # FOGM noise
            self.tau/3,         # slope +1: Brownian
            (self.tau**2)/2])   # slope +2: rate ramp

        # Initialize the states.
        self.j_hi = None        # highlighted component curve
        self.shift = False      # shift key pressed
        self.new_key = None     # one of new keys pressed: q, w, f, b, r
        self.x_ratio = 1.0      # ratio of mouse's x position to component's x
        self.y_ratio = 1.0      # ratio of mouse's y position to component's y

        # Generate a plot axis object if needed.
        if self.ax is None:
            _, self.ax = plt.subplots()

        # Create the component curves.
        self.va_j = []
        self.plot_j = []
        self.va_fit = np.zeros(len(self.tau))
        for j in range(self.J):
            va = self.build_component_va(j)
            self.va_j.append(va)
            plot_obj, = self.ax.plot(self.tau, va,
                color="#CCCCCC", linewidth=0.8)
            self.plot_j.append(plot_obj)
            self.va_fit += va

        # Initialize the optimization bounds.
        self.opt_first, self.opt_last = 0, self.I - 1
        self.opt_left, self.opt_right = self.tau[0], self.tau[-1]
        self.plot_left, = self.ax.plot([], [], color="#CCCCCC", linewidth=0.8)
        self.plot_right, = self.ax.plot([], [], color="#CCCCCC", linewidth=0.8)

        # Plot and save the original Allan variance plot.
        self.plot_true, = self.ax.plot(self.tau, self.va, color=self.truecolor)

        # Create the fitted Allan variance plot.
        if self.J > 0:
            self.plot_fit, = self.ax.plot(self.tau, self.va_fit,
                color=self.fitcolor)
        else:
            self.plot_fit, = self.ax.plot([], [], color=self.fitcolor)

        # Link events to methods.
        self.canvas = self.ax.figure.canvas
        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("motion_notify_event", self.on_motion)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        self.canvas.mpl_connect("scroll_event", self.on_scroll)
        self.canvas.mpl_connect("key_press_event", self.on_key_press)
        self.canvas.mpl_connect("key_release_event", self.on_key_release)
        self.canvas.mpl_connect("resize_event", self.on_resize)
        self.canvas.mpl_connect("close_event", self.on_close)

        # Disable some default keybindings.
        plt.rcParams["keymap.back"] = ["left", "c", "MouseButton.BACK"]
        plt.rcParams["keymap.fullscreen"] = ["ctrl+f"]
        plt.rcParams["keymap.zoom"] = []
        plt.rcParams["keymap.quit"] = ["ctrl+w", "cmd+w"]

        # Set the grid.
        self.ax.grid(visible=True, color="#CCCCCC", linewidth=0.2)

        # Set the scale to log-log.
        self.ax.set_xscale("log")
        self.ax.set_yscale("log")

        # Remove x and y labels
        self.ax.set_xlabel("")
        self.ax.set_ylabel("")

        # Move tick labels inside.
        self.ax.tick_params(axis="x", direction="in", bottom=False, pad=-15)
        self.ax.tick_params(axis="y", direction="in", left=False, pad=-45)

        # Remove the box by hiding all spines.
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["left"].set_visible(False)
        self.ax.spines["bottom"].set_visible(False)

        # Set the view.
        self.fig = self.ax.figure
        self.home()

        # Remove white space around plot.
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

        # Define the optimization bounds.
        self.opt_low, self.opt_high = self.ax.get_ylim()
        self.plot_left.set_data([self.opt_left, self.opt_left],
            [self.opt_low, self.opt_high])
        self.plot_right.set_data([self.opt_right, self.opt_right],
            [self.opt_low, self.opt_high])

        # Render.
        plt.show()

    def build_component_va(self,
            j: int
        ) -> np.ndarray:
        """ Calculate the Allan variance curve for component `j`. """

        k = self.ks[j]
        if abs(k[0]) > 0: # non-zero slope
            va = k[1] * self.k_shapes[k[0] + 2]
        elif k[0] == 0: # zero slope
            M = self.tau/self.T
            q = np.exp(-self.T/k[2])
            va = (k[1]/M**2)*(M*(1 - q)**2 + 2*q*M*(1 - q)
                - 2*q*(1 - q**M) - q*(1 - q**M)**2)/(1 - q)**2
        return va

    def home(self) -> None:
        """ Set the view to the limits of the data with padding. """

        # Get the midpoint and desired span of the view.
        xmin, xmax = np.log10(self.tau.min()), np.log10(self.tau.max())
        ymin, ymax = np.log10(self.va.min()),  np.log10(self.va.max())
        xmid, ymid = (xmin + xmax)/2, (ymin + ymax)/2
        xspan, yspan = (xmax - xmin), 1.5*(ymax - ymin)

        # Set the view limits.
        xlim = 10**(xmid - 0.5*xspan), 10**(xmid + 0.5*xspan)
        ylim = 10**(ymid - 0.5*yspan), 10**(ymid + 0.5*yspan)
        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)
        self.xlim_home = self.ax.get_xlim()
        self.ylim_home = self.ax.get_ylim()

        # Move the lower and upper edges of the optimization bounds.
        self.opt_low, self.opt_high = self.ax.get_ylim()
        self.plot_left.set_data([self.opt_left, self.opt_left],
            [self.opt_low, self.opt_high])
        self.plot_right.set_data([self.opt_right, self.opt_right],
            [self.opt_low, self.opt_high])

    def resize(self) -> None:
        """ Reset the view based on the current view. """

        # Get the midpoint and desired span of the view.
        xmin, xmax = self.ax.get_xlim()
        ymin, ymax = self.ax.get_ylim()
        xmin, xmax = np.log10(xmin), np.log10(xmax)
        ymin, ymax = np.log10(ymin), np.log10(ymax)
        xmid, ymid = (xmin + xmax)/2, (ymin + ymax)/2
        xspan, yspan = (xmax - xmin), (ymax - ymin)

        # Set the view limits.
        xlim = 10**(xmid - 0.5*xspan), 10**(xmid + 0.5*xspan)
        ylim = 10**(ymid - 0.5*yspan), 10**(ymid + 0.5*yspan)
        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)
        self.xlim_home = self.ax.get_xlim()
        self.ylim_home = self.ax.get_ylim()

        # Move the lower and upper edges of the optimization bounds.
        self.opt_low, self.opt_high = self.ax.get_ylim()
        self.plot_left.set_data([self.opt_left, self.opt_left],
            [self.opt_low, self.opt_high])
        self.plot_right.set_data([self.opt_right, self.opt_right],
            [self.opt_low, self.opt_high])

    def dim_bound(self) -> None:
        """ Dim the optimization bound. """

        if self.j_hi == -1: # left bound
            self.plot_left.set_color("#CCCCCC")
        elif self.j_hi == -2: # right bound
            self.plot_right.set_color("#CCCCCC")

    def highlight_bound(self) -> None:
        """ Highlight the optimization bound. """

        if self.j_hi == -1: # left bound
            self.plot_left.set_color("#000000")
        elif self.j_hi == -2: # right bound
            self.plot_right.set_color("#000000")

    def move_bound(self,
            x: float
        ) -> None:
        """ Move the selected optimization bound. """

        # Lock onto a valid value of tau.
        X = x / self.x_ratio
        i = np.argmin(np.abs(self.tau - X))
        X = self.tau[i]

        if self.j_hi == -1: # left bound
            self.opt_first = i
            self.opt_left = X
            self.plot_left.set_data([self.opt_left, self.opt_left],
                [self.opt_low, self.opt_high])
        elif self.j_hi == -2: # right bound
            self.opt_last = i
            self.opt_right = X
            self.plot_right.set_data([self.opt_right, self.opt_right],
                [self.opt_low, self.opt_high])

    def dim_component(self) -> None:
        """ Dim the selected component curve. """

        self.plot_j[self.j_hi].set_color("#CCCCCC")

    def highlight_component(self) -> None:
        """ Highlight the selected component curve. """

        self.plot_j[self.j_hi].set_color("#000000")

    def move_component(self,
            x: float,
            y: float
        ) -> None:
        """
        Move the selected component curve, changing its parameters, its Allan
        variance array, and its plot.
        """

        # Get the position relative to the offset.
        X = x / self.x_ratio
        Y = y / self.y_ratio

        # Set the component curve variance (and tau) using the given (X, Y).
        j = self.j_hi
        k = self.ks[j]
        if k[0] == -2:      # quantization noise
            k[1] = float(Y * X**2/3)
        elif k[0] == -1:    # white noise
            k[1] = float(Y * X)
        elif k[0] == 0:     # FOGM noise
            k[1] = float(Y/0.381153)
            k[2] = float(X/1.89248)
        elif k[0] == 1:     # Brownian noise
            k[1] = float(3 * Y / X)
        elif k[0] == 2:     # ramp noise
            k[1] = float(2 * Y / X**2)
        va = self.build_component_va(j)
        self.va_j[j] = va
        self.plot_j[j].set_data(self.tau, va)

    def update_fit(self) -> None:
        """
        Update the fit to the Allan variance curve with the sum of the component
        Allan variance curves.
        """

        if self.J == 0: # No component curves
            self.va_fit = None
            self.plot_fit.set_data([], [])
        else:
            self.va_fit = np.zeros(len(self.tau))
            for j in range(self.J):
                self.va_fit += self.va_j[j]
            self.plot_fit.set_data(self.tau, self.va_fit)

    def fopt(self,
            k1: list
        ) -> np.ndarray:
        """ Return the error array of the fit to the true Allan variance. """

        na = self.opt_first
        nb = self.opt_last + 1
        y = np.zeros(nb - na)
        for j in range(self.J):
            k = self.ks[j]
            k[1] = 10**min(k1[j], 12)
            y += self.build_component_va(j)[na:nb]
        return np.log10(self.va[na:nb]/y)**2

    def on_press(self,
            event: MouseEvent
        ) -> None:
        """
        Left-mouse click:
            Begin component curve move.

        Left-mouse click with key press:
            Create new component curve.

        Shift, left-mouse click or middle click:
            Begin click and drag to pan view.
        """

        # Exit if mouse is outside canvas.
        if event.inaxes != self.ax:
            return

        # Depending on which mouse button is pressed,
        if event.button == 1: # left mouse button
            if self.shift: # If shift key is down, begin view panning.
                # Remember where the click was.
                self.x_on_press = event.xdata
                self.y_on_press = event.ydata
                self.xlim_on_press = self.ax.get_xlim()
                self.ylim_on_press = self.ax.get_ylim()

            elif self.new_key is not None: # Make a new curve.
                # Initialize the component parameters.
                key_slopes = {"q": -2, "w": -1, "f": 0, "b": 1, "r":2}
                if self.new_key == "f":
                    k = [key_slopes[self.new_key], 0.0, 0.0]
                else:
                    k = [key_slopes[self.new_key], 0.0]

                # Append the component parameters.
                self.ks.append(k)

                # Create and append an empty curve.
                self.va_j.append(np.zeros(len(self.tau)))
                plot_obj, = self.ax.plot([], [],
                    color="#CCCCCC", linewidth=0.4)
                self.plot_j.append(plot_obj)
                self.J += 1

                # Select the new curve, move (define) it to be collocated with
                # the mouse, and highlight it.
                self.j_hi = self.J - 1
                self.move_component(event.xdata, event.ydata)
                self.highlight_component()

                # Update the total fit Allan variance.
                self.update_fit()

                # Refresh the drawing.
                self.canvas.draw_idle()

            else: # Highlight component curve.
                # Find the component curve closest to the mouse.
                r_min_anywhere = np.inf
                j_min = None
                for j in range(self.J):
                    y = self.va_j[j]
                    dx = np.log10(event.xdata/self.tau)
                    dy = np.log10(event.ydata/y)
                    r = np.sqrt(dx**2 + dy**2)
                    r_min = r.min()
                    if r_min < r_min_anywhere:
                        r_min_anywhere = r_min
                        j_min = j

                # Find the optimization bound closest to the mouse.
                x_ratio_left = event.xdata/self.opt_left
                x_ratio_right = event.xdata/self.opt_right
                dx_left = np.abs(np.log10(x_ratio_left))
                dx_right = np.abs(np.log10(x_ratio_right))
                if dx_left < r_min_anywhere:
                    r_min_anywhere = dx_left
                    j_min = -1
                if dx_right < r_min_anywhere:
                    r_min_anywhere = dx_right
                    j_min = -2

                # Remember the selected bound or curve.
                self.j_hi = j_min

                if self.j_hi == -1: # left optimization bound
                    self.x_ratio = x_ratio_left
                    self.y_ratio = 1.0
                    self.highlight_bound()

                elif self.j_hi == -2: # right optimization bound
                    self.x_ratio = x_ratio_right
                    self.y_ratio = 1.0
                    self.highlight_bound()

                else: # Select the component curve.
                    # Find the ratio of the mouse position to the component
                    # curve's position.
                    k = self.ks[self.j_hi]
                    if k[0] == -2:
                        x_k, y_k = event.xdata, 3 * k[1] / event.xdata**2
                    elif k[0] == -1:
                        x_k, y_k = event.xdata, k[1] / event.xdata
                    elif k[0] == 0:
                        x_k, y_k = 1.89248 * k[2], 0.381153 * k[1]
                    elif k[0] == 1:
                        x_k, y_k = event.xdata, k[1] * event.xdata / 3
                    elif k[0] == 2:
                        x_k, y_k = event.xdata, k[1] * event.xdata**2 / 2
                    self.x_ratio = event.xdata / x_k
                    self.y_ratio = event.ydata / y_k

                    self.highlight_component()
                    self.update_fit()

                # Refresh the drawing.
                self.canvas.draw_idle()

        elif event.button == 2: # If middle mouse button, begin view panning.
            # Remember where the click was.
            self.x_on_press = event.xdata
            self.y_on_press = event.ydata
            self.xlim_on_press = self.ax.get_xlim()
            self.ylim_on_press = self.ax.get_ylim()

    def on_motion(self,
            event: MouseEvent
        ) -> None:
        """
        Shift, left-mouse drag or middle click:
            Pan the view.

        Otherwise:
            Move the selected control point.
        """

        # Exit if mouse is outside canvas.
        if event.inaxes != self.ax:
            return

        # Drag view.
        if (self.shift and event.button == 1) or (event.button == 2):
            # Get the change in mouse position.
            dx = event.xdata/self.x_on_press
            dy = event.ydata/self.y_on_press

            # Adjust the view limits.
            self.xlim_on_press /= dx
            self.ylim_on_press /= dy
            self.ax.set_xlim(self.xlim_on_press)
            self.ax.set_ylim(self.ylim_on_press)

            # Move the lower and upper edges of the optimization bounds.
            self.opt_low, self.opt_high = self.ax.get_ylim()
            self.plot_left.set_data([self.opt_left, self.opt_left],
                [self.opt_low, self.opt_high])
            self.plot_right.set_data([self.opt_right, self.opt_right],
                [self.opt_low, self.opt_high])

        # Move the component curve.
        elif self.j_hi is not None:
            if self.j_hi < 0:
                self.move_bound(event.xdata)
            else:
                self.move_component(event.xdata, event.ydata)
                self.update_fit()

        # Refresh the drawing.
        self.canvas.draw_idle()

    def on_release(self,
            _event: MouseEvent
        ) -> None:
        """ Unselect any selected control point and reset the view. """

        # Unhighlight component curve.
        if self.j_hi is not None:
            # Dim the curve or optimization bound.
            if self.j_hi < 0: # left or right bound
                self.dim_bound()
            else: # component curve
                self.dim_component()

            # Reset the ratios and selection index.
            self.x_ratio = 1.0
            self.y_ratio = 1.0
            self.j_hi = None

            # Refresh the drawing.
            self.canvas.draw_idle()

    def on_scroll(self,
            event: MouseEvent
        ) -> None:
        """
        Zoom view centered on the mouse location.
        Hold shift to zoom faster.
        """

        # Exit if mouse is outside canvas.
        if event.inaxes != self.ax:
            return

        # Get the zoom factor.
        f = 0.8 if self.shift else 0.95
        if event.button == "down":
            f = 1/f

        # Get the current view limits.
        xmin, xmax = self.ax.get_xlim()
        ymin, ymax = self.ax.get_ylim()

        # Get the new view limits.
        xmin = event.xdata * (xmin / event.xdata)**f
        xmax = event.xdata * (xmax / event.xdata)**f
        ymin = event.ydata * (ymin / event.ydata)**f
        ymax = event.ydata * (ymax / event.ydata)**f

        # Set the new axis limits.
        self.ax.set_xlim([xmin, xmax])
        self.ax.set_ylim([ymin, ymax])

        # Move the lower and upper edges of the optimization bounds.
        self.opt_low, self.opt_high = ymin, ymax
        self.plot_left.set_data([self.opt_left, self.opt_left],
            [self.opt_low, self.opt_high])
        self.plot_right.set_data([self.opt_right, self.opt_right],
            [self.opt_low, self.opt_high])

        # Refresh the drawing.
        self.canvas.draw_idle()

    def on_key_press(self,
            event: KeyEvent
        ) -> None:
        """
        Register shift key press or new-curve key press, reset view on "h" key,
        or run optimization on "o" key.
        """

        if event.key == "shift":
            self.shift = True
        elif event.key in ["q", "w", "f", "b", "r"]: # new curve
            self.new_key = event.key
        elif event.key == "h": # Reset the view.
            self.home()
            self.canvas.draw_idle()
        elif event.key in ["backspace", "delete", "x"]: # delete curve
            j = self.j_hi
            if j is not None:
                self.x_ratio = 1.0
                self.y_ratio = 1.0
                self.ks.pop(j)
                self.va_j.pop(j)
                self.plot_j[j].remove() # remove the object from the plot
                self.plot_j.pop(j) # remove the element from the list
                self.J -= 1
                self.update_fit()
                self.j_hi = None

                # Refresh the drawing.
                self.canvas.draw_idle()
        elif event.key == "o":
            # Early exit for nothing to optimize.
            if self.J == 0:
                return

            # Show that the optimization is running.
            self.ax.set_facecolor((0.95, 0.95, 0.95, 1.0))
            self.canvas.draw_idle()

            # Optimize the variances.
            k1lg = [np.log10(max(k[1], 1e-12)) for k in self.ks]
            k1lg = opt.leastsq(self.fopt, k1lg, maxfev=1000)[0]
            for j in range(self.J):
                self.ks[j][1] = float(10**k1lg[j])

            # Update the component curves.
            for j in range(self.J):
                va = self.build_component_va(j)
                self.va_j[j] = va
                self.plot_j[j].set_data(self.tau, va)

            # Update the total fit.
            self.update_fit()

            # Show that the optimization is done.
            self.ax.set_facecolor((1.0, 1.0, 1.0, 1.0))
            self.canvas.draw_idle()

    def on_key_release(self,
            event: KeyEvent
        ) -> None:
        """ Unregister shift key and new-curve key presses. """

        if event.key == "shift":
            self.shift = False
        elif event.key in ["q", "w", "f", "b", "r"]: # new curve
            self.new_key = None

    def on_resize(self,
            _event: ResizeEvent
        ) -> None:
        """
        On window resize, maintain the view as either the limits of the data
        with padding or the current view.
        """

        self.resize()
        self.canvas.draw_idle()

    def on_close(self,
            _event: CloseEvent
        ) -> None:
        """ Restore the default keybindings. """

        plt.rcParams["keymap.back"] = ["left", "c",
            "backspace", "MouseButton.BACK"]
        plt.rcParams["keymap.fullscreen"] = ["f", "ctrl+f"]
        plt.rcParams["keymap.zoom"] = ["o"]
        plt.rcParams["keymap.quit"] = ["ctrl+w", "cmd+w", "q"]
