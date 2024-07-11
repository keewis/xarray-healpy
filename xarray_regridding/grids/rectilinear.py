from dataclasses import dataclass


@dataclass
class Rectilinear1D:
    """neighbouring cell search within a rectilinear grid with 1D coordinates"""

    # properties:
    # - rectangular grid cells
    # - regular size of the grid
    # - sorted (ascending or descending)
    # on init, determine:
    # - the cell size in x and y
    # - min / max value per coordinate (including cell size)
    # - sorting of the coordinates (ascending / descending)
    # - presence of discontinuities (poles, prime meridian / date line)

    def search_neighbours(self, points):
        # search algorithm: for each target point,
        # - map to the same coordinate range (0→360 or -180→180)
        # - compute the integer indices of the nearest neighbour
        # - boundary treatment: do we extrapolate?
        # - compute the relative position of the neighbour (quadrant)
        # - query integer offsets for the quadrant
        # - construct the other 3 neighbours
        #   - if the neighbour is at the date line / prime meridian, wrap around
        #   - if the point is between pole and the neighbour, return only two neighbours?
        pass


@dataclass
class Rectilinear2D:
    """neighbouring cell search within a rectilinear grid with 2D coordinates"""

    def search_neighbours(self, points):
        # search algorithm: same as rectilinear 1D, if we drop the duplicated values
        pass
