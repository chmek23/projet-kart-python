import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE, CAR_TURN_SPEED, CAR_BRAKE, CAR_FRICTION, CAR_REVERSE
)


class Car:

    def __init__(self, start_col: int, start_row: int, color):
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
        else : 
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
        Replace la voiture à son point de réeapparition, 
        arrêtée et tournée vers la droite.
        """
        self.x = self.respawn_x
        self.y = self.respawn_y
        self.speed = 0.0
        self.angle = 0.0

    def build_sprite(self) -> pygame.Surface:
        # On remplace le rectangle vertical par un rectangle horizontal car la voiture
        # doit pointer vers la droite lorsque l'angle est de 0
        surf = pygame.Surface((CAR_HEIGHT, CAR_WIDTH), pygame.SRCALPHA) # 50 x 30 : couché
        pygame.draw.rect(surf, (self.color), (0, 0, CAR_HEIGHT,
                         CAR_WIDTH), border_radius=5)
        pygame.draw.rect(surf, (255, 255, 0), (CAR_HEIGHT - 10, 5, 8, CAR_WIDTH - 10))
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        rotated = pygame.transform.rotate(self.sprite, self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect
