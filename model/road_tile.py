import pygame
from abc import ABC, abstractmethod
from constants import TILE_SIZE


class RoadTile(ABC):
    """ Classe mère abstraite représentant une case du circuit.

    On ne crée jamais de RoadTile directement : on crée un terrain
    (Route, Herbe, Terre, Glace, Vide, Mur) qui hérite de cette classe.

    Attributs :
    ----------
    - col, row : int
        La position de la case dans la grille (colonne, ligne).
    - color : tuple[int, int, int]
        La couleur de la case (rouge, vert, bleu).
    - traction : float
        Facilité à accélérer et freiner sur la case (entre 0 et 1).
    - seuil_derapage : float
        Plus il est grand, plus il est difficile de déraper (entre 0 et 1).
    - frottement_derapage : float
        Frottement subi par la voiture quand elle dérape (entre 0 et 1).
    - sprite : pygame.Surface | None
        Le dessin de la case, créé une seule fois.
    """

    @abstractmethod
    def __init__(self, col, row, color, traction, seuil_derapage, frottement_derapage):
        self.col = col
        self.row = row
        self.color = color
        self.traction = traction
        self.seuil_derapage = seuil_derapage
        self.frottement_derapage = frottement_derapage
        self.sprite: pygame.Surface | None = None

    def get_sprite(self, tile_size: int = TILE_SIZE) -> pygame.Surface:
        """ Renvoie le dessin de la case : un carré de sa couleur. """
        if self.sprite and self.sprite.get_width() == tile_size:
            return self.sprite
        surface = pygame.Surface((tile_size, tile_size))
        surface.fill(self.color)
        pygame.draw.rect(surface, (60, 60, 70), surface.get_rect(), 2)

        self.sprite = surface
        return self.sprite


class Route(RoadTile):
    """ Route : bonne traction, difficile de déraper, gros frottement en dérapage. """

    def __init__(self, col, row):
        super().__init__(col, row, (80, 80, 90), 1.0, 0.9, 0.9)


class Herbe(RoadTile):
    """ Herbe : traction moyenne, facile de déraper, frottement important en dérapage. """

    def __init__(self, col, row):
        super().__init__(col, row, (60, 160, 60), 0.6, 0.5, 0.7)


class Terre(RoadTile):
    """ Terre : traction moyenne, très facile de déraper, frottement moyen en dérapage. """

    def __init__(self, col, row):
        super().__init__(col, row, (140, 90, 50), 0.5, 0.3, 0.5)


class Glace(RoadTile):
    """ Glace : faible traction, dérape presque toujours, presque aucun frottement. """

    def __init__(self, col, row):
        super().__init__(col, row, (180, 230, 255), 0.2, 0.05, 0.05)


class Vide(RoadTile):
    """ Vide : la voiture qui tombe dedans réapparaît à son dernier point de passage. """

    def __init__(self, col, row):
        super().__init__(col, row, (0, 0, 0), 0.0, 0.0, 0.0)


class Mur(RoadTile):
    """ Mur en béton : la voiture ne peut pas le traverser. """

    def __init__(self, col, row):
        super().__init__(col, row, (150, 150, 155), 0.0, 0.0, 0.0)

    def get_sprite(self, tile_size: int = TILE_SIZE) -> pygame.Surface:
        """ Dessine un bloc de béton : la case grise de la classe mère, avec des joints. """
        surface = super().get_sprite(tile_size)
        moitie = tile_size // 2
        quart = tile_size // 4
        joint = (110, 110, 115)
        pygame.draw.line(surface, joint, (0, moitie), (tile_size, moitie), 2)
        pygame.draw.line(surface, joint, (moitie, 0), (moitie, moitie), 2)
        pygame.draw.line(surface, joint, (quart, moitie), (quart, tile_size), 2)
        pygame.draw.line(surface, joint, (3 * quart, moitie), (3 * quart, tile_size), 2)
        return surface
