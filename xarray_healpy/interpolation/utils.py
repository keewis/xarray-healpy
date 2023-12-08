import itertools

import numpy as np


def determine_stack_dims(grid, variables):
    all_dims = (tuple(grid[var].dims) for var in variables)

    return tuple(dict.fromkeys(itertools.chain.from_iterable(all_dims)))


def prepare_coords(grid, coords, stacked_dim, stacked_dims):
    stacked = grid[coords].stack({stacked_dim: stacked_dims})

    return np.stack([stacked[coord].data for coord in coords], axis=-1)
