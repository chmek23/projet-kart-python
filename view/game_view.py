import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE,
    COLOR_BG, COLOR_TEXT, COLOR_ACCENT, COLOR_PANEL, COLOR_PANEL_BORDER,
    GameState
)
from model.game_model import GameModel


class GameView:
    """ Classe qui dessine l'état du modèle à l'écran, sans jamais le modifier.

    Attributs :
    ----------
    - screen : pygame.Surface
        La fenêtre dans laquelle on dessine.
    - font : pygame.font.Font
        La police utilisée pour les textes.
    """

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)

    def draw(self, model: GameModel) -> None:
        """ Dessine l'écran qui correspond à l'état du jeu (menu ou course).

        Paramètres :
        ----------
        - model : GameModel
            L'état du jeu à afficher.
        """
        self.screen.fill(COLOR_BG)
        if model.state == GameState.MENU:
            self._draw_menu("Jeu de course 2D", ["JOUER (Entrée)", "QUITTER (Échap)"], 0)
        elif model.state == GameState.CHOIX_CIRCUIT:
            self._draw_menu("Choisis un circuit", model.circuit_names, model.selected)
        elif model.state == GameState.RACING:
            self._draw_racing(model)
        pygame.display.flip()

    def _draw_menu(self, titre, options, selected) -> None:
        """ Dessine un menu : un titre et un bouton par option, le bouton sélectionné en jaune.
        Sert pour le menu principal et pour le choix du circuit.

        Paramètres :
        ----------
        - titre : str
            Le titre affiché en haut.
        - options : list[str]
            Le texte de chaque bouton.
        - selected : int
            L'indice du bouton sélectionné.
        """
        cx = WINDOW_WIDTH // 2

        title_surf = self.font.render(titre, True, COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 160)))

        for i, label in enumerate(options):
            y = 320 + i * 80
            rect = pygame.Rect(cx - 140, y - 25, 280, 50)
            if i == selected:
                couleur = COLOR_ACCENT
            else:
                couleur = COLOR_TEXT
            pygame.draw.rect(self.screen, COLOR_PANEL, rect, border_radius=8)
            pygame.draw.rect(self.screen, couleur, rect, 2, border_radius=8)
            text_surf = self.font.render(label, True, couleur)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    def _draw_racing(self, model: GameModel) -> None:
        """ Dessine la course : les cases du circuit, puis les voitures par-dessus.

        Paramètres :
        ----------
        - model : GameModel
            L'état du jeu à afficher.
        """
        if model.circuit is None:
            return

        for row_idx, row in enumerate(model.circuit.grid):
            for col_idx, tile in enumerate(row):
                sprite = tile.get_sprite(TILE_SIZE)
                self.screen.blit(
                    sprite, (col_idx * TILE_SIZE, row_idx * TILE_SIZE))

        for car in model.cars:
            surf, rect = car.get_rotated_sprite()
            self.screen.blit(surf, rect)
