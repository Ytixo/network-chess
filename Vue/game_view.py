import tkinter as tk

TAILLE_CASE = 80

COULEUR_CLAIRE = "#F0D9B5"
COULEUR_FONCEE = "#B58863"
COULEUR_SELECTION = "#805B3D"

CONVERSION = {
    "♔": "♚", "♕": "♛", "♖": "♜", "♗": "♝", "♘": "♞", "♙": "♟",
    "♚": "♔", "♛": "♕", "♜": "♖", "♝": "♗", "♞": "♘", "♟": "♙",
}


class GameView(tk.Frame):

    def __init__(self, parent: tk.Tk, on_clic_case):
        super().__init__(parent)
        self._on_clic_case = on_clic_case
        self._case_selectionnee: str | None = None
        self._build()

    def _build(self):
        # --- Label de statut (tour en cours) ---
        self._tour_var = tk.StringVar(value="En attente d'un adversaire…")
        tk.Label(
            self,
            textvariable=self._tour_var,
            font=("Arial", 14, "bold"),
        ).pack(pady=(8, 4))

        # --- Conteneur horizontal : historique | échiquier ---
        body = tk.Frame(self)
        body.pack(fill="both", expand=True)

        self._build_historique(body)
        self._build_canvas(body)

    def _build_historique(self, parent: tk.Frame):
        frame = tk.Frame(parent)
        frame.pack(side="left", padx=12, pady=8, anchor="n")

        tk.Label(frame, text="Blancs", font=("Arial", 11, "bold")).grid(row=0, column=0, padx=10)
        tk.Label(frame, text="Noirs",  font=("Arial", 11, "bold")).grid(row=0, column=1, padx=10)

        self._liste_blancs = tk.Listbox(frame, width=10, height=20, font=("Arial", 11))
        self._liste_noirs  = tk.Listbox(frame, width=10, height=20, font=("Arial", 11))
        self._liste_blancs.grid(row=1, column=0, padx=10)
        self._liste_noirs.grid(row=1, column=1, padx=10)

    def _build_canvas(self, parent: tk.Frame):
        size = 10 * TAILLE_CASE
        self._canvas = tk.Canvas(parent, width=size, height=size)
        self._canvas.pack(side="right")

    def set_statut(self, texte: str):
        self._tour_var.set(texte)

    def set_case_selectionnee(self, case: str | None):
        self._case_selectionnee = case

    def ajouter_coup_blancs(self, coup: str):
        self._liste_blancs.insert(tk.END, coup)
        self._liste_blancs.see(tk.END)

    def ajouter_coup_noirs(self, coup: str):
        self._liste_noirs.insert(tk.END, coup)
        self._liste_noirs.see(tk.END)

    def dessiner(self, plateau: list[list[str]], blancs_en_bas: bool):
        if plateau is None:
            return

        self._canvas.delete("all")
        marge = TAILLE_CASE

        lettres = ["A","B","C","D","E","F","G","H"] if blancs_en_bas else ["H","G","F","E","D","C","B","A"]
        chiffres = ["8","7","6","5","4","3","2","1"] if blancs_en_bas else ["1","2","3","4","5","6","7","8"]

        # Coordonnées de bord
        for i in range(8):
            x = marge + i * TAILLE_CASE + TAILLE_CASE / 2
            y = marge + i * TAILLE_CASE + TAILLE_CASE / 2

            for yt in [TAILLE_CASE / 2, marge + 8 * TAILLE_CASE + TAILLE_CASE / 2]:
                self._canvas.create_text(x, yt, text=lettres[i], font=("Arial", 16, "bold"))

            for xt in [TAILLE_CASE / 2, marge + 8 * TAILLE_CASE + TAILLE_CASE / 2]:
                self._canvas.create_text(xt, y, text=chiffres[i], font=("Arial", 16, "bold"))

        # Cases et pièces
        for ligne in range(8):
            for col in range(8):
                x1 = marge + col * TAILLE_CASE
                y1 = marge + ligne * TAILLE_CASE
                x2 = x1 + TAILLE_CASE
                y2 = y1 + TAILLE_CASE

                col_lettre = chr(ord("A") + col) if blancs_en_bas else chr(ord("H") - col)
                ligne_num  = (8 - ligne)          if blancs_en_bas else (ligne + 1)
                case = f"{col_lettre.lower()}{ligne_num}"

                # Couleur de case
                claire = (ligne + col) % 2 == 0
                if case == self._case_selectionnee:
                    couleur = COULEUR_SELECTION
                elif claire:
                    couleur = COULEUR_CLAIRE
                else:
                    couleur = COULEUR_FONCEE

                case_id = self._canvas.create_rectangle(x1, y1, x2, y2, fill=couleur, outline="black")
                self._canvas.tag_bind(case_id, "<Button-1>", lambda e, c=case: self._on_clic_case(c))

                piece = CONVERSION.get(plateau[ligne][col], plateau[ligne][col])
                if piece:
                    piece_id = self._canvas.create_text(
                        x1 + TAILLE_CASE / 2,
                        y1 + TAILLE_CASE / 2,
                        text=piece,
                        font=("Arial", 42),
                    )
                    self._canvas.tag_bind(piece_id, "<Button-1>", lambda e, c=case: self._on_clic_case(c))
