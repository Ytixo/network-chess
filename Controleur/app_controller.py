import threading
import tkinter as tk

from Models.network import NetworkModel
from Models.board import BoardModel
from Models.game import GameModel
from Controleur.login_controller import LoginController
from Controleur.game_controller import GameController

class AppController:

    def __init__(self):
        self._root = tk.Tk()
        self._root.title("Échecs en réseau")

        self._network = NetworkModel()
        self._board   = BoardModel()
        self._game    = GameModel()

        self._game_ctrl: GameController = None

        self._login_ctrl = LoginController(
            self._root,
            self._network,
            self._game,
            on_connected=self._on_connected,
        )

    def _on_connected(self):
        self._game_ctrl = GameController(
            self._root,
            self._network,
            self._board,
            self._game,
        )
        self._game_ctrl.demarrer()

        thread = threading.Thread(target=self._boucle_reseau, daemon=True)
        thread.start()

    def _boucle_reseau(self):
        while True:
            try:
                message = self._network.receive()
            except OSError:
                break

            print(f"[réseau] {message!r}")

            if self._game_ctrl:
                self._game_ctrl.traiter_message(message)

            if "Partie stoppée" in message:
                break

    def run(self):
        self._root.mainloop()
        self._network.close()
