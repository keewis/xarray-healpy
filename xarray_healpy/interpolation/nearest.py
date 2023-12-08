import numpy as np
import sparse
import xarray as xr
from sklearn.neighbors import BallTree

from xarray_healpy.interpolation.utils import determine_stack_dims, prepare_coords


def nearest_neighbor_interpolation_weights(
    source_grid, target_grid, *, metric="euclidean", coords=["longitude", "latitude"]
):
    """xarray-aware nearest-neighbor interpolation weights computation

    Parameters
    ----------
    source_grid : xarray.Dataset
        The source grid. Has to have the coordinates specified by ``coords``.
    target_grid : xarray.Dataset
        The target grid. Has to have the coordinates specified by ``coords``.
    metric : str, default: "euclidean"
        The metric to use when find the nearest neighbors. Look at the value of
        ``BallTree.valid_metrics`` for the full list of metrics. Note that choosing
        metrics other than ``"euclidean"`` affects the neighbors search, but so far the
        weights computation itself happens in a euclidean space.
    coords : list of str, default: ["longitude", "latitude"]
        The names of the spatial coordinates in both the source and target grids.

    Returns
    -------
    weights : xarray.DataArray
        The computed weights as a sparse matrix.
    """
    # TODO: how do we detect the variables and dims to stack?
    # For now, just use the coords directly
    source_stacked_dim = "_source_cells"
    target_stacked_dim = "_target_cells"

    # prepare the grids
    source_stack_dims = determine_stack_dims(source_grid, coords)
    source_coords = prepare_coords(
        source_grid, coords, source_stacked_dim, source_stack_dims
    )

    target_stack_dims = determine_stack_dims(target_grid, coords)
    target_coords = prepare_coords(
        target_grid, coords, target_stacked_dim, target_stack_dims
    )

    # use a tree index to find the n closest neighbors
    tree = BallTree(source_coords, metric=metric)
    _, neighbor_indices = tree.query(target_coords, k=1, dualtree=True)

    raw_weights = np.ones_like(neighbor_indices, dtype=float)

    # arrange as a sparse matrix
    n_target = target_coords.shape[0]
    n_source = source_coords.shape[0]

    target_indices = np.broadcast_to(
        np.arange(n_target)[:, None], neighbor_indices.shape
    )
    sparse_coords = np.stack([target_indices, neighbor_indices], axis=0)

    source_shape = tuple([source_grid.sizes[dim] for dim in source_stack_dims])
    target_shape = tuple([target_grid.sizes[dim] for dim in target_stack_dims])

    reshaped_sparse_coords = np.reshape(sparse_coords, (2, -1))
    reshaped_raw_weights = np.reshape(raw_weights, -1)

    coords = reshaped_sparse_coords
    data = reshaped_raw_weights

    raw_weights_matrix = sparse.COO(
        coords=coords, data=data, shape=(n_target, n_source), fill_value=0.0
    )
    weights_matrix = np.reshape(raw_weights_matrix, target_shape + source_shape)

    # put into a DataArray
    weights = xr.DataArray(
        weights_matrix,
        dims=target_stack_dims + source_stack_dims,
        coords=target_grid.coords,
        attrs={"sum_dims": source_stack_dims},
    )

    return weights
