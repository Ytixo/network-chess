import tkinter as tk
from tkinter import ttk


class LoginView(tk.Frame):

    def __init__(self, parent: tk.Tk, on_submit):
        super().__init__(parent)
        self._on_submit = on_submit
        self._build()

    def _build(self):
        self.configure(padx=40, pady=40)

        tk.Label(
            self,
            text="♟ Échecs en réseau",
            font=("Arial", 22, "bold"),
        ).pack(pady=(0, 24))

        tk.Label(
            self,
            text="Votre pseudo :",
            font=("Arial", 13),
        ).pack(anchor="w")

        self._entry = tk.Entry(self, font=("Arial", 13), width=24)
        self._entry.pack(pady=(4, 12))
        self._entry.bind("<Return>", self._valider)
        self._entry.focus()

        tk.Button(
            self,
            text="Rejoindre la partie",
            font=("Arial", 12, "bold"),
            command=self._valider,
            padx=10,
            pady=6,
        ).pack()

        self._error_var = tk.StringVar()
        tk.Label(
            self,
            textvariable=self._error_var,
            font=("Arial", 11),
            fg="red",
        ).pack(pady=(8, 0))

    def _valider(self, event=None):
        pseudo = self._entry.get().strip()
        if not pseudo:
            self._error_var.set("Le pseudo ne peut pas être vide.")
            return
        self._error_var.set("")
        self._on_submit(pseudo)

    def afficher_erreur(self, message: str):
        self._error_var.set(message)
