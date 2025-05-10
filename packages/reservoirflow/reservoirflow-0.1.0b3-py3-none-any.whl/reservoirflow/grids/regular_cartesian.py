"""
RegularCartesian
================
"""

import numpy as np
import pyvista as pv
import scipy.sparse as ss

from reservoirflow import utils
from reservoirflow.grids.grid import Grid
from reservoirflow.utils.helpers import _lru_cache


class RegularCartesian(Grid):
    """RegularCartesian grid class.

    Returns
    -------
    Grid
        Grid object.
    """

    # ToDo
    # ----
    # - make default calc all flatten because flatten > reshape is faster
    #   than reshape > flatten.

    name = "RegularCartesian"

    def __init__(
        self,
        nx: int,
        ny: int,
        nz: int,
        dx,
        dy,
        dz,
        kx=None,
        ky=None,
        kz=None,
        phi=None,
        z=0,
        comp: float = None,
        unit="field",
        dtype="double",
        unify=True,
        verbose=False,
    ):
        """Create RegularCartesian Grid.

        Parameters
        ----------
        nx : int
            number of cells in x-direction (excluding boundary cells)
            and must be >= 1. Boundary cells are added automatically.
            Consequently, nx values are increased by 2 to account for
            the boundary cells in x-direction.
        ny : int
            number of cells in y-direction (excluding boundary cells)
            and must be >= 1. Boundary cells are added automatically.
            Consequently, ny values are increased by 2 to account for
            the boundary cells in y-direction.
        nz : int
            number of grids in z-direction (excluding boundary cells)
            and must be >= 1. Boundary cells are added automatically.
            Consequently, nz values are increased by 2 to account for
            the boundary cells in z-direction.
        dx : int, float, array-like
            grid dimension in x-direction. In case of a list or an array,
            the length should be equal to nx+2 (including boundary cells).
            Values should be in natural order (i.e. from left to right).
        dy : int, float, array-like
            grid dimension in y-direction. In case of a list or an array,
            the length should be equal to ny+2 (including boundary cells).
            Values should be in natural order (i.e. from front to back).
        dz : int, float, array-like
            grid dimension in z-direction. In case of a list or an array,
            the length should be equal to nz+2 (including boundary cells).
            Values should be in natural order (i.e. from bottom to top).
        kx : int, float, array-like, optional
            Permeability in x-direction. In case of a list or an array,
            the length should be equal to nx+2 (including boundary cells).
            Values should be in natural order (i.g.from left to right).
            These values are only relevant based on the flow direction
            (e.g. kx is ignored if there is no flow at x-direction).
        ky : int, float, array-like, optional
            Permeability in y-direction. In case of a list or an array,
            the length should be equal to ny+2 (including boundary cells).
            Values should be in natural order (i.e. from front to back).
            These values are only relevant based on the flow direction
            (e.g. ky is ignored if there is no flow at y-direction).
        kz : int, float, array-like, optional
            Permeability in z-direction. In case of a list or an array,
            the length should be equal to nz+2 (including boundary cells).
            Values should be in natural order (i.e. from bottom to top).
            These values are only relevant based on the flow direction
            (e.g. kz is ignored if there is no flow at z-direction).
        phi : float, array-like, optional
            effective porosity (in all directions). In case of an array,
            the shape should be equal to `grid.shape` (including
            boundary cells). Values should be in natural order
            (i.e. from left to right at x-direction, from front to back
            at y-direction, and from bottom to top at z-direction).
        z : int, float, array-like, optional.
            depth of grid tops.

            warning
            -------
            grid tops (z) is not fully implemented in visualization.

        comp : float, optional
            compressibility.
        unit : str ('field', 'metric', 'lab'), optional
            unit used in input and output. Both `units` and `factors`
            attributes will be updated based on the selected `unit` and
            can be accessed directly from this class.
        dtype : str or `np.dtype`, optional
            data type used in all arrays. Numpy dtype such as
            `np.single` or `np.double` can be used.
        unify : bool, optional
            unify shape to be always tuple of 3 when set to True. When
            set to False, shape includes only the number of girds in
            flow direction as tuple. This option is only relevant in
            case of 1D or 2D flow. This option may be required to make
            1D and 2D shapes shapes of this class more consistent with
            each other or with 3D shape.
        verbose : bool, optional
            print information for debugging.

        Notes
        -----

        Definitions:
        `Permeability </user_guide/glossary/glossary.html#term-permeability>`_
        ,
        `Porosity </user_guide/glossary/glossary.html#term-porosity>`_
        .

        .. note::
            Both attributes units and factors are defined based on `unit`
            argument, for more details, check
            `Units & Factors </user_guide/units_factors/units_factors.html>`_.
            For definitions, check
            `Glossary </user_guide/glossary/glossary.html>`_.

        .. todo::
            * Arrays default shape:
                - flatten arrays should be the default options.
                - reshaping flatten arrays is faster than flattening reshaped arrays.
            * Complete unify feature:
                - complete unify feature to all class components.
        """
        super().__init__(unit, dtype, unify, verbose)
        assert nx >= 1, "nx must be 1 or larger."
        assert ny >= 1, "ny must be 1 or larger."
        assert nz >= 1, "nz must be 1 or larger."
        self.nx, self.ny, self.nz = nx, ny, nz
        self.__calc_cells_d(dx, dy, dz, False)
        self.__calc_cells_A()
        self.__calc_cells_V()
        self.set_props(kx, ky, kz, phi, z, comp)
        self.cells_id = self.get_cells_id(False, False, "array")

    # -------------------------------------------------------------------------
    # Basic:
    # -------------------------------------------------------------------------

    @_lru_cache(maxsize=1)
    def get_D(self) -> int:
        """Returns the grid dimension (D) as int.

        Returns
        -------
        int
            number of dimensions higher than 1.
        """
        self.D = sum([1 if n > 1 else 0 for n in (self.nx, self.ny, self.nz)])

        if self.verbose:
            print(f"[info] D is {self.D}.")

        return self.D

    @_lru_cache(maxsize=2)
    def get_shape(self, boundary: bool = False) -> tuple:
        """Returns the number of grids in x, y, z as tuple of
        (nx, ny, nz).

        Parameters
        ----------
        boundary : bool, optional
            include boundary cells.

        Returns
        -------
        tuple
            the number of grids as (nx, ny, nz).
        """
        if boundary:
            self.get_fdir()
            if "x" in self.fdir:
                self.nx_b = self.nx + 2
            else:
                self.nx_b = self.nx
            if "y" in self.fdir:
                self.ny_b = self.ny + 2
            else:
                self.ny_b = self.ny
            if "z" in self.fdir:
                self.nz_b = self.nz + 2
            else:
                self.nz_b = self.nz
            self.shape = (self.nx_b, self.ny_b, self.nz_b)
        else:
            self.shape = (self.nx, self.ny, self.nz)

        if self.verbose:
            s = utils.helpers.get_boundary_str(boundary)
            print(f"[info] shape {s} is {self.shape}.")

        return self.shape

    @_lru_cache(maxsize=2)
    def get_n(self, boundary: bool = True) -> int:
        """Returns the total number of grid cells as int.

        Parameters
        ----------
        boundary : bool, optional
            include boundary cells.

        Returns
        -------
        int
            total number of cells.
        """
        shape = self.get_shape(boundary)
        self.n = np.prod(shape)

        if self.verbose:
            s = utils.helpers.get_boundary_str(boundary)
            print(f"[info] n {s} is {self.n}.")

        return self.n

    @_lru_cache(maxsize=2)
    def get_n_max(self, boundary: bool = True):
        """Returns the maximum number of grid cells (n_max) as int.

        Parameters
        ----------
        boundary : bool, optional
            include boundary cells.

        Returns
        -------
        int
            maximum number of grids as max(nx, ny, nz).
        """
        shape = self.get_shape(boundary)
        self.n_max = max(shape)

        if self.verbose:
            s = utils.helpers.get_boundary_str(boundary)
            print(f"[info] n_max {s} is {self.n_max}.")

        return self.n_max

    @_lru_cache(maxsize=1)
    def get_fdir(self) -> str:
        """Returns the flow direction (fdir) as str.

        Returns
        -------
        str
            contains one or combination of ('-','x','y','z') based on
            the grid dimensions that are higher than 1.
        """
        self.get_D()
        self.get_shape(False)

        if self.D == 0:
            self.fdir = "-"
        elif self.D == 1:
            flow_dir_id = np.argmax(self.shape)
            if flow_dir_id == 0:
                self.fdir = "x"
            elif flow_dir_id == 1:
                self.fdir = "y"
            elif flow_dir_id == 2:
                self.fdir = "z"
        elif self.D == 2:
            flow_dir_id = np.argmin(self.shape)
            if flow_dir_id == 2:
                self.fdir = "xy"
            elif flow_dir_id == 1:
                self.fdir = "xz"
            elif flow_dir_id == 0:
                self.fdir = "yz"
        elif self.D == 3:
            self.fdir = "xyz"

        if self.verbose:
            print(f"[info] fdir is {self.fdir}.")

        return self.fdir

    @_lru_cache(maxsize=2)
    def get_fshape(
        self,
        boundary: bool = True,
        points=False,
    ):
        """Returns flow shape (fshape) as tuple.

        Parameters
        ----------
        boundary : bool, optional
            include boundary cells.
        points : bool, optional
            True for points (e.g. coords, icoords) and False for scaler
            values (e.g. id).

        Returns
        -------
        tuple
            number of grids at flow directions in z, y, x order.
        """
        nx, ny, nz = self.get_shape(boundary)

        if self.fdir == "xyz":
            self.fshape = (nz, ny, nx)
        else:
            if not self.unify:
                if self.fdir == "-":
                    self.fshape = (1,)
                elif self.fdir == "x":
                    self.fshape = (nx,)
                elif self.fdir == "y":
                    self.fshape = (ny,)
                elif self.fdir == "z":
                    self.fshape = (nz,)
                elif self.fdir == "xy":
                    self.fshape = (ny, nx)
                elif self.fdir == "xz":
                    self.fshape = (nz, nx)
                elif self.fdir == "yz":
                    self.fshape = (nz, ny)
                else:
                    raise ValueError("unknown fdir value.")
            else:
                if self.fdir == "-":
                    self.fshape = (1, 1, 1)
                elif self.fdir == "x":
                    self.fshape = (1, 1, nx)
                elif self.fdir == "y":
                    self.fshape = (1, ny, 1)
                elif self.fdir == "z":
                    self.fshape = (nz, 1, 1)
                elif self.fdir == "xy":
                    self.fshape = (1, ny, nx)
                elif self.fdir == "xz":
                    self.fshape = (nz, 1, nx)
                elif self.fdir == "yz":
                    self.fshape = (nz, ny, 1)
                else:
                    raise ValueError("unknown fdir value.")

        if points:
            self.fshape = self.fshape + (3,)

        if self.verbose:
            s1 = utils.helpers.get_boundary_str(boundary)
            s2 = utils.helpers.get_points_str(points)
            print(f"[info] fshape {s1}{s2} is {self.fshape}.")

        return self.fshape

    @_lru_cache(maxsize=4)
    def get_order(
        self,
        type: str = "natural",
        boundary: bool = True,
        fshape: bool = False,
    ) -> np.ndarray:
        """Returns grid order as ndarray.

        Parameters
        ----------
        type : str, optional
            grid order type in which grids are numbered. Currently, only
            "natural" order is supported.
        boundary : bool, optional
            include boundary cells.
        fshape : bool, optional
            reshape to flow shape instead of flatten.

        Returns
        -------
        ndarray
            gird order as array.
        """
        if type == "natural":
            self.order = np.arange(self.get_n(True))
        else:
            raise ValueError(
                "Order type is not supported or unknown. "
                "Supported order types: ['natural']"
            )

        if not boundary:
            self.order = self.remove_boundaries(self.order, False, "both")

        if fshape:
            shape = self.get_fshape(boundary, False)
            self.order = self.order.reshape(shape)

        if self.verbose:
            s1, s2 = utils.helpers.get_verbose_str(boundary, fshape)
            print(f"[info] order was computed ({s1} - {s2}).")

        return self.order

    @_lru_cache(maxsize=1)
    def get_ones(
        self,
        boundary: bool = True,
        fshape: bool = False,
        sparse: bool = False,
    ):
        """Returns array of ones.

        Parameters
        ----------
        boundary : bool, optional
            include boundary cells.
        fshape : bool, optional
            reshape to flow shape instead of flatten.
        sparse : bool, optional
            values as sparse matrix (True) or as ndarray (False).

        Returns
        -------
        array
            array in flow shape filled with ones.

        """
        # ToDo
        # ----
        # - Make sure sparse option is valid.
        if fshape:
            shape = self.get_fshape(boundary, False)
        else:
            shape = self.get_n(boundary)

        if not sparse:
            self.ones = np.ones(shape, dtype=self.dtype)
        else:
            self.ones = ss.lil_matrix(shape, dtype=self.dtype)

        if self.verbose:
            print(f"[info] ones array was computed.")

        return self.ones

    @_lru_cache(maxsize=1)
    def get_zeros(
        self,
        boundary: bool = True,
        fshape: bool = False,
        sparse: bool = False,
    ):
        """Returns array of zeros.

        Parameters
        ----------
        boundary : bool, optional
            include boundary cells.
        fshape : bool, optional
            reshape to flow shape instead of flatten.
        sparse : bool, optional
            values as sparse matrix (True) or as ndarray (False).

        Returns
        -------
        array
            array in flow shape filled with ones.

        """
        # ToDo
        # ----
        # - Make sure sparse option is valid.
        if fshape:
            shape = self.get_fshape(boundary, False)
        else:
            shape = self.get_n(boundary)

        if not sparse:
            self.zeros = np.zeros(shape, dtype=self.dtype)
        else:
            self.zeros = ss.lil_matrix(shape, dtype=self.dtype) * 0

        if self.verbose:
            print(f"[info] zeros array was computed.")

        return self.zeros

    # -------------------------------------------------------------------------
    # Cells id and coordinates:
    # -------------------------------------------------------------------------

    @_lru_cache(maxsize=2)
    def get_cells_i(
        self,
        boundary: bool = True,
        fshape: bool = False,
        fmt="array",
    ):
        """Returns range based on the number of cells.

        Parameters
        ----------
        boundary : bool, optional
            include boundary cells.
        fshape : bool, optional
            reshape to flow shape instead of flatten. If set to
            True, fmt argument will be ignored.
        fmt : str, optional
            output format as str from ['array', 'list', 'tuple', 'set'].
            This argument is ignored if fshape argument is set to True.
            For a better performance, use 'set' to check if an item is
            in a list or not. Use tuples to iterate through items. When
            option 'array' is used, utils.helpers.isin() must be used to check
            if a tuple of 3 is in the array.

        Returns
        -------
        int
            total number of cells.
        """
        n = self.get_n(boundary)
        self.cells_i = np.arange(n)

        if fshape:
            shape = self.get_fshape(boundary, False)
            self.cells_i = self.cells_i.reshape(shape)
        else:
            self.cells_i = utils.helpers.reformat(self.cells_i, fmt)

        if self.verbose:
            s = utils.helpers.get_boundary_str(boundary)
            print(f"[info] cells_i {s} for {self.n} was computed.")

        return self.cells_i

    @_lru_cache(maxsize=None)
    def get_cell_id(
        self,
        coords=[],
        boundary: bool = True,
    ):
        """Returns cell/cells id based on natural as int/list.

        Parameters
        ----------
        coords : tuple of int, tuple of tuples of int
            cell coordinates (i,j,k) as a tuple of int. For multiple
            cells, tuple of tuples of int as ((i,j,k),(i,j,k),..).
            Warning: providing an unhashable type (e.g. list, ndarray)
            is not supported and will cause TypeError.
        boundary : bool, optional
            include boundary cells.

        Returns
        -------
        int/list
            cell id based on natural order as int for a single cell
            coords or as list of int for multiple cells coords.
        """
        pyvista_grid = self.get_pyvista_grid(boundary)

        if all(isinstance(c, tuple) for c in coords):
            return [pyvista_grid.cell_id(c) for c in coords]
        else:
            return pyvista_grid.cell_id(coords)

    @_lru_cache(maxsize=4)
    def get_cells_id(
        self,
        boundary: bool = True,
        fshape: bool = False,
        fmt="array",
    ):
        """Returns all cells id based on natural order as ndarray.

        Parameters
        ----------
        boundary : bool, optional
            include boundary cells.
        fshape : bool, optional
            reshape to flow shape instead of flatten. If set to
            True, fmt argument will be ignored.
        fmt : str, optional
            output format as str from ['array', 'list', 'tuple', 'set'].
            This argument is ignored if fshape argument is set to True.
            For a better performance, use 'set' to check if an item is
            in a list or not. Use tuples to iterate through items. When
            option 'array' is used, utils.helpers.isin() must be used to check
            if a tuple of 3 is in the array.

        Returns
        -------
        ndarray
            cells id in natural order as array.

        """
        # ToDo
        # ----
        # can be a generator instead.
        cells_id = self.get_order("natural", boundary, fshape)

        if not fshape:
            cells_id = utils.helpers.reformat(cells_id, fmt)

        if self.verbose:
            s1, s2 = utils.helpers.get_verbose_str(boundary, fshape)
            print(f"[info] cells_id was computed ({s1} - {s2}).")

        return cells_id

    @_lru_cache(maxsize=None)
    def get_cell_coords(
        self,
        id,
        boundary: bool = True,
    ):
        """Returns cell/cells coordinates as tuple/list of tuples.

        Parameters
        ----------
        id : int, tuple of int
            cell id based on natural order as int. For multiple cells,
            tuple of int (id,id,...). Warning: providing an unhashable
            type (e.g. list, ndarray) is not supported and will cause
            TypeError.
        boundary : bool, optional
            include boundary cells.

        Returns
        -------
        tuple/list of tuples
            cell/cells coordinates as tuple/list of tuples.
        """
        pyvista_grid = self.get_pyvista_grid(boundary)

        if isinstance(id, (list, tuple, np.ndarray)):
            return [tuple(x) for x in pyvista_grid.cell_coords(id)]
        else:
            return tuple(pyvista_grid.cell_coords(id))

    @_lru_cache(maxsize=4)
    def get_cells_coords(
        self,
        boundary: bool = True,
        fshape: bool = False,
        fmt="tuple",
    ):
        """Returns all cells coords based on (i,j,k).

        Parameters
        ----------
        boundary : bool, optional
            include boundary cells.
        fshape : bool, optional
            reshape to flow shape instead of flatten. If set to
            True, fmt argument will be ignored.
        fmt : str, optional
            output format as str from ['array', 'list', 'tuple', 'set'].
            This argument is ignored if fshape argument is set to True.
            For a better performance, use 'set' to check if an item is
            in a list or not. Use tuples to iterate through items. When
            option 'array' is used, utils.helpers.isin() must be used to check
            if a tuple of 3 is in the array.

        Returns
        -------
        ndarray
            cells coords in (i,j,k) as array.

        """
        # ToDo
        # ----
        # - can be a generator instead?
        # - check if needs optimization.
        cells_id = self.get_cells_id(boundary, False, "array")
        pyvista_grid = self.get_pyvista_grid(True)
        cells_coords = pyvista_grid.cell_coords(cells_id)

        if fshape:
            shape = self.get_fshape(boundary, True)
            cells_coords = cells_coords.reshape(shape)
        else:
            cells_coords = utils.helpers.reformat(cells_coords, fmt)

        if self.verbose:
            s1, s2 = utils.helpers.get_verbose_str(boundary, fshape)
            print(f"[info] cells_coords was computed ({s1} - {s2}).")

        return cells_coords

    @_lru_cache(maxsize=None)
    def get_cell_icoords(self, coords):
        """Convert `coords` from `(i,j,k)` into `(k,j,i)`.

        This method is required to create `icoords` based on `(k,j,i)`
        which can be used to access ndarrays in this class. icoords is
        not compatible with pyvista grid which use `coords` based on
        `(i,j,k)`.

        Parameters
        ----------
        coords : tuple of int, tuple of tuples of int
            cell coordinates (i,j,k) as a tuple of int. For multiple
            cells, tuple of tuples of int as ((i,j,k),(i,j,k),..).
            Warning: providing an unhashable type (e.g. list, ndarray)
            is not supported and will cause TypeError.

        Returns
        -------
        tuple/list of tuples
            internal coords (icoords)

        """
        # ToDo
        # ----
        # - very slow, improve isin method..

        if not isinstance(coords[0], tuple):
            cells_coords = self.get_cells_coords(True, False, "array")
            msg = "coords are out of range."
            assert utils.helpers.isin(coords, cells_coords), msg
            if not self.unify and self.D <= 2:
                icoords = tuple(c for c in coords[::-1] if c > 0)
                assert len(icoords) == self.get_D(), "icoords is not compatible"
            else:
                icoords = tuple(c for c in coords[::-1])
        else:
            icoords = tuple(self.get_cell_icoords(i) for i in coords)

        return icoords

    def get_cells_icoords(
        self,
        boundary: bool = True,
        fshape: bool = False,
        fmt=None,
    ):
        """Returns all cells icoords based on (k,j,i).

        Parameters
        ----------
        boundary : bool, optional
            include boundary cells.
        fshape : bool, optional
            reshape to flow shape instead of flatten. If set to
            True, fmt argument will be ignored.
        fmt : str, optional
            output format as str from ['array', 'list', 'tuple', 'set'].
            This argument is ignored if fshape argument is set to True.
            For a better performance, use 'set' to check if an item is
            in a list or not. Use tuples to iterate through items. When
            option 'array' is used, utils.helpers.isin() must be used to check
            if a tuple of 3 is in the array.

        Returns
        -------
        ndarray
            cells coords in (i,j,k) as array.

        """
        # ToDo
        # ----
        # - Finish implementation.
        cells_coords = self.get_cells_coords(boundary, False, "tuple")
        cells_icoords = self.get_cell_icoords(cells_coords)

        if fshape:
            shape = self.get_fshape(boundary, True)
            cells_icoords = np.array(cells_icoords).reshape(shape)
        else:
            cells_icoords = utils.helpers.reformat(cells_icoords, fmt)

        if self.verbose:
            s1, s2 = utils.helpers.get_verbose_str(boundary, fshape)
            print(f"[info] cells_icoords was computed ({s1} - {s2}).")

        return cells_icoords

    # -------------------------------------------------------------------------
    # Neighbors and Boundaries:
    # -------------------------------------------------------------------------

    @_lru_cache(maxsize=None)
    def get_cell_neighbors(
        self,
        id=None,
        coords=None,
        boundary: bool = False,
        fmt="dict",
    ):
        """Returns cell neighbors.

        This method returns cell neighbors by id or coords. If
        neighbors are desired by id, then id argument should be used.
        The same applies coords argument. This method will raise
        ValueError if none of id or coords arguments were defined or if
        undefined fmt argument was used. Boundary cells are not allowed.

        Warning: passing ndarray of len(shape) > 1 (e.g. coords ndarray)
        causes a TypeError due to the cache decorator used in this
        method since multi-dim ndarray is unhashable.

        Parameters
        ----------
        id : int, iterable of int
            cell id based on natural order as int. For multiple cells,
            list of int [id,id,..] or tuple of int (id,id,...).
        coords : iterable of int, iterable of tuples of int, by default
            None cell coordinates (i,j,k) as a tuple of int. For
            multiple cells, tuple of tuples of int as
            ((i,j,k),(i,j,k),..).
        boundary : bool, optional
            include boundary cells.
        fmt : str, optional
            output format as str from ['array', 'list', 'tuple', 'set',
            'dict']. Use 'dict' to output neighbors in x,y,z directions
            as keys. Use 'tuple' or 'list' for list of neighbors when
            directions are not needed.

        Returns
        -------
        iterable
            cell neighbors.

        Raises
        ------
        ValueError
            None of id or coords arguments are not defined.
        ValueError
            Unknown str value was used for fmt argument.

        """
        # ToDo
        # ----
        # [Empty]
        cell_neighbors = {"x": [], "y": [], "z": []}

        if id is not None:
            assert not isinstance(id, np.ndarray), "block"
            boundaries = self.get_boundaries("id", "set")
            isin_boundary = utils.helpers.isin(id, boundaries) and boundary is True
            assert (
                not isin_boundary
            ), "boundary cells are not allowed with boundary=True."

            # Cells_id = self.get_cells_id(True, False, "set")
            # isin_Cells_id = utils.helpers.isin(id, Cells_id)
            # assert isin_Cells_id, f"id is out of range {Cells_id}."

            cells_id = self.get_cells_id(boundary, False, "set")
            if self.D >= 1:
                n_lst = [id - 1, id + 1]
                neighbors = [i for i in n_lst if i in cells_id]
                cell_neighbors[self.fdir[0]] = neighbors
            if self.D >= 2:
                nx, ny, _ = self.get_shape(True)
                if "x" in self.fdir:
                    n_lst = [id - nx, id + nx]
                elif "y" in self.fdir:
                    n_lst = [id - ny, id + ny]
                neighbors = [i for i in n_lst if i in cells_id]
                cell_neighbors[self.fdir[1]] = neighbors
            if self.D >= 3:
                nx_ny_b = self.nx_b * self.ny_b
                n_lst = [id - nx_ny_b, id + nx_ny_b]
                neighbors = [i for i in n_lst if i in cells_id]
                cell_neighbors[self.fdir[2]] = neighbors
        elif coords is not None:
            boundaries = self.get_boundaries("coords", "set")
            isin_boundary = utils.helpers.isin(coords, boundaries) and boundary is True
            assert (
                not isin_boundary
            ), "boundary cells are not allowed with boundary=True."

            # Cells_coords = self.get_cells_coords(True, False, "set")
            # isin_Cells_coords = utils.helpers.isin(coords, Cells_coords)
            # assert isin_Cells_coords, f"coords are out of range {Cells_coords}."

            cells_coords = self.get_cells_coords(boundary, False, "set")
            i, j, k = coords
            if "x" in self.fdir:
                n_lst = [(i - 1, j, k), (i + 1, j, k)]
                neighbors = [c for c in n_lst if utils.helpers.isin(c, cells_coords)]
                cell_neighbors["x"] = neighbors
            if "y" in self.fdir:
                n_lst = [(i, j - 1, k), (i, j + 1, k)]
                neighbors = [c for c in n_lst if utils.helpers.isin(c, cells_coords)]
                cell_neighbors["y"] = neighbors
            if "z" in self.fdir:
                n_lst = [(i, j, k - 1), (i, j, k + 1)]
                neighbors = [c for c in n_lst if utils.helpers.isin(c, cells_coords)]
                cell_neighbors["z"] = neighbors
        else:
            raise ValueError("at least id or coords argument must be defined.")

        return utils.helpers.reformat(cell_neighbors, fmt=fmt)

    @_lru_cache(maxsize=None)
    def get_cell_boundaries(
        self,
        id=None,
        coords=None,
        fmt="dict",
    ):
        """Returns cell boundaries.

        This method returns cell boundaries by id or coords. If
        boundaries are desired by id, then id argument should be used.
        The same applies coords argument. This method will raise
        ValueError if none of id or coords arguments were defined or if
        undefined fmt argument was used. Boundary cells are not allowed.

        Warning: passing ndarray of len(shape) > 1 (e.g. coords ndarray)
        causes a TypeError due to the cache decorator used in this
        method since multi-dim ndarray is unhashable.

        Parameters
        ----------
        id : int, iterable of int
            cell id based on natural order as int. For multiple cells,
            list of int [id,id,..] or tuple of int (id,id,...).
        coords : iterable of int, iterable of tuples of int, by default
            None cell coordinates (i,j,k) as a tuple of int. For
            multiple cells, tuple of tuples of int as
            ((i,j,k),(i,j,k),..).
        fmt : str, optional
            output format as str from ['array', 'list', 'tuple', 'set',
            'dict']. Use 'dict' to output neighbors in x,y,z directions
            as keys. Use 'tuple' or 'list' for list of neighbors when
            directions are not needed.

        Returns
        -------
        iterable
            cell boundaries.

        Raises
        ------
        ValueError
            None of id or coords arguments are not defined.
        ValueError
            Unknown str value was used for fmt argument.

        """
        # ToDo
        # ----
        # [Empty]
        cell_boundaries = {"x": [], "y": [], "z": []}

        if id is not None:
            boundaries = self.get_boundaries("id", "set")
            isin_boundary = utils.helpers.isin(id, boundaries)
            assert not isin_boundary, "boundary cells are not allowed."
            cell_neighbors = self.get_cell_neighbors(
                id=id,
                boundary=True,
                fmt="dict",
            )
        elif coords is not None:
            boundaries = self.get_boundaries("coords", "set")
            isin_boundary = utils.helpers.isin(coords, boundaries)
            assert not isin_boundary, "boundary cells are not allowed."
            cell_neighbors = self.get_cell_neighbors(
                coords=coords,
                boundary=True,
                fmt="dict",
            )
        else:
            raise ValueError("at least id or coords argument must be defined.")

        cell_boundaries["x"] = list(set(cell_neighbors["x"]).intersection(boundaries))
        cell_boundaries["y"] = list(set(cell_neighbors["y"]).intersection(boundaries))
        cell_boundaries["z"] = list(set(cell_neighbors["z"]).intersection(boundaries))

        return utils.helpers.reformat(cell_boundaries, fmt)

    def remove_boundaries(
        self,
        in_data,
        points=None,
        remove="both",
    ):
        """Remove boundary cells from ndarray.

        Parameters
        ----------
        in_data : ndarray, dict of ndarray
            input data where boundaries need to be removed. Input data
            must be an ndarray with boundaries. Input data as dict with
            keys for these arrays is also possible.
        points : bool, optional
            True for points (i.e. tuples of len 3 like coords, icoords)
            and False for scaler values (e.g. id). If value is set to
            None, bool value is calculated automatically. Warning:
            this argument must be specified in case that in_data was for
            scaler values in fshape that is (#,..,3) (i.e. not flatten).
            For more information about points automatic calculation,
            check the utility function `utils.helpers.ispoints()`.
        remove : str, optional
            boundaries to remove as str in ['both', 'left', 'right'].

        Returns
        -------
        ndarray, dict
            array with boundaries removed.

        Raises
        ------
        ValueError
            boundaries are not included or points argument must be
            correctly assigned.
        ValueError
            dtype must be ndarray.

        See Also
        --------
        extract_boundaries: keep only boundary cells from input data.

        """
        # ToDo
        # ----
        # add fmt argument.
        if isinstance(in_data, np.ndarray):
            if points is None:
                points = utils.helpers.ispoints(in_data)
            fshape = self.get_fshape(True, points)

            if in_data.shape != fshape:
                try:
                    in_data = in_data.reshape(fshape)
                    flatten = True
                except:
                    utils.helpers.shape_error(in_data.shape, fshape)
            else:
                flatten = False

            if remove == "both":
                l = 1
                r = -1
            elif remove == "left":
                l = 1
                r = None
            elif remove == "right":
                l = 0
                r = -1
            else:
                raise ValueError("remove must be in ['both', 'left', 'right']")

            if self.D == 3:
                out_data = in_data[l:r, l:r, l:r]
            else:
                if not self.unify:
                    if self.D == 0:
                        out_data = in_data
                    elif self.D == 1:
                        out_data = in_data[l:r]
                    elif self.D == 2:
                        out_data = in_data[l:r, l:r]
                    else:
                        raise ValueError("Unknown shape.")
                else:
                    fdir = self.get_fdir()
                    if fdir == "-":
                        out_data = in_data
                    elif fdir == "x":
                        out_data = in_data[:, :, l:r]
                    elif fdir == "y":
                        out_data = in_data[:, l:r, :]
                    elif fdir == "z":
                        out_data = in_data[l:r, :, :]
                    elif fdir == "xy":
                        out_data = in_data[:, l:r, l:r]
                    elif fdir == "xz":
                        out_data = in_data[l:r, :, l:r]
                    elif fdir == "yz":
                        out_data = in_data[l:r, l:r, :]
                    else:
                        raise ValueError("Unknown shape.")

            if flatten:
                if not points:
                    out_data = out_data.flatten()
                else:
                    out_data = out_data.reshape((-1, 3))

            return out_data

        elif isinstance(in_data, dict):
            for k, v in in_data.items():
                in_data[k] = self.remove_boundaries(v, remove="both")
            return in_data
        else:
            raise ValueError("dtype must be ndarray.")

    def extract_boundaries(
        self,
        in_data,
        points=None,
        fmt="tuple",
    ):
        """Extract boundary cells from ndarrays.

        Parameters
        ----------
        in_data : ndarray
            input array must contain all cells including boundary cell.
        points : bool, optional
            True for points (i.e. tuples of len 3 like coords, icoords)
            and False for scaler values (e.g. id). If value is set to
            None, bool value is calculated automatically. Warning:
            this argument must be specified in case that in_data was for
            scaler values in fshape that is (#,..,3) (i.e. not flatten).
            For more information about points automatic calculation,
            check the utility function `utils.helpers.ispoints()`.
        fmt : str, optional
            format of output data as str in ['tuple', 'list', 'set',
            'array'].

        Returns
        -------
        ndarray, list, set
            output data based on fmt argument.

        Raises
        ------
        ValueError
            'fmt is unknown' when fmt is not in ['tuple','list','array']
        ValueError
            'dtype must be ndarray' when in_data is not numpy array.

        See Also
        --------
        remove_boundaries: remove boundary cells from input data.

        """
        # ToDo
        # ----
        # The fshape might be checked automatically based on the provided data.
        # Confirm the behavior of when self.unify set to True.
        if isinstance(in_data, np.ndarray):
            if points is None:
                points = utils.helpers.ispoints(in_data)
            fshape = self.get_fshape(True, points)

            if in_data.shape != fshape:
                try:
                    in_data = in_data.reshape(fshape)
                except:
                    utils.helpers.shape_error(in_data.shape, fshape)

            if self.D == 3:
                out_data = np.concatenate(
                    [
                        in_data[:, [0, -1], :].flatten(),
                        in_data[:, 1:-1, [0, -1]].flatten(),
                        in_data[[0, -1], 1:-1, 1:-1].flatten(),
                    ]
                )
            else:
                if not self.unify:
                    if self.D == 0:
                        out_data = in_data
                    elif self.D == 1:
                        out_data = in_data[[0, -1]].flatten()
                    elif self.D == 2:
                        out_data = np.concatenate(
                            [
                                in_data[[0, -1], :].flatten(),
                                in_data[1:-1, [0, -1]].flatten(),
                            ]
                        )
                    else:
                        raise ValueError("unknown shape.")
                else:
                    fdir = self.get_fdir()
                    if fdir == "-":
                        out_data = in_data
                    elif fdir == "x":
                        out_data = in_data[:, :, [0, -1]]
                    elif fdir == "y":
                        out_data = in_data[:, [0, -1], :]
                    elif fdir == "z":
                        out_data = in_data[[0, -1], :, :]
                    elif fdir == "xy":
                        out_data = np.concatenate(
                            [
                                in_data[:, [0, -1], :].flatten(),
                                in_data[:, 1:-1, [0, -1]].flatten(),
                            ]
                        )
                    elif fdir == "xz":
                        out_data = np.concatenate(
                            [
                                in_data[[0, -1], :, :].flatten(),
                                in_data[1:-1, :, [0, -1]].flatten(),
                            ]
                        )
                    elif fdir == "yz":
                        out_data = np.concatenate(
                            [
                                in_data[[0, -1], :, :].flatten(),
                                in_data[1:-1, [0, -1], :].flatten(),
                            ]
                        )
                    else:
                        raise ValueError("unknown shape.")

            if not points:
                out_data = np.sort(out_data.flatten())
            else:
                out_data = out_data.reshape((-1, 3))

            return utils.helpers.reformat(out_data, fmt)
        else:
            raise ValueError("dtype must be ndarray.")

    @_lru_cache(maxsize=2)
    def get_boundaries(
        self,
        by="id",
        fmt="tuple",
    ):
        """Returns all boundary cells by id or coords.

        Parameters
        ----------
        by : str, optional
            output boundaries as 'id' or 'coords'. Other undefined str
            values will raise ValueError.
        fmt : str, optional
            format of output data as str in ['tuple', 'list', 'set',
            'array']. When option 'array' is used, utils.helpers.isin() must be
            used to check if a tuple of 3 is in the array. For a better
            performance, use 'set' to check if an item is in or not and
            use tuples to iterate through items.

        Returns
        -------
        ndarray, list, set
            boundaries by id or coords based on fmt argument.

        Raises
        ------
        ValueError
            by argument must be either 'id' or 'coords'.
        """
        if by == "id":
            Cells_id = self.get_cells_id(True, True, "array")
            return self.extract_boundaries(Cells_id, False, fmt)
        elif by == "coords":
            Cells_coords = self.get_cells_coords(True, True, "array")
            return self.extract_boundaries(Cells_coords, True, fmt)
        else:
            raise ValueError("'by' argument must be either 'id' or 'coords'.")

    # -------------------------------------------------------------------------
    # Dimensions:
    # -------------------------------------------------------------------------

    def __calc_cells_d_(
        self,
        dx,
        dy,
        dz,
    ):
        """Calculates dimensional axes vectors in x, y, z directions.

        This method takes dx, dy, and dz as scalers or iterables and use
        them to construct axes vectors based on the number of grids in
        x, y, z directions. This method is used __calc_cells_d(). Please
        note that dx_, dy_, dz_ refer to axes vectors while dx, dy, dz
        refer to meshgrid arrays.

        Parameters
        ----------
        dx : int, float, array-like
            grid dimension in x-direction. In case of a list or array,
            the length should be equal to nx+2 for all cells including
            boundary cells. Vales should be in natural order (i.e. from
            left to right).
        dy : int, float, array-like
            grid dimension in y-direction. In case of a list or array,
            the length should be equal to ny+2 for all cells including
            boundary cells. Vales should be in natural order (i.g. from
            front to back).
        dz : int, float, array-like
            grid dimension in z-direction. In case of a list or array,
            the length should be equal to nz+2 for all cells including
            boundary cells. Vales should be in natural order (i.g. from
            down to up).

        Returns
        -------
        list
            a list of len 3 for axes vectors as dx, dy, dz.
        """
        nx, ny, nz = self.get_shape(True)
        n_max = self.get_n_max(True)
        self.cells_d_ = []

        def check_d(d, n, s):
            if isinstance(d, (list, tuple, np.ndarray)):
                assert len(d) == n, f"Please add boundary cells in d{s}."
                if isinstance(d, np.ndarray):
                    assert len(d.shape) == 1, f"Use flatten array in d{s}."

        if "x" in self.fdir:
            check_d(dx, nx, "x")
            self.dx_ = np.ones(nx, dtype="int") * dx
            self.cells_d_.append(self.dx_)
        else:
            self.dx_ = np.ones(n_max, dtype="int") * dx
            self.cells_d_.append(dx)

        if "y" in self.fdir:
            check_d(dy, ny, "y")
            self.dy_ = np.ones(ny, dtype="int") * dy
            self.cells_d_.append(self.dy_)
        else:
            self.dy_ = np.ones(n_max, dtype="int") * dy
            self.cells_d_.append(dy)

        if "z" in self.fdir:
            check_d(dz, nz, "z")
            self.dz_ = np.ones(nz, dtype="int") * dz
            self.cells_d_.append(self.dz_)
        else:
            self.dz_ = np.ones(n_max, dtype="int") * dz
            self.cells_d_.append(dz)

        if self.verbose:
            print(f"[info] axes vectors (dx_, dy_, dz_) were computed.")

        return self.cells_d_

    def __calc_cells_d(
        self,
        dx,
        dy,
        dz,
        fshape: bool = False,
    ):
        """Calculates dimensional meshgrid in x,y,z directions.

        This method takes dx, dy, and dz as scalers or iterables and use
        them to construct dimensional meshgrid based on axes vectors in
        x,y,z provided by __calc_cells_d() method. Please note that dx_,
        dy_, dz_ refer to axes vectors while dx, dy, dz refer to
        meshgrid arrays.

        Parameters
        ----------
        dx : int, float, array-like
            grid dimension in x-direction. In case of a list or array,
            the length should be equal to nx+2 for all cells including
            boundary cells. Vales should be in natural order (i.e. from
            left to right).
        dy : int, float, array-like
            grid dimension in y-direction. In case of a list or array,
            the length should be equal to ny+2 for all cells including
            boundary cells. Vales should be in natural order (i.g. from
            front to back).
        dz : int, float, array-like
            grid dimension in z-direction. In case of a list or array,
            the length should be equal to nz+2 for all cells including
            boundary cells. Vales should be in natural order (i.g. from
            down to up).
        fshape : bool, optional
            reshape to flow shape instead of flatten. If set to
            True, fmt argument will be ignored.

        Returns
        -------
        tuple
            tuple of len 3 for dimension meshgrid as Dx, Dy, Dz.

        """
        # ToDo
        # ----
        # - Do we need any fmt here?
        if fshape:
            shape = self.get_fshape(True, False)
        else:
            shape = self.get_n(True)

        cells_d_ = self.__calc_cells_d_(dx, dy, dz)

        self.dx, self.dy, self.dz = np.meshgrid(*cells_d_, copy=False)
        self.dx = np.transpose(self.dx, axes=(0, 2, 1)).reshape(shape)
        self.dy = np.transpose(self.dy, axes=(2, 0, 1)).reshape(shape)
        self.dz = np.transpose(self.dz, axes=(2, 1, 0)).reshape(shape)

        if self.verbose:
            print(f"[info] axes meshgrid (Dx, Dy, Dz) were computed.")

        self.d["x"] = self.dx
        self.d["y"] = self.dy
        self.d["z"] = self.dz

        return (self.dx, self.dy, self.dz)

    @_lru_cache(maxsize=None)
    def get_cells_d(
        self,
        dir,
        boundary: bool = True,
        fshape: bool = False,
    ):
        """Returns cells dimensional meshgrid.

        Parameters
        ----------
        dir : str
            direction str in ['x', 'y', 'z'].
        boundary : bool, optional
            include boundary cells.
        fshape : bool, optional
            reshape to flow shape instead of flatten.

        Returns
        -------
        ndarray
            array of dx, dy, or dz based on dir argument.

        """
        # ToDo
        # ----
        # - Allow dict for all directions.

        if dir == "x":
            cells_d = self.dx
        elif dir == "y":
            cells_d = self.dy
        elif dir == "z":
            cells_d = self.dz
        elif dir in ["-", "all", "dict"]:
            return {"x": self.dx, "y": self.dy, "z": self.dz}
        else:
            raise ValueError("dir argument must be in ['x', 'y', 'z'].")

        if not boundary:
            cells_d = cells_d[self.cells_id]

        if fshape:
            shape = self.get_fshape(boundary, False)
            cells_d = cells_d.reshape(shape)

        if self.verbose:
            print(f"[info] d{dir} was exported.")

        return cells_d

    def get_cells_dx(
        self,
        boundary: bool = True,
        fshape: bool = False,
    ):
        """Returns cells dx.

        Parameters
        ----------
        boundary : bool, optional
            include boundary cells.
        fshape : bool, optional
            reshape to flow shape instead of flatten.

        Returns
        -------
        ndarray
            array of dx.
        """
        return self.get_cells_d("x", boundary, fshape)

    def get_cells_dy(
        self,
        boundary: bool = True,
        fshape: bool = False,
    ):
        """Returns cells dy.

        Parameters
        ----------
        boundary : bool, optional
            include boundary cells.
        fshape : bool, optional
            reshape to flow shape instead of flatten.

        Returns
        -------
        ndarray
            array of dy.
        """
        return self.get_cells_d("y", boundary, fshape)

    def get_cells_dz(
        self,
        boundary: bool = True,
        fshape: bool = False,
    ):
        """Returns cells dz.

        Parameters
        ----------
        boundary : bool, optional
            include boundary cells.
        fshape : bool, optional
            reshape to flow shape instead of flatten.

        Returns
        -------
        ndarray
            array of dz.
        """
        return self.get_cells_d("z", boundary, fshape)

    @_lru_cache(maxsize=None)
    def get_cell_d(
        self,
        dir,
        id=None,
        coords=None,
    ):
        """Returns cell d.

        Parameters
        ----------
        dir : str
            direction str in ['x', 'y', 'z'].
        id : int, iterable of int
            cell id based on natural order as int. For multiple cells,
            list of int [id,id,..] or tuple of int (id,id,...).
            NotFullyImplemented.
        coords : iterable of int, iterable of tuples of int, by default
            None cell coordinates (i,j,k) as a tuple of int. For
            multiple cells, tuple of tuples of int as
            ((i,j,k),(i,j,k),..). NotFullyImplemented.

        Returns
        -------
        float
            cell d.

        Raises
        ------
        ValueError
            id or coords argument must be defined.

        """
        # ToDo
        # ----
        # - check if id or coords in range.
        cells_D = self.get_cells_d(dir=dir, boundary=True, fshape=True)

        if id is not None:
            return cells_D.flatten()[id]
        elif coords is not None:
            icoords = self.get_cell_icoords(coords)
            return cells_D[icoords]
        else:
            raise ValueError("id or coords argument must be defined.")

    def get_cell_dx(
        self,
        id=None,
        coords=None,
    ):
        """Returns cell dx.

        Parameters
        ----------
        id : int, iterable of int
            cell id based on natural order as int. For multiple cells,
            list of int [id,id,..] or tuple of int (id,id,...).
            NotFullyImplemented.
        coords : iterable of int, iterable of tuples of int, by default
            None cell coordinates (i,j,k) as a tuple of int. For
            multiple cells, tuple of tuples of int as
            ((i,j,k),(i,j,k),..). NotFullyImplemented.

        Returns
        -------
        float
            cell dx.

        Raises
        ------
        ValueError
            id or coords argument must be defined.
        """
        return self.get_cell_d("x", id, coords)

    def get_cell_dy(
        self,
        id=None,
        coords=None,
    ):
        """Returns cell dy.

        Parameters
        ----------
        id : int, iterable of int
            cell id based on natural order as int. For multiple cells,
            list of int [id,id,..] or tuple of int (id,id,...).
            NotFullyImplemented.
        coords : iterable of int, iterable of tuples of int, by default
            None cell coordinates (i,j,k) as a tuple of int. For
            multiple cells, tuple of tuples of int as
            ((i,j,k),(i,j,k),..). NotFullyImplemented.

        Returns
        -------
        float
            cell dy.

        Raises
        ------
        ValueError
            id or coords argument must be defined.
        """
        return self.get_cell_d("y", id, coords)

    def get_cell_dz(
        self,
        id=None,
        coords=None,
    ):
        """Returns cell dz.

        Parameters
        ----------
        id : int, iterable of int
            cell id based on natural order as int. For multiple cells,
            list of int [id,id,..] or tuple of int (id,id,...).
            NotFullyImplemented.
        coords : iterable of int, iterable of tuples of int, by default
            None cell coordinates (i,j,k) as a tuple of int. For
            multiple cells, tuple of tuples of int as
            ((i,j,k),(i,j,k),..). NotFullyImplemented.

        Returns
        -------
        float
            cell dz.

        Raises
        ------
        ValueError
            id or coords argument must be defined.
        """
        return self.get_cell_d("z", id, coords)

    # -------------------------------------------------------------------------
    # Area:
    # -------------------------------------------------------------------------

    def __calc_cells_A(self):
        self.Ax = self.A["x"] = self.dy * self.dz
        self.Ay = self.A["y"] = self.dx * self.dz
        self.Az = self.A["z"] = self.dx * self.dy

    @_lru_cache(maxsize=None)
    def get_cells_A(
        self,
        dir,
        boundary: bool = True,
        fshape: bool = True,
    ):
        """Returns cells cross-sectional area A.

        Parameters
        ----------
        dir : str
            direction str in ['x', 'y', 'z'].
        boundary : bool, optional
            include boundary cells.
        fshape : bool, optional
            reshape to flow shape instead of flatten.

        Returns
        -------
        ndarray
            array of Ax, Ay, or Az based on dir argument.

        """
        # ToDo
        # ----
        # - Allow dict for all directions.
        if dir == "x":
            cells_A = self.Ax
        elif dir == "y":
            cells_A = self.Ay
        elif dir == "z":
            cells_A = self.Az
        elif dir in ["-", "all", "dict"]:
            return {"x": self.Ax, "y": self.Ay, "z": self.Az}
        else:
            raise ValueError("dir argument must be in ['x', 'y', 'z'].")

        if not boundary:
            cells_A = cells_A[self.cells_id]

        if fshape:
            shape = self.get_fshape(boundary, False)
            cells_A = cells_A.reshape(shape)

        if self.verbose:
            print(f"[info] A{dir} was exported.")

        return cells_A

    def get_cells_Ax(
        self,
        boundary: bool = True,
        fshape: bool = True,
    ):
        """Returns cells cross-sectional area Ax.

        Parameters
        ----------
        boundary : bool, optional
            include boundary cells.
        fshape : bool, optional
            reshape to flow shape instead of flatten.

        Returns
        -------
        ndarray
            array of Ax.
        """
        return self.get_cells_A("x", boundary, fshape)

    def get_cells_Ay(
        self,
        boundary: bool = True,
        fshape: bool = True,
    ):
        """Returns cells cross-sectional area Ay.

        Parameters
        ----------
        boundary : bool, optional
            include boundary cells.
        fshape : bool, optional
            reshape to flow shape instead of flatten.

        Returns
        -------
        ndarray
            array of Ay
        """
        return self.get_cells_A("y", boundary, fshape)

    def get_cells_Az(
        self,
        boundary: bool = True,
        fshape: bool = True,
    ):
        """Returns cells cross-sectional area Az.

        Parameters
        ----------
        boundary : bool, optional
            include boundary cells.
        fshape : bool, optional
            reshape to flow shape instead of flatten.

        Returns
        -------
        ndarray
            array of Az.
        """
        return self.get_cells_A("z", boundary, fshape)

    @_lru_cache(maxsize=None)
    def get_cell_A(
        self,
        dir,
        id=None,
        coords=None,
    ):
        """Returns cell cross-sectional area A.

        Parameters
        ----------
        dir : str
            direction str in ['x', 'y', 'z'].
        id : int, iterable of int
            cell id based on natural order as int. For multiple cells,
            list of int [id,id,..] or tuple of int (id,id,...).
            NotFullyImplemented.
        coords : iterable of int, iterable of tuples of int, by default
            None cell coordinates (i,j,k) as a tuple of int. For
            multiple cells, tuple of tuples of int as
            ((i,j,k),(i,j,k),..). NotFullyImplemented.

        Returns
        -------
        int, float
            scaler of A based on dir argument.

        Raises
        ------
        ValueError
            id or coords argument must be defined.
        """
        if id is not None:
            cells_A = self.get_cells_A(dir, True, False)
            return cells_A[id]
        elif coords is not None:
            cells_A = self.get_cells_A(dir, True, True)
            icoords = self.get_cell_icoords(coords)
            return cells_A[icoords]
        else:
            raise ValueError("id or coords argument must be defined.")

    def get_cell_Ax(
        self,
        id=None,
        coords=None,
    ):
        """Returns cell cross-sectional area Ax.

        Parameters
        ----------
        id : int, iterable of int
            cell id based on natural order as int. For multiple cells,
            list of int [id,id,..] or tuple of int (id,id,...).
            NotFullyImplemented.
        coords : iterable of int, iterable of tuples of int, by default
            None cell coordinates (i,j,k) as a tuple of int. For
            multiple cells, tuple of tuples of int as
            ((i,j,k),(i,j,k),..). NotFullyImplemented.

        Returns
        -------
        int, float
            scaler of Ax.

        Raises
        ------
        ValueError
            id or coords argument must be defined.
        """
        return self.get_cell_A("x", id, coords)

    def get_cell_Ay(
        self,
        id=None,
        coords=None,
    ):
        """Returns cell cross-sectional area Ay.

        Parameters
        ----------
        id : int, iterable of int
            cell id based on natural order as int. For multiple cells,
            list of int [id,id,..] or tuple of int (id,id,...).
            NotFullyImplemented.
        coords : iterable of int, iterable of tuples of int, by default
            None cell coordinates (i,j,k) as a tuple of int. For
            multiple cells, tuple of tuples of int as
            ((i,j,k),(i,j,k),..). NotFullyImplemented.

        Returns
        -------
        int, float
            scaler of Ay.

        Raises
        ------
        ValueError
            id or coords argument must be defined.
        """
        return self.get_cell_A("y", id, coords)

    def get_cell_Az(
        self,
        id=None,
        coords=None,
    ):
        """Returns cell cross-sectional area Az.

        Parameters
        ----------
        id : int, iterable of int
            cell id based on natural order as int. For multiple cells,
            list of int [id,id,..] or tuple of int (id,id,...).
            NotFullyImplemented.
        coords : iterable of int, iterable of tuples of int, by default
            None cell coordinates (i,j,k) as a tuple of int. For
            multiple cells, tuple of tuples of int as
            ((i,j,k),(i,j,k),..). NotFullyImplemented.

        Returns
        -------
        int, float
            scaler of Az.

        Raises
        ------
        ValueError
            id or coords argument must be defined.
        """
        return self.get_cell_A("z", id, coords)

    # -------------------------------------------------------------------------
    # Volume:
    # -------------------------------------------------------------------------

    def __calc_cells_V(self):
        self.V = self.dx * self.dy * self.dz
        self.Vt = self.V.sum()

    @_lru_cache(maxsize=2)
    def get_Vt(
        self,
        boundary: bool = True,
        pyvista=False,
    ):
        """Returns total grid volume Vt.

        Parameters
        ----------
        boundary : bool, optional
            include boundary cells.
        pyvista : bool, optional
            use built-in pyvista calculations.

        Returns
        -------
        int, float
            total grid volume Vt.
        """
        if pyvista:
            return self.get_pyvista_grid(boundary).volume
        else:
            if boundary:
                return self.Vt
            else:
                return self.remove_boundaries(self.V, False, "both").sum()

    @_lru_cache(maxsize=4)
    def get_cells_V(
        self,
        boundary: bool = True,
        fshape: bool = False,
        pyvista=False,
    ):
        """Returns cells volume V.

        Parameters
        ----------
        boundary : bool, optional
            include boundary cells.
        fshape : bool, optional
            reshape to flow shape instead of flatten.
        pyvista : bool, optional
            use built-in pyvista calculations.

        Returns
        -------
        ndarray
            array of volume V.
        """
        if pyvista:
            pyvista_grid = self.get_pyvista_grid(True)
            cells_V = pyvista_grid.compute_cell_sizes()["Volume"]
        else:
            cells_V = self.V

        if not boundary:
            cells_V = cells_V[self.cells_id]

        if fshape:
            shape = self.get_fshape(boundary, False)
            cells_V = cells_V.reshape(shape)

        if self.verbose:
            print("[info] V was computed.")

        return cells_V

    @_lru_cache(maxsize=None)
    def get_cell_V(
        self,
        id=None,
        coords=None,
    ):
        """Returns cell volume V.

        Parameters
        ----------
        id : int, iterable of int
            cell id based on natural order as int. For multiple cells,
            list of int [id,id,..] or tuple of int (id,id,...).
            NotFullyImplemented.
        coords : iterable of int, iterable of tuples of int, by default
            None cell coordinates (i,j,k) as a tuple of int. For
            multiple cells, tuple of tuples of int as
            ((i,j,k),(i,j,k),..). NotFullyImplemented.

        Returns
        -------
        int, float
            scaler of V.

        Raises
        ------
        ValueError
            id or coords argument must be defined.
        """
        if id is not None:
            cells_V = self.get_cells_V(True, False, False)
            return cells_V[id]
        elif coords is not None:
            cells_V = self.get_cells_V(True, True, False)
            icoords = self.get_cell_icoords(coords)
            return cells_V[icoords]
        else:
            raise ValueError("id or coords argument must be defined.")

    # -------------------------------------------------------------------------
    # Centers:
    # -------------------------------------------------------------------------

    @_lru_cache(maxsize=4)
    def get_cells_center(
        self,
        boundary: bool = True,
        fshape: bool = False,
        pyvista=False,
    ):
        """Returns cells center.

        Parameters
        ----------
        boundary : bool, optional
            include boundary cells.
        fshape : bool, optional
            reshape to flow shape instead of flatten.
        pyvista : bool, optional
            use built-in pyvista calculations.

        Returns
        -------
        ndarray
            cells center array.
        """
        if pyvista:
            pyvista_grid = self.get_pyvista_grid(True)
            cells_center = pyvista_grid.cell_centers().points
        else:

            def calc_d_center(d_, n_b):
                d = d_ / 2
                d[1:] = d[1:] + d_[:-1].cumsum()
                return d[:n_b]

            dxx = calc_d_center(self.dx_, self.nx_b)
            dyy = calc_d_center(self.dy_, self.ny_b)
            dzz = calc_d_center(self.dz_, self.nz_b)
            cells_center = np.meshgrid(dxx, dyy, dzz)
            cells_center = np.transpose(cells_center, axes=(1, 3, 2, 0))
            # cells_center = [a.reshape(-1, 1) for a in cells_center]
            cells_center = np.concatenate(cells_center, axis=1).reshape(-1, 3)

        if not boundary:
            cells_center = cells_center[self.cells_id]

        if fshape:
            shape = self.get_fshape(boundary, True)
            cells_center = cells_center.reshape(shape)

        if self.verbose:
            print(f"[info] center was computed.")

        return cells_center

    @_lru_cache(maxsize=None)
    def get_cell_center(
        self,
        id=None,
        coords=None,
    ):
        """Returns cell center.

        Parameters
        ----------
        id : int, iterable of int
            cell id based on natural order as int. For multiple cells,
            list of int [id,id,..] or tuple of int (id,id,...).
            NotFullyImplemented.
        coords : iterable of int, iterable of tuples of int, by default
            None cell coordinates (i,j,k) as a tuple of int. For
            multiple cells, tuple of tuples of int as
            ((i,j,k),(i,j,k),..). NotFullyImplemented.

        Returns
        -------
        int, float
            array of cell center.

        Raises
        ------
        ValueError
            id or coords argument must be defined.
        """
        if id is not None:
            cells_centers = self.get_cells_center(True, False, False)
            return cells_centers[id]
        elif coords is not None:
            cells_centers = self.get_cells_center(True, True, False)
            icoords = self.get_cell_icoords(coords)
            return cells_centers[icoords]
        else:
            raise ValueError("id or coords argument must be defined.")

    # -------------------------------------------------------------------------
    # Pyvista:
    # -------------------------------------------------------------------------

    # @_lru_cache(maxsize=2)
    def get_pyvista_grid(self, boundary: bool = True):
        """Returns pyvista ExplicitStructuredGrid object.

        Parameters
        ----------
        boundary : bool, optional
            include boundary cells.

        Returns
        -------
        ExplicitStructuredGrid
            pyvista gird object.

        References
        ----------
        - pyvista: `ExplicitStructuredGrid <https://docs.pyvista.org/api/core/_autosummary/pyvista.ExplicitStructuredGrid.html>`_.
        """
        shape = np.array(self.get_shape(boundary)) + 1
        corners = self.get_corners(boundary)
        grid_pv = pv.ExplicitStructuredGrid(shape, corners)

        if self.verbose:
            s = utils.helpers.get_boundary_str(boundary)
            print(f"[info] grid_pv {s} was created.")

        return grid_pv

    @_lru_cache(maxsize=2)
    def get_corners(self, boundary: bool = True):
        """Returns corners required to create pyvista grid.

        Parameters
        ----------
        boundary : bool, optional
            include boundary cells.

        Returns
        -------
        ndarray
            corners as an array.

        References
        ----------
        - pyvista: `Creating an Explicit Structured Grid <https://docs.pyvista.org/examples/00-load/create-explicit-structured-grid.html>`_.
        """

        if "x" in self.fdir:
            xcorn = np.insert(self.dx_.cumsum(), 0, 0)
        else:
            xcorn = np.arange(0, (self.nx + 1) * self.dx_[0], self.dx_[0])

        if "y" in self.fdir:
            ycorn = np.insert(self.dy_.cumsum(), 0, 0)
        else:
            ycorn = np.arange(0, (self.ny + 1) * self.dy_[0], self.dy_[0])

        if "z" in self.fdir:
            zcorn = np.insert(self.dz_.cumsum(), 0, 0)
        else:
            zcorn = np.arange(0, (self.nz + 1) * self.dz_[0], self.dz_[0])

        # Boundary:
        if boundary:
            ix = 2 if "x" in self.fdir else 0
            iy = 2 if "y" in self.fdir else 0
            iz = 2 if "z" in self.fdir else 0
        else:
            ix = 0
            iy = 0
            iz = 0
            if "x" in self.fdir:
                xcorn = xcorn[1:-1]
            if "y" in self.fdir:
                ycorn = ycorn[1:-1]
            if "z" in self.fdir:
                zcorn = zcorn[1:-1]

        # X corners:
        xcorn = np.repeat(xcorn, 2)
        xcorn = xcorn[1:-1]
        xcorn = np.tile(xcorn, 4 * (self.ny + iy) * (self.nz + iz))

        # Y corners:
        ycorn = np.repeat(ycorn, 2)
        ycorn = ycorn[1:-1]
        ycorn = np.tile(ycorn, (2 * (self.nx + ix), 2 * (self.nz + iz)))
        ycorn = np.transpose(ycorn)
        ycorn = ycorn.flatten()

        # Z corners:
        zcorn = np.repeat(zcorn, 2)
        zcorn = zcorn[1:-1]
        zcorn = np.repeat(zcorn, 4 * (self.nx + ix) * (self.ny + iy))

        if self.verbose:
            s = utils.helpers.get_boundary_str(boundary)
            print(f"[info] corners {s} were calculated.")
            print(
                "    - xcorn shape:",
                xcorn.shape,
                "- ycorn shape:",
                ycorn.shape,
                "- zcorn shape:",
                zcorn.shape,
            )

        # Combine corners:
        corners = np.stack((xcorn, ycorn, zcorn))
        corners = corners.transpose()

        return corners

    # -------------------------------------------------------------------------
    # Properties:
    # -------------------------------------------------------------------------

    def set_props(
        self,
        kx=None,
        ky=None,
        kz=None,
        phi=None,
        z=None,
        comp=None,
        id=None,
        coords=None,
    ):
        """Set properties for all cells or a selected cell.

        This method is used to set or change properties. If neither id
        nor coords are defined, the same value will be assigned to all
        cells including boundary cells.

        Parameters
        ----------
        kx : int, float, array-like, optional
            permeability in x-direction (relevant only if 'x' was in
            fluid flow direction). In case of a list or array,
            the length should be equal to nx+2 for all cells including
            boundary cells. Vales should be in natural order (i.g. from
            left to right).
        ky : int, float, array-like, optional
            permeability in y-direction (relevant only if 'y' was in
            fluid flow direction). In case of a list or array,
            the length should be equal to ny+2 for all cells including
            boundary cells. Vales should be in natural order (i.g.from
            front to back).
        kz : int, float, array-like, optional
            permeability in z-direction (relevant only if 'z' was in
            fluid flow direction). In case of a list or array,
            the length should be equal to nz+2 for all cells including
            boundary cells. Vales should be in natural order (i.g. from
            down to up).
        phi : float, array-like, optional
            porosity. In case of an array, the shape should be equal to
            grid.shape with boundaries. Vales should be in natural
            order.
        z : int, float, array-like, optional
            depth of grid tops (NOT FULLY IMPLEMENTED).
        comp : float, optional
            compressibility.
        id : int, iterable of int
            cell id based on natural order as int. For multiple cells,
            list of int [id,id,..] or tuple of int (id,id,...).
            NotFullyImplemented.
        coords : iterable of int, iterable of tuples of int, by default
            None cell coordinates (i,j,k) as a tuple of int. For
            multiple cells, tuple of tuples of int as
            ((i,j,k),(i,j,k),..). NotFullyImplemented.

        """
        # ToDo
        # ----
        # - allow iterables for id and coords.
        if kx is not None:
            self.set_prop("kx", kx, id, coords)
            self.kx = self.k["x"] = self.__props__["kx"]
        if ky is not None:
            self.set_prop("ky", ky, id, coords)
            self.ky = self.k["y"] = self.__props__["ky"]
        if kz is not None:
            self.set_prop("kz", kz, id, coords)
            self.kz = self.k["z"] = self.__props__["kz"]
        if phi is not None:
            self.set_prop("phi", phi, id, coords)
            self.phi = self.__props__["phi"]
        if z is not None:
            self.set_prop("z", z, id, coords)
            self.z = self.__props__["z"]
        if comp is not None:
            self.set_comp(comp)
        if self.__props__["z"] is None:
            self.set_prop("z", 0)
            self.z = self.__props__["z"]
        if not hasattr(self, "comp"):
            self.set_comp(0)

    def set_cell_value(
        self,
        array,
        value,
        id=None,
        coords=None,
    ):
        if id is not None:
            coords = self.get_cell_coords(id, True)
            # prop = self.props[name].flatten()
            # prop[id] = value
            # fshape = self.get_fshape(True, False)
            # self.props[name] = prop.reshape(fshape)
            # s = "cell id " + str(id)
        if coords is not None:
            icoords = self.get_cell_icoords(coords)
            array[icoords] = value

    def set_prop(
        self,
        name,
        value,
        id=None,
        coords=None,
    ):
        """Set a property in all cells or a selected cell.

        This method is used to populate properties values based on grid
        shape. By default, values are populated in a flatten array which
        can then be reshaped based on fshape.

        Parameters
        ----------
        name : str
            property name as a string from props attribute keys.
        value : int, float, array-like
            property value. In case of an array, the shape should be
            equal to grid.shape with boundaries. Vales should be in
            natural order.
        id : int, iterable of int
            cell id based on natural order as int. For multiple cells,
            list of int [id,id,..] or tuple of int (id,id,...). If None,
            then all cells are selected. NotFullyImplemented.
        coords : iterable of int, iterable of tuples of int, by default
            None cell coordinates (i,j,k) as a tuple of int. For
            multiple cells, tuple of tuples of int as
            ((i,j,k),(i,j,k),..). If None, then all cells are selected.
            NotFullyImplemented.

        Raises
        ------
        ValueError
            Property name is unknown or not defined.

        """
        # ToDo
        # ----
        # - allow iterables for id and coords.
        # - check for id or coords inside grid.
        # - make get_ones(#, False, #) > with flatt as default.

        # Backup
        # ------
        # - Code for id part:
        #     prop = self.props[name].flatten()
        #     prop[id] = value
        #     fshape = self.get_fshape(True, False)
        #     self.props[name] = prop.reshape(fshape)
        #     s = "cell id " + str(id)
        if name in self.__props__.keys():
            if id is None and coords is None:
                self.__props__[name] = self.get_ones(True, False, False) * value
                s = "all cells"
            else:
                if id is not None:
                    coords = self.get_cell_coords(id, True)
                if coords is not None:
                    icoords = self.get_cell_icoords(coords)
                    self.__props__[name][icoords] = value
                    s = "cell coords " + str(coords)
        else:
            msg = (
                f"Property {name} is unknown or not defined. "
                f"Known properties are: {list(self.__props__.keys())}."
            )
            raise ValueError(msg)

        if self.verbose:
            print(f"[info] {name} is {value} for {s}.")

    def get_prop(
        self,
        name,
        boundary: bool = True,
        fshape: bool = True,
        fmt="array",
    ):
        """Get property values in all cells.

        Parameters
        ----------
        name : str
            property name as a string from props attribute keys.
        boundary : bool, optional
            include boundary cells.
        fshape : bool, optional
            reshape to flow shape instead of flatten. If set to
            True, fmt argument will be ignored.
        fmt : str, optional
            output format as str from ['array', 'list', 'tuple', 'set'].
            This argument is ignored if fshape argument is set to True.
            For a better performance, use 'set' to check if an item is
            in a list or not. Use tuples to iterate through items. When
            option 'array' is used, utils.helpers.isin() must be used to check
            if a tuple of 3 is in the array.


        Raises
        ------
        ValueError
            Property name is unknown or not defined.

        """
        # ToDo
        # ----
        # - flatten when fmt not array and in fshape.
        if name in self.__props__.keys() and self.__props__[name] is not None:
            prop = self.__props__[name]

            if not boundary:
                prop = prop[self.cells_id]

            if fshape:
                shape = self.get_fshape(boundary, False)
                prop = prop.reshape(shape)

            return utils.helpers.reformat(prop, fmt)

        else:
            msg = (
                f"Property {name} is not defined. "
                # f"Known properties are: {list(self.__props__.keys())}."
            )
            raise ValueError(msg)

    def get_cells_k(
        self,
        dir,
        boundary: bool = True,
        fshape: bool = True,
        fmt="array",
    ):
        """Returns permeability values for all cells.

        Parameters
        ----------
        name : str
            property name as a string from props attribute keys.
        boundary : bool, optional
            include boundary cells.
        fshape : bool, optional
            reshape to flow shape instead of flatten. If set to
            True, fmt argument will be ignored.
        fmt : str, optional
            output format as str from ['array', 'list', 'tuple', 'set'].
            This argument is ignored if fshape argument is set to True.
            For a better performance, use 'set' to check if an item is
            in a list or not. Use tuples to iterate through items. When
            option 'array' is used, utils.helpers.isin() must be used to check
            if a tuple of 3 is in the array.


        Raises
        ------
        ValueError
            dir must be in ['x', 'y', 'z'].

        """
        # ToDo
        # ----
        # - flatten when fmt not array and in fshape.
        if dir in ["x", "y", "z"]:
            name = "k" + dir
        else:
            raise ValueError("dir must be in ['x', 'y', 'z'].")

        return self.get_prop(name, boundary, fshape, fmt)

    @_lru_cache(maxsize=None)
    def get_cell_k(
        self,
        dir,
        id=None,
        coords=None,
    ):
        """Returns cell permeability.

        Parameters
        ----------
        dir : str
            direction str in ['x', 'y', 'z'].
        id : int, iterable of int
            cell id based on natural order as int. For multiple cells,
            list of int [id,id,..] or tuple of int (id,id,...).
            NotFullyImplemented.
        coords : iterable of int, iterable of tuples of int, by default
            None cell coordinates (i,j,k) as a tuple of int. For
            multiple cells, tuple of tuples of int as
            ((i,j,k),(i,j,k),..). NotFullyImplemented.

        Returns
        -------
        int, float
            scaler of k based on dir argument.

        Raises
        ------
        ValueError
            id or coords argument must be defined.
        """
        if id is not None:
            cells_k = self.get_cells_k(dir, True, False)
            return cells_k[id]
        elif coords is not None:
            cells_k = self.get_cells_k(dir, True, True)
            icoords = self.get_cell_icoords(coords)
            return cells_k[icoords]
        else:
            raise ValueError("id or coords argument must be defined.")

    def get_cell_kx(
        self,
        id=None,
        coords=None,
    ):
        """Returns cell permeability at x direction.

        Parameters
        ----------
        id : int, iterable of int
            cell id based on natural order as int. For multiple cells,
            list of int [id,id,..] or tuple of int (id,id,...).
            NotFullyImplemented.
        coords : iterable of int, iterable of tuples of int, by default
            None cell coordinates (i,j,k) as a tuple of int. For
            multiple cells, tuple of tuples of int as
            ((i,j,k),(i,j,k),..). NotFullyImplemented.

        Returns
        -------
        int, float
            scaler of kx.

        Raises
        ------
        ValueError
            id or coords argument must be defined.
        """
        return self.get_cell_k("x", id, coords)

    def get_cell_ky(
        self,
        id=None,
        coords=None,
    ):
        """Returns cell permeability at y direction.

        Parameters
        ----------
        id : int, iterable of int
            cell id based on natural order as int. For multiple cells,
            list of int [id,id,..] or tuple of int (id,id,...).
            NotFullyImplemented.
        coords : iterable of int, iterable of tuples of int, by default
            None cell coordinates (i,j,k) as a tuple of int. For
            multiple cells, tuple of tuples of int as
            ((i,j,k),(i,j,k),..). NotFullyImplemented.

        Returns
        -------
        int, float
            scaler of ky.

        Raises
        ------
        ValueError
            id or coords argument must be defined.
        """
        return self.get_cell_k("y", id, coords)

    def get_cell_kz(
        self,
        id=None,
        coords=None,
    ):
        """Returns cell permeability at z direction.

        Parameters
        ----------
        id : int, iterable of int
            cell id based on natural order as int. For multiple cells,
            list of int [id,id,..] or tuple of int (id,id,...).
            NotFullyImplemented.
        coords : iterable of int, iterable of tuples of int, by default
            None cell coordinates (i,j,k) as a tuple of int. For
            multiple cells, tuple of tuples of int as
            ((i,j,k),(i,j,k),..). NotFullyImplemented.

        Returns
        -------
        int, float
            scaler of kz.

        Raises
        ------
        ValueError
            id or coords argument must be defined.
        """
        return self.get_cell_k("z", id, coords)

    @property
    @_lru_cache(maxsize=1)
    def is_homogeneous(self):
        """Returns homogeneity as bool.

        This property checks if the porosity (phi) is the same across
        all grids.

        Returns
        -------
        bool
            True if homogeneous, otherwise False.
        """
        props = ["phi"]
        props = [name for name in props if self.__props__[name] is not None]
        for name in props:
            prop = self.get_prop(name, False, False)
            if not np.all(prop == prop[0]):
                return False
        return True

    @property
    @_lru_cache(maxsize=1)
    def is_heterogeneous(self):
        """Returns heterogeneity as bool.

        This property checks if the porosity (phi) is not the same
        across all grids.

        Returns
        -------
        bool
            True if heterogeneous, otherwise False.
        """
        return not self.is_homogeneous

    @property
    @_lru_cache(maxsize=1)
    def is_isotropic(self):
        """Returns isotropic as bool.

        This property checks if kx, ky, and kz are the same across all
        grids. In other words, `all(kx == kx[0])`, `all(ky == ky[0])`,
        and `all(kz == kz[0])`. However, other isotropic conventions
        where `kx = ky = kz` either across all cells or in single cells
        are still not used.

        Returns
        -------
        bool
            True if isotropic, otherwise False.
        """
        props = ["kx", "ky", "kz"]
        props = [name for name in props if self.__props__[name] is not None]
        for name in props:
            prop = self.get_prop(name, False, False)
            if not np.all(prop == prop[0]):
                return False
        return True

    @property
    @_lru_cache(maxsize=1)
    def is_anisotropic(self):
        """Returns anisotropic as bool.

        This property checks if kx, ky, and kz are not the same across
        all grids.

        Returns
        -------
        bool
            True if anisotropic, otherwise False.
        """
        return not self.is_isotropic

    @property
    @_lru_cache(maxsize=1)
    def is_regular(self):
        """Returns regularity as bool.

        This property checks if dx, dy, and dz are the same across all
        grids.

        Returns
        -------
        bool
            True if regular, otherwise False.
        """
        props = ["x", "y", "z"]
        for name in props:
            prop = self.get_cells_d(name, False, False)
            if not np.all(prop == prop[0]):
                return False
        return True

    @property
    @_lru_cache(maxsize=1)
    def is_irregular(self):
        """Returns irregularity as bool.

        This property checks if dx, dy, and dz are the same across all
        grids.

        Returns
        -------
        bool
            True if irregular, otherwise False.
        """
        return not self.is_regular

    # -------------------------------------------------------------------------
    # Geometry Factor:
    # -------------------------------------------------------------------------

    def get_cells_G_diag_1(self, boundary: bool = False):
        if self.D == 1:
            dir = self.fdir
        else:
            dir = self.fdir[0]
        k = self.get_cells_k(dir, boundary, False, "array")
        A = self.get_cells_A(dir, boundary, False)
        d = self.get_cells_d(dir, boundary, False)

        if self.is_isotropic and self.is_regular:
            diag_1 = (
                self.factors["transmissibility conversion"]
                * ((k[:-1] + k[1:]) / 2)
                * ((A[:-1] + A[1:]) / 2)
                / ((d[:-1] + d[1:]) / 2)
            )
        else:
            diag_1 = (
                2
                * self.factors["transmissibility conversion"]
                / ((d[:-1] / (A[:-1] * k[:-1])) + (d[1:] / (A[1:] * k[1:])))
            )
        return diag_1

    def get_cells_G_diag_2(
        self,
        boundary: bool = False,
        diag_1=None,
    ):
        assert self.D >= 2, "diag_2 is possible only when D>=2"
        n = self.get_n(boundary)
        dir = self.fdir[1]
        if self.fdir[0] == "x":
            if boundary:
                n2 = self.nx_b
            else:
                n2 = self.nx
        elif self.fdir[0] == "y":
            if boundary:
                n2 = self.ny_b
            else:
                n2 = self.ny
        n2_ = n - n2
        if diag_1 is not None:
            diag_1[n2 - 1 :: n2] = 0
        k = self.get_cells_k(dir, boundary, False, "array")
        A = self.get_cells_A(dir, boundary, False)
        d = self.get_cells_d(dir, boundary, False)

        if self.is_isotropic and self.is_regular:
            diag_2 = (
                self.factors["transmissibility conversion"]
                * ((k[:n2_] + k[n2:]) / 2)
                * ((A[:n2_] + A[n2:]) / 2)
                / ((d[:n2_] + d[n2:]) / 2)
            )
        else:
            diag_2 = (
                2
                * self.factors["transmissibility conversion"]
                / ((d[:n2_] / (A[:n2_] * k[:n2_])) + (d[n2:] / (A[n2:] * k[n2:])))
            )
        return diag_2, n2

    def get_cells_G_diag_3(
        self,
        boundary: bool = False,
        diag_2=None,
    ):
        assert self.D == 3, "diag_3 is possible only when D==3"
        dir = self.fdir[-1]
        if boundary:
            n3 = self.nx_b * self.ny_b
            n3_ = n3 - self.nx_b
            n4 = n3 * self.nz_b - n3
            diag_2_zero_ids = n3_ + np.arange(0, self.nx_b, n3)
        else:
            n3 = self.nx * self.ny
            n3_ = n3 - self.nx
            n4 = n3 * self.nz - n3
            diag_2_zero_ids = n3_ + np.arange(0, self.nx, n3)
        if diag_2 is not None:
            diag_2[diag_2_zero_ids] = 0
        k = self.get_cells_k(dir, boundary, False, "array")
        A = self.get_cells_A(dir, boundary, False)
        d = self.get_cells_d(dir, boundary, False)

        if self.is_isotropic and self.is_regular:
            diag_3 = (
                self.factors["transmissibility conversion"]
                * ((k[:n4] + k[n3:]) / 2)
                * ((A[:n4] + A[n3:]) / 2)
                / ((d[:n4] + d[n3:]) / 2)
            )
        else:
            diag_3 = (
                2
                * self.factors["transmissibility conversion"]
                / ((d[:n4] / (A[:n4] * k[:n4])) + (d[n3:] / (A[n3:] * k[n3:])))
            )
        return diag_3, n3

    def get_cells_G(
        self,
        boundary: bool = False,
        sparse: bool = True,
    ):
        """Returns cells geometric factor (G) Matrix.

        This matrix is essential to build the coefficient matrix (A).
        Note that this matrix should not include boundary. However,
        boundary argument is included just for testing purposes.

        Parameters
        ----------
        sparse : bool, optional
            _description_

        Returns
        -------
        ndarray or sparse matrix
            G matrix for the entire grid model without boundary.
        """

        if self.D >= 1:
            diag_1 = self.get_cells_G_diag_1(boundary)

        if self.D >= 2:
            diag_2, n2 = self.get_cells_G_diag_2(boundary, diag_1)

        if self.D == 3:
            diag_3, n3 = self.get_cells_G_diag_3(boundary, diag_2)

        if sparse:
            diag = ss.diags(
                [diag_1, diag_1],
                [1, -1],
                dtype=self.dtype,
            )
        else:
            diag = np.diag(diag_1, 1) + np.diag(diag_1, -1)

        if self.D >= 2:
            if sparse:
                diag = diag + ss.diags(
                    [diag_2, diag_2],
                    [n2, -n2],
                    dtype=self.dtype,
                )
            else:
                diag = diag + np.diag(diag_2, n2) + np.diag(diag_2, -n2)

        if self.D == 3:
            if sparse:
                diag = diag + ss.diags(
                    [diag_3, diag_3],
                    [n3, -n3],
                    dtype=self.dtype,
                )
            else:
                diag = diag + np.diag(diag_3, n3) + np.diag(diag_3, -n3)

        if sparse:
            return ss.lil_matrix(diag, dtype=self.dtype)
        else:
            return diag

    @_lru_cache(maxsize=None)
    def get_cell_G(
        self,
        id=None,
        coords=None,
        boundary: bool = True,
    ):
        """Returns cell geometric factor (G) with all cell neighbors.

        Parameters
        ----------
        id : int, iterable of int
            cell id based on natural order as int. For multiple cells,
            list of int [id,id,..] or tuple of int (id,id,...).
            NotFullyImplemented.
        coords : iterable of int, iterable of tuples of int, by default
            None cell coordinates (i,j,k) as a tuple of int. For
            multiple cells, tuple of tuples of int as
            ((i,j,k),(i,j,k),..). NotFullyImplemented.
        boundary : bool, optional
            include boundary cells.

        Returns
        -------
        ndarray
            array of G based on dir argument.

        """
        # ToDo
        # ----
        # - for now use only with id
        neighbors = self.get_cell_neighbors(id, coords, boundary, fmt="dict")
        G = {}

        for fdir in self.get_fdir():
            d = self.get_cell_d(fdir, id, coords)
            A = self.get_cell_A(fdir, id, coords)
            k = self.get_cell_k(fdir, id, coords)

            for id_n in neighbors[fdir]:
                if id is not None:
                    d_n = self.get_cell_d(fdir, id_n, None)
                    A_n = self.get_cell_A(fdir, id_n, None)
                    k_n = self.get_cell_k(fdir, id_n, None)
                else:
                    d_n = self.get_cell_d(fdir, None, id_n)
                    A_n = self.get_cell_A(fdir, None, id_n)
                    k_n = self.get_cell_k(fdir, None, id_n)

                if self.is_isotropic:  # or regular grid (To do)
                    G[id_n] = (
                        self.factors["transmissibility conversion"]
                        * ((k + k_n) / 2)
                        * ((A + A_n) / 2)
                        / ((d + d_n) / 2)
                    )
                else:
                    G[id_n] = (
                        2
                        * self.factors["transmissibility conversion"]
                        / ((d / (A * k)) + (d_n / (A_n * k_n)))
                    )
        return G

    # -------------------------------------------------------------------------
    # Visualization:
    # -------------------------------------------------------------------------

    show = utils.pyvista.show_grid

    # -------------------------------------------------------------------------
    # Synonyms:
    # -------------------------------------------------------------------------

    def allow_synonyms(self):
        """Allow full descriptions.

        This function maps functions as following:

        .. code-block:: python

            self.get_flow_shape = self.get_fshape
            self.flow_shape = self.fshape
            self.porosity = self.phi
            self.get_dimension = self.get_D
            self.dimension = self.D
            self.set_properties = self.set_props
            self.permeability = self.k
            self.permeability_x = self.kx
            self.permeability_y = self.ky
            self.permeability_z = self.kz
            self.tops = self.z

        """
        self.get_flow_shape = self.get_fshape
        self.flow_shape = self.fshape
        self.porosity = self.phi
        self.get_dimension = self.get_D
        self.dimension = self.D
        self.set_properties = self.set_props
        self.permeability = self.k
        self.permeability_x = self.kx
        self.permeability_y = self.ky
        self.permeability_z = self.kz
        self.tops = self.z

    # -------------------------------------------------------------------------
    # End
    # -------------------------------------------------------------------------


if __name__ == "__main__":

    def get_d(d_0, n):
        if n > 1:
            return [d_0] + [d_0 + (i * d_0) for i in range(1, n + 1)] + [d_0]
        else:
            return d_0

    nx, ny, nz = (2, 2, 2)

    dx = get_d(10, nx)
    dy = get_d(10, ny)
    dz = get_d(10, nz)

    grid = RegularCartesian(
        nx=nx,
        ny=ny,
        nz=nz,
        dx=dx,
        dy=dy,
        dz=dz,
        kx=270,
        ky=10,
        kz=20,
        phi=0.27,
        verbose=False,
        unify=False,
    )

    print(grid)
    grid.show(label="i")
    # cells_id = grid.get_cells_id(False, False, "array")
    # Ay = grid.get_cells_Ay(False, False)
    # Ay_b = grid.get_cells_Ay(True, False)
    # print(Ay_b)

    # print(Ay)
    # print(Ay_b[cells_id])
