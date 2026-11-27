import pygame
import sys
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    GameState
)
from model.game_model import GameModel
from view.game_view import GameView
from controller.input_handler import InputHandler, MAPPING_P1, MAPPING_P2


class GameController:
    """ Classe qui relie le clavier, le modèle et la vue, et fait tourner la boucle du jeu.

    Attributs :
    ----------
    - screen : pygame.Surface
        La fenêtre du jeu.
    - clock : pygame.time.Clock
        L'horloge qui limite le jeu à FPS images par seconde.
    - model : GameModel
        L'état du jeu (circuit, voitures, état courant).
    - view : GameView
        L'objet qui dessine le modèle à l'écran.
    - input_handlers : list[InputHandler]
        Un traducteur de touches par joueur, dans le même ordre que model.cars.
    - running : bool
        Vaut False quand on quitte le jeu.
    """

    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.model = GameModel()
        self.view = GameView(self.screen)
        self.input_handlers = [InputHandler(MAPPING_P1), InputHandler(MAPPING_P2)]
        self.running = True

    def run(self) -> None:
        """ Fait tourner la boucle principale du jeu jusqu'à ce qu'on quitte. """
        while self.running:
            self.handle_events()    # 1. Lire les événements (fermer la fenêtre, touche appuyée)
            self.update()           # 2. Mettre à jour le modèle (la voiture bouge)
            self.render()           # 3. Tout redessiner
            self.clock.tick(FPS)    # 4. Attendre pour faire 60 tours par seconde

    def handle_events(self) -> None:
        """ Traite les événements de la frame : fermeture de la fenêtre
        et touches qui viennent d'être enfoncées.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key: int) -> None:
        """ Transmet une touche qui vient d'être enfoncée au traitement de l'état courant.

        Paramètres :
        ----------
        - key : int
            Le code pygame de la touche enfoncée.
        """
        state = self.model.state

        if state == GameState.MENU:
            self.handle_menu_key(key)
        elif state == GameState.CHOIX_CIRCUIT:
            self.handle_choix_key(key)
        elif state == GameState.RACING and key == pygame.K_ESCAPE:
            self.model.state = GameState.CHOIX_CIRCUIT

    def handle_menu_key(self, key: int) -> None:
        """ Gère une touche dans le menu : Entrée ouvre le choix du circuit, Échap quitte le jeu.

        Paramètres :
        ----------
        - key : int
            Le code pygame de la touche enfoncée.
        """
        if key == pygame.K_RETURN:
            self.model.state = GameState.CHOIX_CIRCUIT
        elif key == pygame.K_ESCAPE:
            self.quit()

    def handle_choix_key(self, key: int) -> None:
        """ Gère une touche dans le choix du circuit : les flèches changent de circuit,
        Entrée lance la course, Échap revient au menu.

        Paramètres :
        ----------
        - key : int
            Le code pygame de la touche enfoncée.
        """
        if key == pygame.K_UP and self.model.selected > 0:
            self.model.selected -= 1
        elif key == pygame.K_DOWN and self.model.selected < len(self.model.circuits) - 1:
            self.model.selected += 1
        elif key == pygame.K_RETURN:
            self.model.load_circuit(self.model.circuits[self.model.selected])
            self.model.state = GameState.RACING
        elif key == pygame.K_ESCAPE:
            self.model.state = GameState.MENU

    def update(self) -> None:
        """ Pendant la course, applique les commandes de chaque joueur à sa voiture,
        puis met à jour le modèle.
        """
        if self.model.state != GameState.RACING:
            return

        # zip associe la voiture 1 au clavier du joueur 1, et la voiture 2 au clavier du joueur 2
        for car, handler in zip(self.model.cars, self.input_handlers):
            self.apply_input(car, handler.get_inputs())
        self.model.update()

    def apply_input(self, car, player_input) -> None:
        """ Appelle les méthodes de la voiture qui correspondent aux actions demandées.

        Paramètres :
        ----------
        - car : Car
            La voiture du joueur.
        - player_input : dict[str, bool]
            Les actions demandées par le joueur, renvoyées par InputHandler.get_inputs().
        """
        if player_input['accelerate']:
            car.accelerate()
        if player_input['brake']:
            car.brake()
        if player_input['turn_left']:
            car.turn_left()
        if player_input['turn_right']:
            car.turn_right()

    def render(self) -> None:
        """ Demande à la vue de dessiner l'état actuel du modèle. """
        self.view.draw(self.model)

    def quit(self) -> None:
        """ Ferme pygame et quitte le programme. """
        self.running = False
        pygame.quit()
        sys.exit()
