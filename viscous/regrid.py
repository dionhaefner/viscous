import numpy as np
from scipy import interpolate, spatial

class Regridder(object):
    def __init__(self):
        self._points = None
        self._method = None
        self._nanmask = None
        self._triangulation = None
        self._kdtree = None
        self._dim = None


    def _nearest_interpolator(self,x,y):
        xp = np.array([xi.flatten() for xi in x])
        _, i = self._kdtree.query(xp.T, n_jobs=-1)
        ival = y.flat[i].reshape(x[0].shape)
        return np.squeeze(ival)

    def _linear_interpolator(self,x,y):
        if self._dim == 1:
            ival = interpolate.interp1d(self._points.flatten(),
                                        y, kind="linear")(x)[:,np.newaxis]
        else:
            ival = interpolate.LinearNDInterpolator(self._triangulation, y)(x)
        return np.squeeze(ival)

    def _cubic_interpolator(self,x,y):
        if self._dim == 1:
            ival = interpolate.interp1d(self._points[self._nanmask].flatten(),
                                        y[self._nanmask].flatten(),
                                        kind="cubic")(x)[:,np.newaxis]
        else:
            ival = interpolate.CloughTocher2DInterpolator(self._triangulation,
                                                          y[self._nanmask])(x)
        return np.squeeze(ival)

    def evaluate(self, points, values, rpoints, method="linear"):
        if len(np.array(points).shape) == 1:
            self._dim = 1
            points = points[:,np.newaxis]
        elif len(points.shape) == 2:
            self._dim = points.shape[1]
        else:
            raise ValueError("Points must be ndarray of shape (npoints,dim)")

        methods = ["nearest", "linear", "cubic"]
        if not method in methods:
            raise ValueError("Supported methods: {}".format(", ".join(methods)))

        if method == "cubic" and self._dim > 2:
            raise ValueError("Cubic interpolator only supported for 1D and 2D data")

        nanmask = ~np.isnan(values)
        if not np.array_equal(self._points, points) \
          or self._method != method \
          or not np.array_equal(self._nanmask, nanmask):
            self._kdtree = spatial.cKDTree(points)
            if self._dim == 1:
                self._triangulation = None
            elif method == "nearest":
                self._triangulation = None
            elif method == "linear":
                self._triangulation = spatial.Delaunay(points)
            elif method == "cubic":
                self._triangulation = spatial.Delaunay(points[nanmask])
            self._points = points
            self._method = method
            self._nanmask = nanmask

        if method == "nearest":
            ivalues = self._nearest_interpolator(rpoints,values)
        elif method == "linear":
            lval = self._linear_interpolator(rpoints,values)
            mask = np.isnan(lval)
            lval[mask] = self._nearest_interpolator([x[mask] for x in rpoints],values)
            ivalues = lval
        elif method == "cubic":
            cval = self._cubic_interpolator(rpoints,values)
            nval = self._nearest_interpolator(rpoints,values)
            cval[np.isnan(nval)] = np.nan
            ivalues = cval
        return np.squeeze(ivalues)

# global Regridder object so settings can be cached between function calls
regridder = Regridder()
def regrid(coords, values, rcoords, method="linear", cyclic_ax=None, cyclic_val=360.):
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
    if not cyclic_ax is None:
        npoints = coords.shape[0]
        coords = np.tile(coords,(3,1))
        coords[:npoints,cyclic_ax] -= cyclic_val
        coords[npoints:2*npoints,cyclic_ax] += cyclic_val
        values = np.tile(values,3)
    return regridder.evaluate(coords, values, rcoords, method)
