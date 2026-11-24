from model.road_tile import RoadTile
from constants import TILE_SIZE


class Circuit:
    """ Classe représentant le circuit : une grille de cases (terrains).

    Attributs :
    ----------
    - grid : list[list[RoadTile]]
        La grille des cases, rangée par lignes : grid[ligne][colonne].
    - rows : int
        Le nombre de lignes de la grille.
    - cols : int
        Le nombre de colonnes de la grille.
    """

    def __init__(self,  grid: list[list[RoadTile]]):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

    def get_tile(self, col: int, row: int) -> RoadTile | None:
        """ Renvoie la case située à une colonne et une ligne données.

        Paramètres :
        ----------
        - col : int
            Le numéro de colonne de la case.
        - row : int
            Le numéro de ligne de la case.

        Retourne :
        ----------
        - RoadTile | None
            La case demandée, ou None si la position est en dehors de la carte.
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def get_tile_at_pixel(self, px: float, py: float) -> RoadTile | None:
        """ Renvoie la case qui se trouve sous un point de l'écran.

        Paramètres :
        ----------
        - px, py : float
            La position du point, en pixels.

        Retourne :
        ----------
        - RoadTile | None
            La case sous ce point, ou None si le point est en dehors de la carte.
        """
        col = int(px // TILE_SIZE)
        row = int(py // TILE_SIZE)
        return self.get_tile(col, row)

    def pixel_width(self) -> int:
        """ Renvoie la largeur du circuit, en pixels. """
        return self.cols * TILE_SIZE

    def pixel_height(self) -> int:
        """ Renvoie la hauteur du circuit, en pixels. """
        return self.rows * TILE_SIZE
