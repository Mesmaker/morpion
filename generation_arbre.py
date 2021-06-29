from classe_morpion import *

########################################
# Fonctions servant à faire et étudier
# l'arbre des parties

def lister_parties_filles(partie):
    """A partir d'une partie, on en déduit toutes les parties
    ayant un tour de plus. On enlève les parties équivalentes
    à d'autres parties pour ne pas avoir de parties redondantes."""

    # Test si présence d'une feuille, si 9 tours ont été joué
    # ou bien si un des deux joueurs a gagné.
    if len(partie.tours) == 9:
        return [0, []]
    if partie.grille.vainqueur() != 0:
        return [0, []]

    # Dans le cas où il y a d'autre tour possible,
    # on recherche des cases libres où jouer, on y joue dedans
    # puis avant de stocker cette nouvelle partie on teste si elle
    # n'est pas équivalente à une autre et puis on passe à la case
    # libre suivante.
    parties_filles = []
    nbr_filles = 0
    
    for i in range(3):
        for j in range(3):
            if partie.grille.case(i, j) == 0:
                partie_fille = Partie.copier(partie)
                tour = Tour(i, j)
                partie_fille.nouveau_tour(tour)
                # Inclue la nouvelle partie dans la liste.
                # Incrémente la compteur du nombre de parties filles
                parties_filles.append(partie_fille)
                nbr_filles += 1
    # Retourne le nombre de parties filles et ces parties
    return [nbr_filles, parties_filles]

def generer_arbre(partie):
    """A partir d'une partie, on génère l'arbre des parties possibles"""
    # On commence par générer, les parties possibles au tour suivant
    nbr_filles, parties_filles = lister_parties_filles(partie)

    # Soit il n'y a pas de tours suivants et alors il s'agit d'une
    # feuille d'un arbre
    if nbr_filles == 0:
        return Arbre(partie)
    # Soit il y a des tours suivants et par récurrence on génère
    # l'arbre pour chaque partie ayant un suivant. On regroupe enfin
    # tous ces arbres sous la première partie.
    else:
        arbre = Arbre(partie)
        arbres_fils = []
        for partie_fille in parties_filles:
            arbre_fils = generer_arbre(partie_fille)
            arbres_fils.append(arbre_fils)
        arbre.enraciner(arbres_fils)
        return arbre

def generer_arbre_vainqueur_1(partie):

    # Si un joueur a gagné ou si toutes la grille est remplie,
    # alors la partie est finie.
    if partie.grille.vainqueur() != 0 or len(partie.tours) == 9:
        return Arbre(partie)

    # Dans le cas où le nombre de tours est impair,
    # ce n'est pas au joueur 1 de jouer donc toutes les
    # possibilités doivent être envisagées
    if len(partie.tours)%2 == 1:
        arbre = Arbre(partie)
        nbr_filles, parties_filles = lister_parties_filles(partie)
        nbr_parties = 0
        arbres_fils = []
        for partie_fille in parties_filles:
            arbre_fils = generer_arbre_vainqueur_1(partie_fille)
            arbres_fils.append(arbre_fils)
        arbre.enraciner(arbres_fils)
        return arbre
    
    # Dans les autres cas, on regarde les parties filles et
    # on cherche celle qui a le plus de chance de donner la
    # victoire au joueur 1. Pour cela, on calcul le nombre
    # de partie gagnée par 1 sur celle gagné par 2.
    nbr_filles, parties_filles = lister_parties_filles(partie)
    indicatrice = -1
    for partie_fille in parties_filles:
        arbre_fils = generer_arbre_vainqueur_1(partie_fille)
        liste_0    = arbre_fils.lister_feuilles(0, -1)
        liste_1    = arbre_fils.lister_feuilles(1, -1)
        liste_2    = arbre_fils.lister_feuilles(2, -1)
        #print("2, 1, 0 :", len(liste_2), len(liste_1), len(liste_0))
        indicatrice_tmp = arbre_fils.nbr_feuilles
        #print("Nbr_arbre : ", indicatrice_tmp)
        if len(liste_2) == 0 and (indicatrice_tmp < indicatrice or
                                  indicatrice < 0):
            indicatrice = indicatrice_tmp
            meilleur_arbre = arbre_fils
            #return [arbre_fille[0], partie, 1, [arbre_fille]]
        #else:
         #   pass
            #indicatrice_tmp = len(liste_1)/(len(liste_2)**2+len(liste_0))
            #if indicatrice_tmp > indicatrice:
            #    indicatrice = indicatrice_tmp
            #    meilleur_arbre = arbre_fille
            #    nbr_parties = arbre_fille[0]
    if indicatrice == -1:
        #print("Pas trouvé de victoire assurée")
        arbre_fils = generer_arbre_vainqueur_1(parties_filles[0])
        meilleur_arbre = arbre_fils

    arbre = Arbre(partie)
    arbre.enraciner([meilleur_arbre])
    return arbre

