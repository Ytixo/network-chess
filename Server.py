from Logique.Tile import Tile
from Logique.Grid import Grid
import socket
import threading
from queue import Queue

host = "0.0.0.0"
port = 6767

class Client:
    def __init__(self, name, addr):
        self.name = name
        self.addr = addr
        self.queue = Queue()
        self.in_game = False

waiting_players = []
clients_connectes = {}
partie_id = 0
lock = threading.Lock()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

print("Serveur lancé !")

def envoyer(message, joueur):
    s.sendto(message.encode("utf-8"), joueur.addr)

def recevoir(joueur):
    return joueur.queue.get().strip()

def partie(joueur1, joueur2, id_partie):
    print(f"Partie #{id_partie} : {joueur1.name} vs {joueur2.name}")

    envoyer(f"La partie va commencer contre {joueur2.name}", joueur1)
    envoyer(f"La partie va commencer contre {joueur1.name}", joueur2)

    grid = Grid()
    grid.InitBoard()

    color_playing = "white"
    joueur_actif = joueur1
    joueur_inactif = joueur2

    while True:
        
        
        envoyer(grid.afficher(flip=True), joueur1)
        envoyer(grid.afficher(flip=False), joueur2)

        if(grid.Winner != ""):
            envoyer(f"Echec et mat, les " + str(joueur_actif) + "ont gagnés", joueur_inactif)
            envoyer(f"Echec et mat, les " + str(joueur_inactif) + "ont perdu",joueur_actif)
            break

        envoyer(f"TON_TOUR Quelle pièce veux-tu bouger ?", joueur_actif)
        envoyer(f"ATTENDRE C'est le tour de {joueur_actif.name}", joueur_inactif)

        inp = recevoir(joueur_actif)

        if inp == "stop":
            envoyer("Partie stoppée.", joueur1)
            envoyer("Partie stoppée.", joueur2)
            print(f"Partie #{id_partie} stoppée")
            break

        envoyer("Sur quelle case veux-tu l'emmener ?", joueur_actif)
        out = recevoir(joueur_actif)

        if grid.ResolveTile(inp) is None or grid.ResolveTile(out) is None:
            envoyer("Coup illégal, cases invalides.", joueur_actif)
            continue

        res = grid.ResolveTile(inp)
        if grid.grid[res].ColorPresent != color_playing:
            envoyer("Jouez un coup avec vos pièces !", joueur_actif)
            continue

        if not grid.CanMove(inp, out):
            envoyer("Coup illégal.", joueur_actif)
            continue
    
        if (grid.CanMove(inp, out)):
                grid.UpdateBoard(grid.ResolveTile(inp), grid.ResolveTile(out))


        color_playing = "black" if color_playing == "white" else "white"
        joueur_actif, joueur_inactif = joueur_inactif, joueur_actif
    
    joueur1.in_game = False
    joueur2.in_game = False

    print(f"Partie #{id_partie} terminée")

while True:
    data, addr = s.recvfrom(1024)
    message = data.decode("utf-8").strip()

    if addr in clients_connectes:
        joueur = clients_connectes[addr]
        if joueur.in_game:
            joueur.queue.put(message)
        continue

    # Nouveau joueur
    joueur = Client(message, addr)
    clients_connectes[addr] = joueur
    print(f"Le joueur {joueur.name} vient de se connecter")
    envoyer(f"Tu es bien connecté {joueur.name}", joueur)
    envoyer("En attente d'un adversaire...", joueur)

    with lock:
        waiting_players.append(joueur)

        while len(waiting_players) >= 2:
            partie_id += 1

            joueur1 = waiting_players.pop(0)
            joueur2 = waiting_players.pop(0)

            joueur1.in_game = True
            joueur2.in_game = True

            thread = threading.Thread(
                target=partie,
                args=(joueur1, joueur2, partie_id),
                daemon=True
            )
            thread.start()