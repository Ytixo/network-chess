class GameModel:

    def __init__(self):
        self.pseudo: str = ""
        self.blancs_en_bas: bool | None = None
        self.historique_blancs: list[str] = []
        self.historique_noirs: list[str] = []
        self.mon_coup_en_attente: bool = False
        self.coup_depart: str | None = None  # case sélectionnée au 1er clic

    def reset(self):
        self.historique_blancs.clear()
        self.historique_noirs.clear()
        self.mon_coup_en_attente = False
        self.coup_depart = None
        self.blancs_en_bas = None

    def enregistrer_coup(self, depart: str, arrivee: str, moi: bool):
        coup = f"{depart}→{arrivee}"
        # Si je suis les blancs (en bas) mes coups vont dans blancs, sinon noirs
        if moi:
            if self.blancs_en_bas:
                self.historique_blancs.append(coup)
            else:
                self.historique_noirs.append(coup)
        else:
            if self.blancs_en_bas:
                self.historique_noirs.append(coup)
            else:
                self.historique_blancs.append(coup)
