from classe_morpion import *
from generation_arbre import *

###################
# Intelligence artificielle
    
def IA_1(grille):
    """Intelligence artificielle basique pour le jeu du Morpion.
    Elle joue aléatoirement dans les cases libres"""
    
    liste_cases_vides = []  # On initialise la liste des cases vides

    # On regarde chaque case de la grille pour savoir si elle est vide
    # Si oui, on la range dans liste_cases_vides
    for i in range(3):
        for j in range(3):
            if grille.case(i, j) == 0:
                liste_cases_vides.append([i, j])

    # On utilise la bibliothèque random pour choisir une case dans
    # la liste des cases vides
    nbr_cases_vides = len(liste_cases_vides)
    numero_case_vide = random.randint(0, nbr_cases_vides-1)
    case_vide = liste_cases_vides[numero_case_vide]
    
    # On retourne la case vide
    return case_vide


def test_alignement(alignement, joueur):
    """test_alignement étudie un alignement (ligne, colonne ou diagonale) 
    pour savoir si un joueur est en mesure de gagner et avec quelle case"""
    # la liste nbr conserve le nombre de 0 de 1 et de 2
    # On regarde chaque élément d'alignement et on augmente dans nbr
    # le nombre de l'élément trouvé
    nbr_joueur = alignement.count(joueur)
    nbr_vide   = alignement.count(0)
    
    if nbr_vide == 1 and nbr_joueur == 2:
        return (1, alignement.index(0))
    else:
        return (0, 0)

    
def test_gagner(grille, joueur):
    """Test si un joueur peut gagner, si oui donne la case"""
    # Sur une ligne
    for i in range(3):
        gagnant, numero = test_alignement([grille.case(i, 0),
                                           grille.case(i, 1),
                                           grille.case(i, 2)], joueur)
        if gagnant == 1:
            return [i, numero]
    # Sur une colonne
    for i in range(3):
        gagnant, numero = test_alignement([grille.case(0, i),
                                           grille.case(1, i),
                                           grille.case(2, i)], joueur)
        if gagnant == 1:
            return [numero, i]
    # Sur une diagonale
    gagnant, numero = test_alignement([grille.case(0, 0),
                                       grille.case(1, 1),
                                       grille.case(2, 2)], joueur)
    if gagnant == 1:
        return [numero, numero]
    gagnant, numero = test_alignement([grille.case(0, 2),
                                       grille.case(1, 1),
                                       grille.case(2, 0)], joueur)
    if gagnant == 1:
        return [numero, 2-numero]
    
    return []
    
                    
def IA_2(grille, joueur):
    """IA_2 est le niveau 2 de l'intelligence artificielle 
    au jeu du Morpion."""

    # On commence par tester si joueur peut gagner
    case = test_gagner(grille, joueur)
    if len(case) != 0:
        return case

    # Puis si l'autre joueur peut gagner
    if joueur == 1:
        joueur2 = 2
    else:
        joueur2 = 1

    case = test_gagner(grille, joueur2)
    if len(case) != 0:
        return case

    # Sinon, l'IA joue au hasard en reprenant l'ancien programme IA_1
    case = IA_1(grille)
    return case

def IA_3(partie, arbre):
    pass

def IA_1_vs_IA_1(nbr_parties):
    """Test les chances de succès et d'echec
    de IA_1 contre lui-même"""
    nbr_victoire_1 = 0
    nbr_victoire_2 = 0
    nbr_match_nul  = 0
    
    for numero_partie in range(nbr_parties):
        #print("Partie : ", numero_partie)
        partie_tmp = Partie()
        while (partie_tmp.grille.vainqueur() == 0
               and partie_tmp.grille.nbr_tours() < 9):
            x, y = IA_1(partie_tmp.grille)
            tour_tmp = Tour(x, y)
            partie_tmp.nouveau_tour(tour_tmp)
            #print(partie_tmp.grille)
        if partie_tmp.grille.vainqueur() == 1:
            nbr_victoire_1 += 1
        elif partie_tmp.grille.vainqueur() == 2:
            nbr_victoire_2 += 1
        else:
            nbr_match_nul += 1

    print("% de victoire nul, 1, 2 : ",
          nbr_match_nul/nbr_parties*100,
          nbr_victoire_1/nbr_parties*100,
          nbr_victoire_2/nbr_parties*100)
        
def IA_1_vs_IA_2(nbr_parties):
    """Test les chances de succès et d'echec
    de IA_1 contre IA_2"""
    nbr_victoire_IA_1 = 0
    nbr_victoire_IA_2 = 0
    nbr_match_nul     = 0
    
    for numero_partie in range(nbr_parties):
        #print("Partie : ", numero_partie)
        IA_2_joueur = numero_partie%2+1
        partie_tmp = Partie()

        while (partie_tmp.grille.vainqueur() == 0
               and partie_tmp.grille.nbr_tours() < 9):
            if partie_tmp.grille.nbr_tours()%2 == 0:
                if IA_2_joueur == 1:
                    x, y = IA_2(partie_tmp.grille, IA_2_joueur)
                    tour_tmp = Tour(x, y)
                    partie_tmp.nouveau_tour(tour_tmp)
                else:
                    x, y = IA_1(partie_tmp.grille)
                    tour_tmp = Tour(x, y)
                    partie_tmp.nouveau_tour(tour_tmp)
            else:
                if IA_2_joueur == 2:
                    x, y = IA_2(partie_tmp.grille, IA_2_joueur)
                    tour_tmp = Tour(x, y)
                    partie_tmp.nouveau_tour(tour_tmp)
                else:
                    x, y = IA_1(partie_tmp.grille)
                    tour_tmp = Tour(x, y)
                    partie_tmp.nouveau_tour(tour_tmp)
            #print(partie_tmp.grille)

        if partie_tmp.grille.vainqueur() == 1:
            if IA_2_joueur == 1:
                nbr_victoire_IA_2 += 1
            else:
                nbr_victoire_IA_1 += 1
        elif partie_tmp.grille.vainqueur() == 2:
            if IA_2_joueur == 2:
                nbr_victoire_IA_2 += 1
            else:
                nbr_victoire_IA_1 += 1
        else:
            nbr_match_nul += 1
            
    print("% de victoire nul, 1, 2 : ",
          nbr_match_nul/nbr_parties*100,
          nbr_victoire_IA_1/nbr_parties*100,
          nbr_victoire_IA_2/nbr_parties*100)

