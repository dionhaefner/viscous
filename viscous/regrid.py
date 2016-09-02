import numpy as np
from scipy import interpolate, spatial

try:
    from numba import jit
except ImportError:
    print("Numba not found")
    jit = lambda f: f

class Regridder(object):
    def __init__(self):
        self._points = None
        self._method = None
        self._nanmask = None
        self._triangulation = None

    #@jit
    def evaluate(self, points, values, rpoints, method="linear"):
        points = np.squeeze(points)
        if len(points.shape) == 1:
            dim = 1
        elif len(points.shape) == 2:
            dim = points.shape[1]
        else:
            raise ValueError("Points must be ndarray of shape (npoints,dim)")

        methods = ["nearest", "linear", "cubic"]
        if not method in methods:
            raise ValueError("Supported methods: {}".format(", ".join(methods)))

        if method == "cubic" and dim > 2:
            raise ValueError("Cubic interpolator only supported for 1D and 2D data")

        nanmask = ~np.isnan(values)
        if not np.array_equal(self._points, points) \
          or self._method != method \
          or not np.array_equal(self._nanmask, nanmask):
            if dim == 1 or method == "nearest":
                self._triangulation = None
            elif method == "linear":
                self._triangulation = spatial.Delaunay(points)
            elif method == "cubic":
                self._triangulation = spatial.Delaunay(points[nanmask])
            self._points = points
            self._method = method
            self._nanmask = nanmask

        triangulation = self._triangulation
        if dim == 1:
            nearest_interpolator = lambda: interpolate.interp1d(points, values, kind="nearest")
            linear_interpolator = lambda: interpolate.interp1d(points, values, kind="linear")
            cubic_interpolator = lambda: interpolate.interp1d(points[nanmask], values[nanmask], kind="cubic")
        else:
            nearest_interpolator = lambda: interpolate.NearestNDInterpolator(points, values)
            linear_interpolator = lambda: interpolate.LinearNDInterpolator(triangulation, values)
            cubic_interpolator = lambda: interpolate.CloughTocher2DInterpolator(triangulation, values[nanmask])

        if method == "nearest":
            ivalues = nearest_interpolator()(rpoints)
        elif method == "linear":
            lval = linear_interpolator()(rpoints)
            mask = np.isnan(lval)
            lval[mask] = nearest_interpolator()(np.vstack([x[mask] for x in rpoints]).T)
            ivalues = lval
        elif method == "cubic":
            cval = cubic_interpolator()(rpoints)
            nvalues = nearest_interpolator()(rpoints)
            cval[np.isnan(nvalues)] = np.nan
            ivalues = cval

        return np.squeeze(ivalues)

# global Regridder object so settings can be cached between function calls
regridder = Regridder()
def regrid(coords, values, rcoords, method="linear"):
    try:
        tmp = iter(coords[0])
    except TypeError:
        coords = (coords,)
        rcoords = (rcoords,)
    if len(coords) != len(rcoords):
        raise ValueError("Coordinates must have the same dimensions")
    get_points = lambda x: np.vstack([i.flatten() for i in x]).T
    coords = get_points(coords)
    values = values.flatten()
    return regridder.evaluate(coords, values, rcoords, method)
