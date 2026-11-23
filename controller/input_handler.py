import pygame

# Touches du joueur 1 : Z ou W et Q ou A, pour les claviers AZERTY et QWERTY
MAPPING_P1 = {
    pygame.K_z: "accelerate",
    pygame.K_w: "accelerate",
    pygame.K_s: "brake",
    pygame.K_q: "turn_left",
    pygame.K_a: "turn_left",
    pygame.K_d: "turn_right"
}

# Touches du joueur 2 : les flèches
MAPPING_P2 = {
    pygame.K_UP:    "accelerate",
    pygame.K_DOWN:  "brake",
    pygame.K_LEFT:  "turn_left",
    pygame.K_RIGHT: "turn_right",
}


class InputHandler:
    """ Classe qui traduit les touches du clavier d'un joueur en actions du jeu.

    Attributs :
    ----------
    - mapping : dict[int, str]
        Associe chaque code de touche pygame au nom d'une action ("accelerate", "brake", ...).
    """

    def __init__(self, mapping: dict):
        self.mapping = mapping

    def get_inputs(self) -> dict:
        """ Regarde quelles touches du joueur sont maintenues à cet instant.

        Retourne :
        ----------
        - dict[str, bool]
            Pour chaque action, True si une de ses touches est enfoncée, False sinon.
        """
        keys = pygame.key.get_pressed()  # état de toutes les touches : True si enfoncée
        # Au départ, aucune action n'est demandée
        p = {action: False for action in self.mapping.values()}

        # items() renvoie les couples (touche, action)
        for key, action in self.mapping.items():
            if keys[key]:                           # Si la touche est enfoncée
                p[action] = True                    # L'action est demandée

        return p