def IA_2_vs_IA_3(nbr_parties):
    """Test les chances de succès et d'echec
    de IA_2 contre IA_3"""
    nbr_victoire_IA_2 = 0
    nbr_victoire_IA_3 = 0
    nbr_match_nul     = 0

    # Génération de l'arbre pour IA_3
    partie = Partie()
    print(partie.grille)
    print("Génération vainqueur 1")
    arbre_vainqueur_1 = generer_arbre_vainqueur_1(partie)
    print("Génération vainqueur 2")
    arbre_vainqueur_2 = generer_arbre_vainqueur_2(partie)
    
    for numero_partie in range(nbr_parties):
        print("Partie : ", numero_partie)
        IA_2_joueur = numero_partie%2+1
        partie_tmp  = Partie()
        if IA_2_joueur == 1:
            arbre_tmp   = arbre_vainqueur_2
        else:
            arbre_tmp   = arbre_vainqueur_1
        
        nombre_tour = 0
        while (partie_tmp.grille.vainqueur() == 0
               and partie_tmp.grille.nbr_tours() < 9):
            print("Tour : ", nombre_tour)
            nombre_tour += 1
            # Tour pair donc le joueur 1 joue
            if partie_tmp.grille.nbr_tours()%2 == 0:
                if IA_2_joueur == 1:
                    #print("IA_2 joue pair")
                    x, y = IA_2(partie_tmp.grille, IA_2_joueur)
                    tour_tmp = Tour(x, y)
                    partie_tmp.nouveau_tour(tour_tmp)
                    #print("Partie après le tour de IA_2 pair")
                    #print(partie_tmp.grille)
                    for fils in arbre_tmp.fils:
                        partie_fille = fils.partie
                        if partie_fille.egal(partie_tmp):
                            #print("EGALITE")
                            #print(partie_fille)
                            arbre_tmp = fils
                            break
                    #print("Partie de l'arbre fils")
                    #print(arbre_tmp.partie.grille)
                else:
                    #print("IA_3 joue pair")
                    partie_tmp = arbre_tmp.fils[0].partie
                    #print(partie_tmp.grille)
                    arbre_tmp = arbre_tmp.fils[0]
            # Tour impair donc le joueur 2 joue
            else:
                if IA_2_joueur == 2:
                    #print("IA_2 joue impair")
                    x, y = IA_2(partie_tmp.grille, IA_2_joueur)
                    tour_tmp = Tour(x, y)
                    partie_tmp.nouveau_tour(tour_tmp)
                    for fils in arbre_tmp.fils:
                        partie_fille = fils.partie
                        if partie_fille.egal(partie_tmp):
                            arbre_tmp = fils
                            break
                else:
                    #print("IA_3 joue impair")
                    #print("Avant IA_3 joue partie_tmp arbre_tmp.partie")
                    #print(partie_tmp.grille)
                    #print(arbre_tmp.partie.grille)
                    partie_tmp = arbre_tmp.fils[0].partie
                    #print("Après IA_3 joue")
                    #print(partie_tmp.grille)
                    arbre_tmp = arbre_tmp.fils[0]
            # Affiche la grille en cours
            print("FIN DU TOUR")
            print(partie_tmp.grille)

                    
        if partie_tmp.grille.vainqueur() == 1:
            if IA_2_joueur == 1:
                nbr_victoire_IA_2 += 1
            else:
                nbr_victoire_IA_3 += 1
        elif partie_tmp.grille.vainqueur() == 2:
            if IA_2_joueur == 2:
                nbr_victoire_IA_2 += 1
            else:
                nbr_victoire_IA_3 += 1
        else:
            nbr_match_nul += 1
            
    print("% de victoire nul, 2, 3 : ",
          nbr_match_nul/nbr_parties*100,
          nbr_victoire_IA_2/nbr_parties*100,
          nbr_victoire_IA_3/nbr_parties*100)

        
########################################
# Test du programme

if __name__ == "__main__":

    # Test de l'IA 1
    print("\n\n##########################")
    print("TEST pour IA_1:")
    grille = Grille()
    grille.ajoute(0, 0, 2)
    grille.ajoute(1, 0, 2)
    grille.ajoute(2, 0, 1)
    grille.ajoute(1, 1, 1)
    print(grille)
    x, y = IA_1(grille)
    print("Coordonnées de la case : ", (x, y))
    print("Valeur de la case : ", grille.case(x, y))

    # Test de l'IA 2
    print("\n\n##########################")
    print("TEST pour IA_2:")
    grille = Grille()
    grille.ajoute(0, 0, 1)
    grille.ajoute(1, 0, 1)
    grille.ajoute(1, 2, 2)
    grille.ajoute(0, 2, 2)
    joueur = 1
    print(grille)
    x, y = IA_2(grille, joueur)
    print("Coordonnées de la case pour le joueur : ", joueur, [x, y])

    # Combat d'IA
    IA_1_vs_IA_1(100)
    IA_1_vs_IA_2(100)
#    IA_2_vs_IA_3(10)
