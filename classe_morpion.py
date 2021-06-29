########################################
#
# Classes servant pour le jeu du Morpion :
# - Grille
# - Tour
# - Partie
# - Arbre
#
########################################

import random


########################################
# Grille représente une grille 3x3 sur
# laquelle se joue le Morpion
# Si une case est libre elle contient un
# 0, si le joueur 1 la remplie elle contient
# un 1, pour le joueur 2 il s'agit d'un 2

class Grille():

    def __init__(self):
        """Instanciation de la grille remplie de 0"""
        self.grille = []
        for i in range(3):
            self.grille.append([0, 0, 0])
            
    def ajoute(self, x, y, joueur):
        """Ajoute le tour d'un joueur : 1 ou 2"""
        if (x <= 2 and x >= 0 and
            y <= 2 and y >= 0 and
            (joueur == 1 or joueur == 2)):
            self.grille[x][y] = joueur
            
    def __str__(self):
        """Affiche la grille"""
        txt = ""
        for i in range(3):
            if i == 1 or i == 2:
                txt += "\n----------\n"
            for j in range(3):
                txt += str(self.grille[j][2-i])
                if j == 0 or j == 1:
                    txt += " | "
        txt = txt.replace("0", " ")
        txt = txt.replace("1", "X")
        txt = txt.replace("2", "O")
        return txt+"\n"

    def case(self, x, y):
        """Retourne le joueur qui a rempli une case"""
        return self.grille[x][y]

    def nbr_tours(self):
        """Retourne le nombre de tours"""
        nbr_tours = 0
        for i in range(3):
            for j in range(3):
                if self.grille[i][j] != 0:
                    nbr_tours += 1
        return nbr_tours

    def vainqueur(self):
        """Test si la partie a un vainqueur.
        Comme la grille est remplie de nombre et non
        de croix, cercle et vide, on multiplie le
        contenu des cases pour savoir s'il y a un vainqueur.
        Le résultat 1 signifie trois 1 d'alignés alors que 8
        implique trois deux d'alignés. Sinon, le résultat serait
        0. Cette fonction retourne le numéro du vainqueur 1 ou 2.
        S'il n'y a pas de vainqueur retourne 0."""
        
        if (self.grille[0][0]*self.grille[0][1]*self.grille[0][2] == 1 or
            self.grille[1][0]*self.grille[1][1]*self.grille[1][2] == 1 or
            self.grille[2][0]*self.grille[2][1]*self.grille[2][2] == 1 or
            self.grille[0][0]*self.grille[1][0]*self.grille[2][0] == 1 or
            self.grille[0][1]*self.grille[1][1]*self.grille[2][1] == 1 or
            self.grille[0][2]*self.grille[1][2]*self.grille[2][2] == 1 or
            self.grille[0][0]*self.grille[1][1]*self.grille[2][2] == 1 or
            self.grille[0][2]*self.grille[1][1]*self.grille[2][0] == 1):
            return 1
        elif (self.grille[0][0]*self.grille[0][1]*self.grille[0][2] == 8 or
            self.grille[1][0]*self.grille[1][1]*self.grille[1][2] == 8 or
            self.grille[2][0]*self.grille[2][1]*self.grille[2][2] == 8 or
            self.grille[0][0]*self.grille[1][0]*self.grille[2][0] == 8 or
            self.grille[0][1]*self.grille[1][1]*self.grille[2][1] == 8 or
            self.grille[0][2]*self.grille[1][2]*self.grille[2][2] == 8 or
            self.grille[0][0]*self.grille[1][1]*self.grille[2][2] == 8 or
            self.grille[0][2]*self.grille[1][1]*self.grille[2][0] == 8):
            return 2
        else:
            return 0

    def copier(self):
        """Retourne une grille copiée"""
        # Instanciation d'une nouvelle grille
        grille_copiee = Grille()

        for i in range(3):
            for j in range(3):
                grille_copiee.grille[i][j] = self.grille[i][j]

        return grille_copiee

    ###########
    # Rotation et symétrie de grille
    
    def tourner90(self):
        """Tourne de 90 degrés la grille du morpion"""
        grille_copie = self.copier()
        for i in range(3):
            for j in range(3):
                #tour.x, tour.y = -(tour.y-1)+1, (tour.x-1)+1
                self.grille[-j+2][i] = grille_copie.grille[i][j]
            
    def tourner180(self):
        """Tourne de 180 degrés la grille du morpion"""
        self.tourner90()
        self.tourner90()

    def tourner270(self):
        """Tourne de 270 degrés la grille du morpion"""
        self.tourner180()
        self.tourner90()

    def symetriser1(self):
        """Symétrise la partie suivant la deuxième diagonale"""
        grille_copie = self.copier()
        for i in range(3):
            for j in range(3):
                self.grille[j][i] = grille_copie.grille[i][j]
        
    def symetriser2(self):
        """Symétriser puis tourner de 90 degrés"""
        self.symetriser1()
        self.tourner90()

    def symetriser3(self):
        """Symétriser puis tourner de 180 degrés"""
        self.symetriser1()
        self.tourner180()

    def symetriser4(self):
        """Symétriser puis tourner de 270 degrés"""
        self.symetriser1()
        self.tourner270()
        
    def __eq__(self, grille):
        
        """Vérifie que deux grilles sont équivalentes."""
        grille_tmp = grille.copier()
        if self.grille == grille_tmp.grille:
            return 1
        grille_tmp.tourner90()
        if self.grille == grille_tmp.grille:
            return 1
        grille_tmp.tourner90()
        if self.grille == grille_tmp.grille:
            return 1
        grille_tmp.tourner90()
        if self.grille == grille_tmp.grille:
            return 1
        grille_tmp.symetriser1()
        if self.grille == grille_tmp.grille:
            return 1
        grille_tmp.tourner90()
        if self.grille == grille_tmp.grille:
            return 1
        grille_tmp.tourner90()
        if self.grille == grille_tmp.grille:
            return 1
        grille_tmp.tourner90()
        if self.grille == grille_tmp.grille:
            return 1

        return 0

    def __in__(self, grilles):
        """Vérifie qu'une grille ou une de ses équivalente sont
        dans une suite de grille"""
        for grille in grilles:
            if self == grille:
                return 1
        return 0


