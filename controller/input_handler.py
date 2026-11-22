import pygame


MAPPING = {
    pygame.K_UP:    "accelerate",
    pygame.K_DOWN:  "brake"
}


class InputHandler:

    def __init__(self):
        self.mapping = MAPPING

    def get_inputs(self) -> dict:
        keys = pygame.key.get_pressed() # vaut TRUE si la touche du haut est enfoncée en ce moment
        # On part d'un dictionnaire où toutes les actions sont à FALSE : p = {"accelerate" : False}
        p = {action: False for action in self.mapping.values()}     # values() renvoie "accelerate"

        for key, action in self.mapping.items():    # items() renvoie les couples (clé, valeur)
            if keys[key]:                           # Si la touche est enfoncée
                p[action] = True                    # L'action est demandée

        return p
