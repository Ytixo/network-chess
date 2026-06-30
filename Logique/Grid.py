from Logique.Tile import Tile
from math import *
class Grid:

    grid: list[Tile] = []
    
    Winner = ""
    colorPlaying = "white"
    LegMove = []
    whiteChecked= False
    blackChecked = False
    clouages = []
    Wr = True
    Bwr = True
    Br = True
    Bbr = True
    def InitBoard(self):
        char = 1
        for i in range(64):
            
            if i%8 == 0:
                char += 1
            
            if char % 2 != 0:
                if i%2 == 0:
                    self.grid.append(Tile("none", str(char) +str(i%8 + 1), "black", "none"))
                else:
                    self.grid.append(Tile("none", str(char) +str(i%8 + 1), "white", "none"))
            else:
                if i%2 == 0:
                    self.grid.append(Tile("none", str(char) +str(i%8 + 1), "white", "none"))
                else:
                    self.grid.append(Tile("none", str(char) +str(i%8 + 1), "black", "none"))

        for i in range(4):
            for j in range(8):
                y = i
                if i >1:
                    y+=4
                    self.grid[y*8 + j].ColorPresent = "black"
                else:
                    self.grid[y*8+j].ColorPresent = "white"
                
                if(i == 1 or i == 2):
                    self.grid[y*8+j].PiecePresent = "Pa"
                    if i == 2:
                        self.grid[y*8+j].Symbol = "♙"
                    else:
                        self.grid[y*8+j].Symbol = "♟"

                else:
                    match j:
                        case 0 | 7:
                            self.grid[y*8+j].PiecePresent = "Ro"
                            if i == 3:
                                self.grid[y*8+j].Symbol = "♖"
                            else:
                                self.grid[y*8+j].Symbol = "♜"
                        case 1 | 6:
                            self.grid[y*8+j].PiecePresent = "Kn"
                            if i == 3:
                                self.grid[y*8+j].Symbol = "♘"
                            else:
                                self.grid[y*8+j].Symbol = "♞"
                        case 2 | 5:
                            self.grid[y*8+j].PiecePresent = "Bi"
                            if i == 3:
                                self.grid[y*8+j].Symbol = "♗"
                            else:
                                self.grid[y*8+j].Symbol = "♝"
                        case 3 :
                            self.grid[y*8+j].PiecePresent = "Ki"
                            if i == 3:
                                self.grid[y*8+j].Symbol = "♔"
                            else:
                                self.grid[y*8+j].Symbol = "♚"
                        case 4 :
                            self.grid[y*8+j].PiecePresent = "Qu"
                            if i == 3:
                                self.grid[y*8+j].Symbol = "♕"
                            else:
                                self.grid[y*8+j].Symbol = "♛"              
               

        
       
    
    def afficher(self, flip=False):
        stringR = ""
        tabL = ["A", "B", "C", "D", "E", "F", "G", "H"]
        
        rows = [self.grid[i*8:(i+1)*8] for i in range(8)]
        
        if flip:
            rows = list(reversed(rows))
            rows = [list(reversed(row)) for row in rows]
            tabL_display = tabL
        else:
            tabL_display = list(reversed(tabL)) 
        
        for col in tabL_display:
            stringR += "| " + col + " |"
        stringR += "\n"
        
        for i, row in enumerate(rows):
            rang = (8 - i) if flip else (i + 1)
            for tile in row:
                if tile.PiecePresent == "No":
                    stringR += "|   |"
                else:
                    stringR += "| " + tile.Symbol + " |"
            stringR += "| " + str(rang) + " |\n"
        
        return stringR

    def ResolveTile(self, move:str):

        if len(move) != 2:
            return None
        tabL = ["a", "b", "c", "d", "e", "f", "g", "h"]
        if move[0] not in tabL or int(move[1]) < 0 or int(move[1]) > 8:
            return None
        
     
        tabL.reverse()

        return self.GetTile(tabL.index(move[0]), int(move[1])-1)

    def GetTile(self, x, y):
        return x + y*8
    
    def GetEnnemies(self, color):
        ennemies = []
        for i in range(len(self.grid)):
            if self.grid[i].ColorPresent != color and self.grid[i].ColorPresent != "none":
                ennemies.append(i)
        return ennemies

    def CanMove(self, input, output):


        

        a = self.ResolveTile(input) if type(input) is str else input
        b = self.ResolveTile(output) if type(output) is str else output

        if len(self.LegMove) != 0 and ((self.whiteChecked and self.colorPlaying == "white") or (self.blackChecked and self.colorPlaying != "white")):
            found = False
            for i in range(len(self.LegMove)):
                if self.LegMove[i][0] == a and self.LegMove[i][1] == b:
                    found = True
                    break
            if found == False:
                return False
            
    

        if a == None or b == None:

            return False

        
        
        x0 = a%8 if a%8 >= 0 else -1
        y0 = floor(a/8) if floor(a/8) >= 0 and floor(a/8) < 8 else -1
        x1 = b%8 if b%8 >= 0 else -1
        y1 = floor(b/8) if floor(b/8) >= 0 and floor(b/8) < 8 else -1

        if self.grid[a].Pin != 0:
            
            found = False
            mechants = []
            for i in self.clouages:
                if i[1] == a:
                    mechants.append(i[0])
            
            for j in mechants:
                for i in self.drawLine(x0, y0, j%8, floor(j/8)):
                    if b == i:
                        found = True
            
            if not found:
                print("pinned by" + str(mechants))
                return False

        if(x0 == -1 or y0 == -1 or x1 == -1 or y1 == -1):

            return False
        
        piece = self.grid[self.GetTile(x0, y0)].PiecePresent


        if piece == "No":
            return False

        dx = x1-x0
        dy = y1-y0

        if dy ==0 and dx == 0:
            return False

        match piece:
            case "Ro":
                if not self.SolveRo(dx, dy):
                    return False
            case "Bi":

                if not self.SolveBi(dx, dy):
                    return False
            case "Qu":
                if not self.SolveQu(dx, dy):
                    return False
            case "Ki":

               
                if (dx == 2 or dx == -2 ) and dy == 0:
                    x2 = -1
                    y2 = -1
                    x3 = -1
                    y3 = -1
                    if self.grid[a].ColorPresent == "white":
                        x2 = 3
                        y2 = 0
                        x3 = 7 if dx == 2 else 0
                        y3 = 0
                        if dx == 2 and self.Wr == False:
                            
                            
                            return False
                        elif dx == -2 and self.Bwr == False:
                            
                            return False
                    if self.grid[a].ColorPresent == "black":
                        
                        x2 = 3
                        y2 = 7
                        x3 = 7 if dx == 2 else 0
                        y3 = 7
                        if dx == 2 and self.Bbr == False:
                           
                            return False
                        elif dx == -2 and self.Br == False:
                            
                            return False
                    pixels = self.drawLine(x2, y2, x3, y3)
                    
                    en = self.GetEnnemies(self.grid[pixels[0]].ColorPresent)
                    for enem in en:
                        if self.CanMove(enem, pixels[len(pixels)-2]) or self.CanMove(enem, pixels[len(pixels)-3]):
                            return False
                    for i in range(len(pixels)-2):
                        if self.grid[pixels[i+1]].PiecePresent != "No":
                            
                            return False
                    
                elif abs(dx)> 1 or abs(dy) > 1:
                    return False
                
                ennemies = self.GetEnnemies(self.grid[a].ColorPresent)
                for e in ennemies:
                    if self.CanMove(e, b):
                        return False
                
            case "Kn":
                if not self.SolveKn(dx, dy):
                    return False
            case "Pa":

                if (self.grid[a].ColorPresent == "white" and dy < 1) or ( self.grid[a].ColorPresent == "black" and dy > -1):

                    return False
                


                if abs(dx) == 1 and abs(dy) == 1:
                    if self.grid[b].PiecePresent == "No":
                        if self.grid[a].ColorPresent == "white":
                            
                            if self.grid[a].CanPassant != b-8:
                                return False
                            
                               

                        elif self.grid[a].ColorPresent == "black":
                            if self.grid[a].CanPassant != b+8:
                                return False
                            else:
                                self.grid[b+8].PiecePresent = "No"
                                self.grid[b+8].ColorPresent = "none"
                        else:
                            return False
                elif abs(dx) == 0:
                    match abs(dy):
                        case 1:
                            if self.grid[b].PiecePresent != "No":
                                return False
                        case 2:
                            if self.grid[b].PiecePresent != "No" or (self.grid[a].ColorPresent == "white" and floor(a/8) != 1) or (self.grid[a].ColorPresent == "black" and floor(a/8) != 6):
                                
                                return False
                            
                        case _ :

                            return False
                else:

                    return False
   
                            


        if self.grid[b].ColorPresent == self.grid[a].ColorPresent:

            return False
            




        if (piece != "Kn"):
            pixels = self.drawLine(x0, y0, x1, y1)
            if self.grid[a].ColorPresent == "black":
                pixels.reverse()
            for i in range(len(pixels)-2):
                if self.grid[pixels[i+1]].PiecePresent != "No":
                    return False

           

            return True
        
        return True
    
    def UpdateBoard(self, fromA:int, toB:int):
        tileA = self.grid[fromA]
        tileB = self.grid[toB]
        
        pieceToMove = tileA.PiecePresent
        colorOfPiece = tileA.ColorPresent
        SymbolOfPiece = tileA.Symbol
        tileA.PiecePresent = "No"
        tileA.ColorPresent = "none"
        tileA.Symbol = ""
        tileB.PiecePresent = pieceToMove
        tileB.ColorPresent = colorOfPiece
        tileB.Symbol = SymbolOfPiece
        kingC = None
        kingS = None
        self.LegMove = []
        for i in range(64):
            if self.grid[i].PiecePresent == "Ki" and self.grid[i].ColorPresent != self.colorPlaying:
                kingC = i
            elif self.grid[i].PiecePresent == "Ki" and self.grid[i].ColorPresent == self.colorPlaying:
                kingS = i
        self.whiteChecked = False
        self.blackChecked = False
        self.clouages = []
        for i in range(64):
            if self.grid[i].ColorPresent == tileB.ColorPresent:
                self.grid[i].Pin = 0
            else:
                self.grid[i].Pinning = -1
            

        



        if self.grid[toB].PiecePresent == "Pa":
            if abs(fromA-toB) == 16:
                if self.grid[toB + 1].ColorPresent != self.grid[toB].ColorPresent and floor((toB+1)/8) == floor(toB/8):
                   
                    self.grid[toB + 1].CanPassant = toB
                if self.grid[toB - 1].ColorPresent != self.grid[toB].ColorPresent and floor((toB-1)/8) == floor(toB/8):
                   
                    self.grid[toB - 1].CanPassant = toB

            if abs(fromA%8-toB%8) == 1 and abs(floor(fromA/8)-floor(toB/8)) == 1:
                if self.grid[toB].ColorPresent == "white":
                    
                    if self.grid[fromA].CanPassant == toB-8:
                        self.grid[toB-8].PiecePresent = "No"
                        self.grid[toB-8].ColorPresent = "none"
                        
                            

                elif self.grid[toB].ColorPresent == "black":
                    if self.grid[fromA].CanPassant == toB+8:
                        self.grid[toB+8].PiecePresent = "No"
                        self.grid[toB+8].ColorPresent = "none"
            
            if tileB.ColorPresent == "black" and floor(toB/8) == 0:
                tileB.PiecePresent = "Qu"
                tileB.Symbol = "♕"
               
            if tileB.ColorPresent == "white" and floor(toB/8) == 7:
                tileB.PiecePresent = "Qu"
                tileB.Symbol = "♛"
                    

        if self.grid[toB].PiecePresent == "Ki":
            if self.grid[toB].ColorPresent == "white":
                self.Wr = False
                self.Bwr = False
            elif self.grid[toB].ColorPresent == "black":
                self.Br = False
                self.Bbr = False
        if self.grid[toB].PiecePresent == "Ro":
            if self.grid[toB].ColorPresent == "white":
                if self.grid[fromA].TileName == 0:
                    self.BWr = False
                elif self.grid[fromA].TileName == 7:
                    self.Wr = False
            else:
                if self.grid[toB].ColorPresent == "black":
                    if self.grid[fromA].TileName == 54:
                        self.Bbr = False
                    elif self.grid[fromA].TileName == 63:
                        self.Br = False

        x0 = toB%8
        y0 = floor(toB/8) 
        x1 = kingC%8 
        y1 = floor(kingC/8)


        LoS = self.drawLine(x0, y0, x1, y1)
        self.CheckPins(kingS)
        print(toB, kingC)
        if self.CheckCheck(toB, kingC):
            print("atteint")
            if str(self.grid[kingC].ColorPresent) != "none":
                if(self.CheckCheckMate(kingC, LoS)):
                    self.Winner = "fin"
                    print("CheckMate")
                    return
            
            print("lmove", str(self.LegMove))

        if abs(fromA-toB) == 2 and self.grid[toB].PiecePresent == "Ki":
            if self.grid[toB].ColorPresent == "black":
                self.Bbr = False
                self.Br = False
                if fromA-toB == 2:
                    self.UpdateBoard(56, 58)
                    
                    
                else:
                    self.UpdateBoard(63, 60)
            elif self.grid[toB].ColorPresent == "white":
                self.Wr = False
                self.Bwr = False
                if fromA-toB == 2:
                    self.UpdateBoard(0, 2)
                else:
                    self.UpdateBoard(7, 4)

        if self.colorPlaying == "white":
            self.colorPlaying = "black"
        else:
            self.colorPlaying = "white"

        tileA.CanPassant = -1
        tileB.CanPassant = -1
        self.afficher()

    def CheckPins(self, king:int):
        ennemies = self.GetEnnemies(self.grid[king].ColorPresent)
        for en in ennemies:
            self.CheckCheck(en, king)

    def CheckCheck(self, A: int, king:int):

        if self.grid[A].PiecePresent == "Ki":
            return False

        if A == king:
            return False
        if self.grid[A].ColorPresent == self.grid[king].ColorPresent:
            return False

        tileA = self.grid[A]
        
        
        x0 = A%8
        y0 = floor(A/8) 
        x1 = king%8 
        y1 = floor(king/8)
        dx = x1-x0
        dy = y1-y0

        LoS = self.drawLine(x0, y0, x1, y1)
        if len(LoS) == 0:
            return True
        match tileA.PiecePresent:
            case "Ro":
                if not self.SolveRo(dx, dy):
                    return False
            case "Bi":
                if not self.SolveBi(dx, dy):
                    return False
            case "Qu":

                if not self.SolveQu(dx, dy):
                    return False
            case "Kn":
                if not self.SolveKn(dx, dy):
                    return False
            case "Pa":
                if tileA.ColorPresent == "white":
                    if not ((dx == 1) and (dy == 1)):
                        
                        return False
                else:
                    if not ((dx == -1) and (dy == -1)):
                        return False
        
        
        nbP = 0
        if tileA.PiecePresent not in ["Kn", "Ki", "Pa"]:
            if self.grid[A].ColorPresent == "black":
                LoS.reverse()

            
            p = []
            for i in LoS:
                if self.grid[i].PiecePresent != "No" and i not in [king, A]:
                    p.append(i)
                    nbP += 1
        if nbP == 0:
            c = king
            assert c is not None
            print("Check on "+ str(self.grid[c].ColorPresent)+" king from " + str(LoS[0]))

            if str(self.grid[c].ColorPresent) == "white":
                self.whiteChecked = True
            elif str(self.grid[c].ColorPresent) == "black":
                self.blackChecked = True
            return True
        elif nbP ==1:
            self.grid[p[0]].Pin += 1
            self.grid[A].Pinning = p[0]
            
            if (A, p[0]) not in self.clouages:
                self.clouages.append((A, p[0]))
           
            return False
        else:

            return False
        


    def CheckCheckMate(self, king: int, LoS):
        
        cases = [king-1, king+1, king+8, king-8, king+9, king-9, king+7, king-7]
        print("king : "+str(king))
        print(cases)

        for c in cases:
            
            if self.CanMove(king, c):
                print("king can move to "+ str(c))
                self.LegMove.append((king, c))
                
            
        pieces = self.GetEnnemies("white") if self.grid[king].ColorPresent == "black" else self.GetEnnemies("black")
        
     
        if self.grid[LoS[len(LoS)-1]].PiecePresent == "Kn":
            for piece in pieces:
                if self.CanMove(piece, LoS[len(LoS)-1]):  
                    print("piece "+ str(piece) + " can move to "+ str(p))
                    self.LegMove.append((piece, p))
        else:
            for p in LoS:
                for piece in pieces:

                    if self.CanMove(piece, p):  
                        print("piece "+ str(piece) + " can move to "+ str(p))
                        self.LegMove.append((piece, p))
    
        
        if len(self.LegMove) != 0:
            return False
        
        return True

            
            
    def SolveKn(self, dx, dy):
        return ((abs(dx) == 2 and abs(dy) == 1) or (abs(dx) == 1 and abs(dy) == 2))
            
    def SolveQu(self, dx, dy):
        return self.SolveBi(dx, dy) or self.SolveRo(dx, dy)
    
    def SolveRo(self, dIn, dOu):
        return not (dIn != 0 and dOu != 0)
    
    def SolveBi(self, dIn, dOu):

        return abs(dIn) == abs(dOu)
    
    def drawLine(self, x0, y0, x1, y1):
        if abs(x1-x0) > abs(y1-y0):
            return self.drawLineH(x0, y0, x1, y1)
        else:
            return self.drawLineV(x0, y0, x1, y1)

    def drawLineH(self, x0, y0, x1, y1):
        pixels = []
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dx = x1-x0
        dy = y1-y0

        dir = -1 if dy < 0 else 1
        dy *= dir

        if dx != 0:
            y = y0
            p = 2*dy - dx
            for i in range(dx + 1):
                pixels.append(self.GetTile(x0+i, y))
                if p >= 0:
                    y+= dir
                    p = p -2*dx
                p = p+2*dy
        return pixels
    
    def drawLineV(self, x0, y0, x1, y1):
        pixels = []
        if y0 > y1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dx = x1-x0
        dy = y1-y0

        dir = -1 if dx < 0 else 1
        dx *= dir

        if dy != 0:
            x = x0
            p = 2*dx - dy
            for i in range(dy + 1):
                pixels.append(self.GetTile(x,i+ y0))
                if p >= 0:
                    x+= dir
                    p = p -2*dy
                p = p+2*dx
        return pixels

    def AskPlayer(self):
        while True:
            print("les "+self.colorPlaying+" jouent :")
            inp = input("quelle pièce voulez vous bouger ?")
            if inp == "stop":
                self.Winner = "stop"
                print("partie stoppée")
                break
            out = input("sur quelle case voulez vous l'emmener ?")

            

            if self.ResolveTile(inp) == None or self.ResolveTile(out) == None:
                print("coup illégal veuillez renseigner des coups valides")
                
            else:
                res = self.ResolveTile(inp)
                assert res is not None

                if self.grid[res].ColorPresent != self.colorPlaying:
                    print("Jouez un coup avec vos pièces")
                elif self.CanMove(inp, out) == False:
                    print("coup illégal veuillez renseigner des coups valides")
                else:
                    if (self.CanMove(inp, out)):
                        self.UpdateBoard(self.ResolveTile(inp), self.ResolveTile(out))
                    
                    break
            
            self.afficher()

    def LaunchGame(self):
        while self.Winner == "":
            self.AskPlayer()