########################################
# Tour est la classe représentant chaque
# tour de jeu, donc les coordonnées de la
# case qui vient d'être joués, le numéro
# du joueur 1 ou 2 et le numéro du tour.

class Tour():
    
    def __init__(self, x=1, y=1, joueur=1, numero=1):
        """Instanciation d'un objet Tour"""
        if (x < 3 and x >= 0 and
            y < 3 and y >= 0 ):
            self.x = x
            self.y = y
        else :
            self.x = x
            self.y = y
        if (joueur < 3 and joueur > 0):
            self.joueur = joueur
        else:
            self.joueur = joueur
        if (numero > 0 and numero < 10):
            self.numero = numero
        else:
            self.numero = numero
    def __eq__(self, tour):
        test = (self.x == tour.x and
                self.y == tour.y and
                self.joueur == tour.joueur and
                self.numero == tour.numero)
        return test
            
    def __str__(self):
        """Affiche un tour"""
        txt = "Tour "+str(self.numero)+" du joueur "+str(self.joueur)+\
            " sur la case "+str(self.x)+str(" ")+str(self.y)+\
            "\n"
        return txt


########################################
# Partie_Morpion est la classe représentant
# un jeu en tran de se dérouler. C'est donc
# une suite ordonnée de Tour. De plus, il y
# a une représentation graphique et instantané
# de la partie avec une grille représentant
# le jeu au dernier tour. Cette grille n'a pas
# la mémoire de l'ordre des tours.
#
# La grille est remplie de 0, 1 ou 2. Le nombre
# 0 correspond à une case vide, 1 à un tour du
# premier joueur et 2 du second.
#
# grille[x][y], correspond à la case d'ordonnée
# x et d'abscisse y.

