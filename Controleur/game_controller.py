from Models.network import NetworkModel
from Models.board import BoardModel
from Models.game import GameModel
from Vue.game_view import GameView


class GameController:

    def __init__(self, root, network: NetworkModel, board: BoardModel, game: GameModel):
        self._root = root
        self._network = network
        self._board = board
        self._game = game

        self._view = GameView(root, on_clic_case=self._clic_case)
        self._view.pack(fill="both", expand=True)

        self._doit_jouer = False

    def demarrer(self):
        self._view.set_statut("En attente d'un adversaire…")

    def _clic_case(self, case: str):
        if not self._doit_jouer:
            return

        if self._game.coup_depart is None:
            # Premier clic : sélection de la pièce
            self._game.coup_depart = case
            self._view.set_case_selectionnee(case)
            self._rafraichir_plateau()
            return

        # Deuxième clic : envoi du coup
        depart  = self._game.coup_depart
        arrivee = case
        self._game.coup_depart = None
        self._doit_jouer = False

        self._network.send(depart)
        self._network.send(arrivee)

        self._game.mon_coup_en_attente = True
        self._game.enregistrer_coup(depart, arrivee, moi=True)
        self._root.after(0, lambda d=depart, a=arrivee: self._afficher_coup_historique(d, a, moi=True))

        self._view.set_case_selectionnee(arrivee)
        self._rafraichir_plateau()

    def traiter_message(self, message: str):
        print(f"[message reçu] {repr(message)}")
        if "TON_TOUR" in message:
            self._root.after(0, lambda: self._view.set_statut("Ton tour — choisis une pièce"))
            self._doit_jouer = True

        elif "Sur quelle case" in message:
            self._root.after(0, lambda: self._view.set_statut("Ton tour — choisis la destination"))
            self._doit_jouer = True

        elif "gagnés" in message:
            self._root.after(0, lambda: self._view.set_statut("Partie terminée — Vous avez gagné ! 🏆"))

        elif "perdu" in message:
            self._root.after(0, lambda: self._view.set_statut("Partie terminée — Vous avez perdu."))

        elif "||" in message and "|" in message:
            self._recevoir_plateau(message)

        elif "Partie stoppée" in message:
            self._root.after(0, lambda: self._view.set_statut("Partie stoppée par le serveur."))

    def _recevoir_plateau(self, texte: str):
        ancien_plateau = self._board.plateau
        nouveau_plateau, blancs_en_bas = self._board.appliquer_plateau(texte)
        self._game.blancs_en_bas = blancs_en_bas

        if self._game.mon_coup_en_attente:
            self._game.mon_coup_en_attente = False
        elif ancien_plateau is not None:
            dep, arr = self._board.detecter_coup(ancien_plateau, nouveau_plateau)
            if dep and arr:
                case_dep = self._board.indices_vers_case(dep)
                case_arr = self._board.indices_vers_case(arr)
                self._game.enregistrer_coup(case_dep, case_arr, moi=False)
                self._root.after(0, lambda d=case_dep, a=case_arr: self._afficher_coup_historique(d, a, moi=False))

        self._root.after(0, lambda: self._view.set_statut("⏳ Tour de l'adversaire…"))
        self._root.after(0, self._rafraichir_plateau)

    def _rafraichir_plateau(self):
        if self._board.plateau and self._game.blancs_en_bas is not None:
            self._view.dessiner(self._board.plateau, self._game.blancs_en_bas)

    def _afficher_coup_historique(self, depart: str, arrivee: str, moi: bool):
        coup = f"{depart}→{arrivee}"
        # moi=True : je suis les blancs si blancs_en_bas
        if moi:
            if self._game.blancs_en_bas:
                self._view.ajouter_coup_blancs(coup)
            else:
                self._view.ajouter_coup_noirs(coup)
        else:
            if self._game.blancs_en_bas:
                self._view.ajouter_coup_noirs(coup)
            else:
                self._view.ajouter_coup_blancs(coup)
