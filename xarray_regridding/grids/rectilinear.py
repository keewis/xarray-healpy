from dataclasses import dataclass


@dataclass
class Rectilinear1D:
    """neighbouring cell search within a rectilinear grid with 1D coordinates"""

    def search_neighbours(self, points):
        pass


@dataclass
class Rectilinear2D:
    """neighbouring cell search within a rectilinear grid with 2D coordinates"""

    def search_neighbours(self, points):
        pass