class Partie():
    
    def __init__(self):
        """Instanciation d'un objet Partie"""
        self.tours = []
        self.grille = Grille()
        
    def nouveau_tour(self, tour):
        """Ajoute un nouveau tour dans la partie seulement
        si la case est libre donc contient 0."""
        # Teste si la case est libre
        if self.grille.case(tour.x, tour.y) == 0:
            nbr_tour = len(self.tours)+1 # Calcul du nombre de tour
            tour.numero = nbr_tour
            if nbr_tour%2 == 1:          # Décide du joueur du tour
                tour.joueur = 1
            else:
                tour.joueur = 2
            self.tours.append(tour)      # Ajoute le tour
            self.grille.ajoute(tour.x, tour.y, tour.joueur) # Actualise la case

    def copier(partie):
        """Copie la partie dans un autre objet"""
        # Instanciation d'une nouvelle partie
        partie_copiee = Partie()

        for tour in partie.tours:
            tour_tmp = Tour(tour.x, tour.y) # Instanciation d'un tour
            partie_copiee.nouveau_tour(tour_tmp) # Ajout du tour

        return partie_copiee


    def __str__(self):
        """Affiche une partie en cours avec l'ordre des tours"""
        txt = "\n"
        for tour in self.tours:
            txt += str(tour)
        return txt

    def tourner90(self):
        """Tourne de 90 degrés la grille du morpion d'une partie"""
        for tour in self.tours:
            #tour.x, tour.y = -(tour.y-2)+2, (tour.x-2)+2
            tour.x, tour.y = -tour.y+2, tour.x
        self.grille.tourner90()
            
    def tourner180(self):
        """Tourne de 180 degrés la grille du morpion"""
        self.tourner90()
        self.tourner90()

    def tourner270(self):
        """Tourne de 270 degrés la grille du morpion"""
        self.tourner180()
        self.tourner90()

    def symetriser1(self):
        """Symétrise la partie suivant la deuxième diagonale"""
        for tour in self.tours:
            tour.x, tour.y = tour.y, tour.x
        self.grille.symetriser1()
        
    def symetriser2(self):
        """Symétriser puis tourner de 90 degrés"""
        self.symetriser1()
        self.tourner90()

    def symetriser3(self):
        """Symétriser puis tourner de 180 degrés"""
        self.symetriser1()
        self.tourner180()

    def symetriser4(self):
        """Symétriser puis tourner de 270 degrés"""
        self.symetriser1()
        self.tourner270()
        
    def egal(self, partie):
        """Test si deux parties sont identiques"""
        if len(self.tours) != len(partie.tours):
            return False

        for numero in range(len(self.tours)):
            if self.tours[numero] != partie.tours[numero]:
                return False

        return True
            
    def __eq__(self, partie):
        """Test si deux parties sont équivalentes.
        On test si une transformation de partie est égale à self.
        Il faut copier partie sinon on la transforme.
        De nouveau, l'équivalence tient compte de l'ordre des tours,
        il ne suffit pas que deux grilles soit équivalente il faut
        aussi que les tours soient dans le bon ordre."""
        partie_tmp = Partie.copier(partie)
        if self.egal(partie_tmp):
            return True
        partie_tmp.tourner90()
        if self.egal(partie_tmp):
            return True
        partie_tmp.tourner90()
        if self.egal(partie_tmp):
            return True
        partie_tmp.tourner90()
        if self.egal(partie_tmp):
            return True
        partie_tmp.symetriser1()
        if self.egal(partie_tmp):
            return True
        partie_tmp.tourner90()
        if self.egal(partie_tmp):
            return True
        partie_tmp.tourner90()
        if self.egal(partie_tmp):
            return True
        partie_tmp.tourner90()
        if self.egal(partie_tmp):
            return True

        return False

    def __in__(self, parties):
        """Vérifie qu'une partie est dans une suite de partie"""
        for partie in parties:
            if self == partie:
                return True
        return False

    
########################################
# La classe Arbre sert à représenter les
# arbres informatiques qui listent les
# différentes parties.

class Arbre():

    def __init__(self, partie):
        """Instancie une feuille d'un arbre"""
        self.ID = 0
        self.nbr_noeuds = 1
        self.nbr_feuilles = 1
        self.partie = partie
        self.nbr_fils = 0
        self.fils = []

    def __str__(self):
        txt = "\n"+str(self.ID)+"\n"+str(self.partie.grille)
        for fils in self.fils:
            txt += str(fils)
        return txt
    
    def copier(self):
        arbre_copie = Arbre(self.partie)
        liste_fils = []
        for fils in self.fils:
            fils_copie = fils.copier()
            #self.nbr_noeuds += fils_copie.nbr_noeuds
            #self.nbr_feuilles += fils_copie.nbr_feuilles
            #self.nbr_fils += fils_copie.nbr_fils
            liste_fils += [fils_copie]
        arbre_copie.enraciner(liste_fils)
        return arbre_copie
        
    def enraciner(self, arbres):
        """Fait un arbre à partir d'une racine et 
        d'une liste d'arbres fils"""
        ID = 0
        self.nbr_feuilles = 0
        self.ID = ID
        ID += 1
        for arbre in arbres:
            self.nbr_noeuds += arbre.nbr_noeuds
            self.nbr_feuilles += arbre.nbr_feuilles
            arbre.ID = ID
            ID += 1
            
        self.nbr_fils = len(arbres)
        self.fils = arbres
        
    def lister_feuilles(self, vainqueur, nbr_tours):
        """Une fois qu'un arbre est générer, on peut vouloir connaître
        son nombre de feuille. De plus on peut choisir les feuilles, donc
        les parties qui sont gagnées par un joueur spécifique et en 
        un certain nombre de tours."""
        # On teste d'abord le nombre de parties filles de l'arbre.
        # Si ce nombre est nul, cela correspond à une feuille.
        # On vérifie le vainqueur et le nombre de tours avant de
        # conserver la feuille.
        # Si ce n'est pas une feuille, par récurrence,
        # on vérifie les arbres fils.
        if self.nbr_fils == 0:
            if (vainqueur == -1 and nbr_tours == -1):
                return [self.partie]
            elif (vainqueur == -1 and nbr_tours == len(self.partie.tours)):
                return [self.partie]
            elif (self.partie.grille.vainqueur() == vainqueur
                  and nbr_tours == -1):
                return [self.partie]
            elif (self.partie.grille.vainqueur() == vainqueur and
                  nbr_tours == len(self.partie.tours)):
                return [self.partie]
            else:
                return []
        else:
            liste_feuilles = []
            for i in range(self.nbr_fils):
                liste_tmp = self.fils[i].lister_feuilles(vainqueur, nbr_tours)
                liste_feuilles += liste_tmp
            return liste_feuilles
    
    def lister_feuilles_2(self, vainqueur, nbr_tours):
        """Identique à la fonction lister_feuilles mais ici on ne garde
        pas deux feuilles qui ont des grilles équivalentes."""
        if self.nbr_fils == 0:
            if (vainqueur == -1 and nbr_tours == -1):
                return [self.partie]
            elif (vainqueur == -1 and nbr_tours == len(self.partie.tours)):
                return [self.partie]
            elif (self.partie.grille.vainqueur() == vainqueur and
                  nbr_tours == -1):
                return [self.partie]
            elif (self.partie.grille.vainqueur() == vainqueur and
                  nbr_tours == len(self.partie.tours)):
                return [self.partie]
            else:
                return []
        else:
            liste_feuilles = []
            for i in range(self.nbr_fils):
                liste_tmp = self.fils[i].lister_feuilles_2(vainqueur,
                                                           nbr_tours)
                for feuille in liste_tmp:
                    # On teste si la grille de la partie est équivalente
                    # à une autre. Si oui, on ne prend pas la partie.
                    if feuille in liste_feuilles:
                        liste_feuilles += [feuille]
            return liste_feuilles
        
    
########################################
# Test les classes

if __name__ == "__main__":

    # Test la classe grille
    print("TESTS de la classe Grille")
    grille1 = Grille()
    grille1.ajoute(0, 0, 1)
    grille1.ajoute(1, 1, 2)
    grille1.ajoute(1, 0, 1)
    grille1.ajoute(2, 2, 2)

    grille2 = grille1.copier()
    grille2.ajoute(0, 2, 1)
    grille2_copie = grille2.copier()

    print(grille2)

    print("Valeur case 2, 2: ", grille2.case(2, 2))

    print("Nbr tours : ", grille2.nbr_tours())
    print("Vainqueur: ", grille2.vainqueur())
    grille2.tourner90()
    print("Tourner 90 :\n", grille2)
    grille2.symetriser1()
    print("Puis symetriser : \n", grille2)
    
    print("Copie grille 2 avant transformation :\n", grille2_copie)
    print("Equivalent : ", grille2 == grille2_copie)
    
    grilles = []
    grilles += [grille1]
    grilles += [grille2]
    grilles += [grille2_copie]
    print(grilles)
    print("Dedans : ", grille2 in grilles)


    # Test la classe Tour
    print("\n\nTESTS de la classe Tour")
    tour1 = Tour()
    tour1.x=2
    tour1.y=1
    print(tour1)
    tour2 = Tour()
    print("Test d'égalité", tour2 == tour1)
    
    # Test la classe Partie
    print("\n\nTESTS de la classe Partie")
    partie1 = Partie()

    tour_tmp = Tour(1, 2)
    partie1.nouveau_tour(tour_tmp)
    tour_tmp = Tour(1, 1)
    partie1.nouveau_tour(tour_tmp)
    print("Partie 1 : ", partie1)
    
    partie2 = Partie()
    partie2 = Partie.copier(partie1)
    tour_tmp = Tour(0, 0)
    partie2.nouveau_tour(tour_tmp)
    print("Partie 2 : ", partie2)
    print(partie2.grille)
    partie3 = Partie.copier(partie2)
    partie3.tourner270()
    print("Rot 270 Partie 2 : ", partie3)
    print(partie3.grille)
    
    print("Test équivalence")

    print("TEST equivalence partie1 partie2", partie2 == partie3)

    #Test de la classe Arbre
    print("TEST de la classe Arbre")
    arbre1 = Arbre(partie1)
    arbre2 = Arbre(partie2)
    arbre3 = Arbre(partie3)
    arbre1.enraciner([arbre2.copier(), arbre3.copier()])
    print("Arbre 2 : \n", arbre2)
    print("Arbre 3 : \n", arbre3)
    print("Arbre 1 : \n", arbre1)

    liste_feuilles = arbre1.lister_feuilles(1, -1)
    liste_feuilles = arbre1.lister_feuilles_2(1, -1)
