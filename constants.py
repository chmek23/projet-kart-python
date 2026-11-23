WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FPS = 60

TILE_SIZE = 32
GRID_COLS = 32
GRID_ROWS = 24

CAR_ACCELERATION = 0.15
CAR_BRAKE = 0.4            # Freinage : 3 fois plus fort que l'accélération
CAR_REVERSE = 0.08          # Marche arrière : Plus lente que la marche avant
CAR_FRICTION = 0.98
CAR_WIDTH = 30
CAR_HEIGHT = 50
CAR_TURN_SPEED = 3


class GameState:
    """ Classe regroupant les états possibles du jeu.

    Attributs :
    ----------
    - MENU : str
        Le menu principal est affiché.
    - RACING : str
        Une course est en cours.
    """
    MENU = "menu"
    RACING = "racing"


# --- Couleurs UI ---
COLOR_BG = (15, 15, 25)
COLOR_TEXT = (240, 240, 240)
COLOR_ACCENT = (255, 200, 0)
COLOR_PANEL = (30, 30, 50)
COLOR_PANEL_BORDER = (60, 60, 100)