def generer_arbre_vainqueur_2(partie):

    # Si un joueur a gagné ou si toutes la grille est remplie,
    # alors la partie est finie.
    if partie.grille.vainqueur() != 0 or len(partie.tours) == 9:
        return Arbre(partie)

    # Dans le cas où le nombre de tours est impair,
    # ce n'est pas au joueur 2 de jouer donc toutes les
    # possibilités doivent être envisagées
    if len(partie.tours)%2 == 0:
        arbre = Arbre(partie)
        nbr_filles, parties_filles = lister_parties_filles(partie)
        nbr_parties = 0
        arbres_fils = []
        for partie_fille in parties_filles:
            arbre_fils = generer_arbre_vainqueur_2(partie_fille)
            arbres_fils.append(arbre_fils)
        arbre.enraciner(arbres_fils)
        return arbre
    
    # Dans les autres cas, on regarde les parties filles et
    # on cherche celle qui a le plus de chance de donner la
    # victoire au joueur 2.
    nbr_filles, parties_filles = lister_parties_filles(partie)
    indicatrice = -1
    for partie_fille in parties_filles:
        arbre_fils = generer_arbre_vainqueur_2(partie_fille)
        liste_0    = arbre_fils.lister_feuilles(0, -1)
        liste_1    = arbre_fils.lister_feuilles(1, -1)
        liste_2    = arbre_fils.lister_feuilles(2, -1)
        #print("2, 1, 0 :", len(liste_2), len(liste_1), len(liste_0))
        indicatrice_tmp = arbre_fils.nbr_feuilles
        #print("Nbr_arbre : ", indicatrice_tmp)
        if len(liste_1) == 0 and (indicatrice_tmp < indicatrice or
                                  indicatrice < 0):
            indicatrice = indicatrice_tmp
            meilleur_arbre = arbre_fils
            #return [arbre_fille[0], partie, 1, [arbre_fille]]
        #else:
         #   pass
            #indicatrice_tmp = len(liste_1)/(len(liste_2)**2+len(liste_0))
            #if indicatrice_tmp > indicatrice:
            #    indicatrice = indicatrice_tmp
            #    meilleur_arbre = arbre_fille
            #    nbr_parties = arbre_fille[0]
    if indicatrice == -1:
        #print("Pas trouvé de victoire assurée")
        arbre_fils = generer_arbre_vainqueur_2(parties_filles[0])
        meilleur_arbre = arbre_fils

    arbre = Arbre(partie)
    arbre.enraciner([meilleur_arbre])
    return arbre


########################################
# Test

if __name__ == "__main__":

    partie = Partie()

    tour_tmp = Tour(0, 2)
    partie.nouveau_tour(tour_tmp)

    tour_tmp = Tour(0, 0)
    partie.nouveau_tour(tour_tmp)

    tour_tmp = Tour(2, 0)
    partie.nouveau_tour(tour_tmp)

    tour_tmp = Tour(1, 1)
    partie.nouveau_tour(tour_tmp)

    #tour_tmp = Tour(1, 1)
    #partie.nouveau_tour(tour_tmp)

    #tour_tmp = Tour(2, 1)
    #partie.nouveau_tour(tour_tmp)
    #tour_tmp = Tour(3, 1)
    #partie.nouveau_tour(tour_tmp)

    print(partie.grille)

    nbr_filles, liste_filles = lister_parties_filles(partie)
    print("Lister parties filles : ")
    print(nbr_filles, liste_filles)

    print("ARBRE VAINQUEUR 1")
    arbre = generer_arbre_vainqueur_1(partie)
    print("ARBRE VAINQUEUR 2")
    arbre = generer_arbre_vainqueur_2(partie)
    print("Arbre des possibles")
    arbre = generer_arbre(partie)

    liste = arbre.lister_feuilles(0, -1)
    print("Match nul : ", len(liste))
    #for partie_tmp in liste:
    #    print(partie_tmp)
    #    partie_tmp.afficher_grille()

    liste = arbre.lister_feuilles(1, -1)
    print("Vainqueur 1 :", len(liste))
    #for partie_tmp in liste:
    #    print(partie_tmp)
    #    partie_tmp.afficher_grille()

    liste = arbre.lister_feuilles(2, -1)
    print("Vainqueur 2: ", len(liste))
    #for partie_tmp in liste:
    #    partie_tmp.afficher_grille()


    partie = Partie()
    print(partie.grille)
    arbre = generer_arbre_vainqueur_2(partie)
