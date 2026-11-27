import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_BRAKE, CAR_REVERSE, CAR_FRICTION,
    CAR_TURN_SPEED, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE
)


class Car:
    """ Classe représentant la voiture d'un joueur.

    Attributs :
    ----------

    - x, y : float
        La position du centre de la voiture, en pixels.
    - respawn_x, respawn_y : float
        La position où la voiture réapparait quand elle sort de la carte.
    - speed : float
        La vitesse de la voiture, négative en marche arrière.
    - angle : float
        L'orientation de la voiture en degrés (0 = vers la droite, sens trigonométrique).
    - color: tuple[int, int, int]
        La couleur de la carrosserie (rouge, vert, bleu).
    - sprite : pygame.Surface
        Le dessin de la voiture, pointant vers la droite.
    """

    def __init__(self, start_col: int, start_row: int, color: tuple[int, int, int]):
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2     # Position horizontale (en pixels)
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2     # Position verticale (en pixels)
        self.respawn_x = self.x
        self.respawn_y = self.y
        self.speed: float = 0.0                             # Vitesse
        self.angle: float = 0.0                             # Orientation
        self.color = color
        self.sprite = self.build_sprite()

    def accelerate(self) -> None:
        self.speed += CAR_ACCELERATION

    def brake(self) -> None:
        """Freine si la voiture avance, sinon la fait reculer."""
        if self.speed > 0:
            self.speed -= CAR_BRAKE
        else:
            self.speed -= CAR_REVERSE

    def turn_left(self) -> None:
        self.angle += CAR_TURN_SPEED

    def turn_right(self) -> None:
        self.angle -= CAR_TURN_SPEED

    def update_position(self) -> None:
        self.speed *= CAR_FRICTION  # On utilise les frottements car ils réduisent la vitesse
        angle_rad = math.radians(self.angle)
        self.x += self.speed * math.cos(angle_rad)  # Partie horizontale
        self.y -= self.speed * math.sin(angle_rad)  # Partie verticale

    def respawn(self) -> None:
        """
        Replace la voiture à son point de réapparition,
        arrêtée et tournée vers la droite.
        """
        self.x = self.respawn_x
        self.y = self.respawn_y
        self.speed = 0.0
        self.angle = 0.0

    def build_sprite(self) -> pygame.Surface:
        """Dessine la voiture de dessus"""
        length, width = CAR_HEIGHT, CAR_WIDTH       # 50 x 30, couchée
        surf = pygame.Surface((length, width), pygame.SRCALPHA)

        # Roues (dessinées en premier : la carosserie passe par dessus)
        for x, y in [(5, 0), (35, 0), (5, width - 6), (35, width - 6)]:
            pygame.draw.rect(surf, (25, 25, 25), (x, y, 10, 6), border_radius=2)

        # Carosserie, à la couleur du joueur
        pygame.draw.rect(surf, self.color, (1, 4, length - 2, width - 8), border_radius=8)
        # Bande blanche au milieu
        pygame.draw.rect(surf, (255, 255, 255), (4, width // 2 - 2, length - 9, 4))
        # Vitre arrière
        pygame.draw.rect(surf, (40, 40, 55), (10, 8, 7, width - 16), border_radius=2)
        # Pare-brise (vers l'avant)
        pygame.draw.rect(surf, (150, 210, 255), (27, 7, 10, width - 14), border_radius=3)
        # Phares
        pygame.draw.rect(surf, (255, 240, 150), (length - 4, 6, 3, 5), border_radius=1)
        pygame.draw.rect(surf, (255, 240, 150), (length - 4, width - 11, 3, 5), border_radius=1)

        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        rotated = pygame.transform.rotate(self.sprite, self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect
