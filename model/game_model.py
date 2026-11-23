from constants import GameState, GRID_ROWS, GRID_COLS
from model.car import Car
from model.circuit import Circuit
from model.road_tile import Route, Herbe, Terre, Glace, Vide


class GameModel: 
    """ Classe représentant l'état complet du jeu.

    Attributs :
    ----------
    - state : str
        L'état courant du jeu (GameState.MENU ou GameState.RACING).
    - circuit : Circuit | None
        Le circuit de la course, None tant qu'aucune course n'est lancée.
    - cars : list[Car]
        Les voitures des joueurs (la première est celle du joueur 1).
    """

    def __init__(self):
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.cars: list[Car] | None = None

    def load_circuit(self, fichier="circuits/circuit1.txt") -> None:
        """ Crée le circuit à partir d'un fichier texte, puis place les voitures.

        Chaque lettre du fichier est un terrain :
        R = route, H = herbe, T = terre, G = glace, V = vide.
        """
        terrains = {"R": Route, "H": Herbe, "T": Terre, "G": Glace, "V": Vide}

        with open(fichier) as f:
            lignes = f.readlines()

        grid = []
        for row_idx in range(GRID_ROWS):
            ligne = []
            for col_idx in range(GRID_COLS):
                lettre = lignes[row_idx][col_idx]
                ligne.append(terrains[lettre](col_idx, row_idx))
            grid.append(ligne)

        self.circuit = Circuit(grid=grid)
        self.spawn_car()

    def spawn_car(self) -> None:
        """ Crée les voitures des deux joueurs à leur position de départ. """
        self.cars = [
            Car(7, 1, (255, 0, 0)),     # Joueur 1 : rouge
            Car(7, 2, (0, 120, 255)),   # Joueur 2 : bleu
        ]

    def update(self) -> None:
        """ Déplace chaque voiture, et la fait réapparaître si elle est sortie de la carte. """
        if self.state != GameState.RACING or self.circuit is None:
            return

        for car in self.cars:
            car.update_position()
            tile = self.circuit.get_tile_at_pixel(car.x, car.y)
            if tile is None:    # Pas de case sous la voiture : elle est sortie 
                car.respawn()
