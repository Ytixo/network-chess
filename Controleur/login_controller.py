import threading

from Models.network import NetworkModel
from Models.game import GameModel
from Vue.login_view import LoginView


class LoginController:

    def __init__(self, root, network: NetworkModel, game: GameModel, on_connected):
        self._root = root
        self._network = network
        self._game = game
        self._on_connected = on_connected

        self._view = LoginView(root, on_submit=self._valider_pseudo)
        self._view.pack(fill="both", expand=True)

    def _valider_pseudo(self, pseudo: str):
        self._game.pseudo = pseudo
        
        self._network.send(pseudo)

        # Cache la vue de login et signale la connexion réussie
        self._view.pack_forget()
        self._view.destroy()
        self._on_connected()