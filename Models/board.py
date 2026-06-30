CONVERSION = {
    "♔": "♚", "♕": "♛", "♖": "♜", "♗": "♝", "♘": "♞", "♙": "♟",
    "♚": "♔", "♛": "♕", "♜": "♖", "♝": "♗", "♞": "♘", "♟": "♙",
}

class BoardModel:
    def __init__(self):
        self.plateau = None
        self.blancs_en_bas = None

    def appliquer_plateau(self, texte):
        lignes = texte.strip().split("\n")
        nouveau = []
        for ligne in lignes[1:]:
            cases = [c.strip() for c in ligne.strip("|").split("||")][:-1]
            nouveau.append(cases)

        if self.blancs_en_bas is None:
            piece = CONVERSION.get(nouveau[7][0], nouveau[7][0])
            self.blancs_en_bas = piece in {"♖", "♘", "♗", "♕", "♔", "♙"}

        self.plateau = nouveau
        return self.plateau, self.blancs_en_bas

    def detecter_coup(self, ancien, nouveau):
        depart = arrivee = None
        for r in range(8):
            for c in range(8):
                if ancien[r][c] and not nouveau[r][c]:
                    depart = (r, c)
                elif nouveau[r][c] and ancien[r][c] != nouveau[r][c]:
                    arrivee = (r, c)
        return depart, arrivee

    def indices_vers_case(self, pos):
        r, c = pos
        if self.blancs_en_bas:
            return f"{chr(ord('a') + c)}{8 - r}"
        else:
            return f"{chr(ord('h') - c)}{r + 1}"