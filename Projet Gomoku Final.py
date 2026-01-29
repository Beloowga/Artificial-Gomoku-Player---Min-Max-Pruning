import time
from itertools import groupby

dico_listes_remarquables = {
    '11111': 2000000,
    '22222': -2000000,
    '111100': 1000000,
    '222200': -1000000,
    '022020': -200000,
    '101110': 1000000,
    '202220': -1000000,
    '011110': 1000000,
    '122220': -500000,
    '01110': 300000,
    '00110': 10000,
    '022220': -1000000,
    '02220': -300000,
    '011010': 200000,
    '210110': 100000,
    '01100': 10000,
    '010110': 200000,
    '002222': -1000000,
    '001111': 1000000,
    '0110': 1000,
    '0220': -1000,
    '1211': 100,
    '2122': -100,
    '020220': -200000,
    '001112': 100000,
    '211100': 100000,
    '011112': 500000,
    '211110': 500000,
    '022221': -500000,
    '02200': -10000,
    '00220': -10000,
    '002221': -100000,
    '122200': -100000,
    '211010': 100000,
}

def afficher_plateau(plateau):
    print("\n   " + " ".join(f"{i:2}" for i in range(15)))
    for indice, ligne in enumerate(plateau):
        print(f"{indice:2} " + " ".join(" X" if cell == 1 else " O" if cell == 2 else " ." for cell in ligne))
    print()

def actions(etat): # on retourne les coups possibles
    plateau=etat["plateau"]
    directions=[(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1, 1)]#les différentes directions où aller
    if etat["tour"]==1:
        return [(7,7)] #on est obligé de jouer au milieu
    elif etat["tour"]==2:#ici peut importe où on joue
        return [(i,j) for i in range(15) for j in range(15) if plateau[i][j] == 0 and (i, j) != (7, 7)]
    elif etat["tour"]==3:#ici il faut respecter la règle du carré centrale donc on introduit une liste de coup interdit pour ce tour
        cellules_vides=[(i,j) for i in range(15) for j in range(15) if plateau[i][j]==0] 
        cellules_interdites= [(i,j) for i in range(4,11) for j in range(4,11)]
        return [cellule for cellule in cellules_vides if cellule not in cellules_interdites]
    else:
        cellules_vides=set()
        for i in range(15):
            for j in range(15):
                if plateau[i][j]!=0: #on regarde seulement les cases qui ne sont pas vides, sinon ça n'aurait pas de sens de jouer des cases éloignées de celles non vides
                    for di,dj in directions:
                        for k in range(1,6):#on prends les cases dans un carré de coté 5
                            ni,nj = i+di*k,j+dj*k
                            if 0<=ni<15 and 0<=nj< 15 and plateau[ni][nj]==0:
                                cellules_vides.add((ni,nj))
        return list(cellules_vides)

def result(etat,action): #on update l'état du plateau selon une action
    nouveau_plateau=[ligne[:] for ligne in etat["plateau"]]
    i,j=action
    joueur=etat["joueur"]
    nouveau_plateau[i][j]=joueur #on regarde qui est le joueur actuel
    prochain_joueur=2 if joueur==1 else 1 # on regarde qui est le prochain joueur
    return {"plateau":nouveau_plateau,"tour":etat["tour"]+1,"joueur":prochain_joueur} #ici on update l'état du plateau avec le nouveau joueur

def Terminal_Test(etat):#est ce que la partie est terminée ?
    plateau = etat["plateau"]
    def ligne(cases):
        return any(all(case!=0 and case==cases[i] for case in cases[i:i+5]) for i in range(len(cases)-4))#Ici on vérifie si une ligne contient 5 cellules consécutives d'un même joueur et non nulles

    for i in range(15): # Vérification des lignes et colonnes
        if ligne(plateau[i]):#ici les lignes
            return True
        if ligne([plateau[j][i] for j in range(15)]): # et là les colonnes
            return True

    for i in range(11):# Pareil ici mais pour les diagonales
        for j in range(11):
            if all(plateau[i+k][j+k]!=0 and plateau[i+k][j+k]== plateau[i][j] for k in range(5)):#Diagonale vers bas droite
                return True
            if all(plateau[i+k][j-k]!=0 and plateau[i+k][j-k]==plateau[i][j] for k in range(5)):# Diagonale vers bas gauche
                return True
    return all(cell != 0 for row in plateau for cell in row) #Si on a rien return jusqu'à cette ligne alors c'est que le tableau est plein 



def score_motif(liste,joueur,adversaire):
    #ici on teste des motifs de cases selon qui est le joueur et qui est l'adversaire
    score=0
    joueur_nb=liste.count(joueur)
    adversaire_nb=liste.count(adversaire)

    if joueur_nb>0 and adversaire_nb==0:
        score+=10**joueur_nb
    elif adversaire_nb>0 and joueur_nb==0:
        score-=10**adversaire_nb
    return score

def utility(etat):
    plateau=etat["plateau"]
    joueur=etat["joueur"]
    adversaire=2 if joueur==1 else 1
    score=0
    for i in range(15):
        for j in range(11):
            score+=score_motif([plateau[i][j+k] for k in range(5)],joueur,adversaire)
        for j in range(11):
            score+= score_motif([plateau[j+k][i] for k in range(5)],joueur,adversaire) 
    for i in range(11):
        for j in range(11):
            score+= score_motif([plateau[i+k][j+k] for k in range(5)],joueur,adversaire)
            score +=score_motif([plateau[i+k][j-k] for k in range(5)],joueur,adversaire)  
    return score

def action_gagnante(etat): #on rajoute cette fonction pour voir si il y a une opportunité de victoire immédiate (si ya 4 cases d'affilées)
    plateau=etat["plateau"]
    joueur=etat["joueur"]
    adversaire=2 if joueur==1 else 1
    for i in range(15):
        for j in range(11):
            ligne=[plateau[i][j+k] for k in range(5)]
            if ligne.count(joueur)==4 and ligne.count(0)==1:
                return i,j+ligne.index(0) 

    for i in range(11):
        for j in range(15):
            colonne=[plateau[i+k][j] for k in range(5)]
            if colonne.count(joueur)==4 and colonne.count(0)==1:
                return i+colonne.index(0),j
    for i in range(11):
        for j in range(11):
            diagonale1=[plateau[i+k][j+k] for k in range(5)]
            if diagonale1.count(joueur)==4 and diagonale1.count(0)==1:
                return i+diagonale1.index(0),j+diagonale1.index(0)

            diagonale2=[plateau[i+k][j-k] for k in range(5)]
            if diagonale2.count(joueur)==4 and diagonale2.count(0)==1:
                return i+diagonale2.index(0),j-diagonale2.index(0)
    return None

def minimax_alpha_beta(etat, profondeur, alpha, beta, maximisant):
    if Terminal_Test(etat) or profondeur==0: #on vérifie d'abord si la partie est terminée ou si la profondeur max est atteinte
        return utility(etat),None #si la partie n'est pas terminée on récupère le score de l'état du plateau
    if maximisant: #ici c'est pour le joueur maximinsant
        # Ici pour le joueur maximisant (celui qui essaie d'obtenir le score maximum)
        meilleur_score=float('-inf')  # Initialisation au pire score possible
        meilleure_action=None  # Pas d'action définie pour l'instant
        # on vérifie si une action gagnante immédiate existe
        action=action_gagnante(etat)
        if action:
            return float('inf'),action# Retourne un score infini si l'action garantit une victoire
        for action in actions(etat):
            # il faut parcourir toutes les actions possibles depuis l'état actuel
            nouvel_etat=result(etat,action)  # On applique une action pour obtenir un nouvel état
            score, _=minimax_alpha_beta(nouvel_etat,profondeur-1,alpha,beta,False)
            # Appel récursif pour évaluer le score de cet état en supposant que l'adversaire joue ensuite
            if score>meilleur_score:
                # Met à jour le meilleur score et la meilleure action si le score est supérieur au précédent
                meilleur_score=score
                meilleure_action=action
            alpha=max(alpha, meilleur_score)#On met à jour la borne alpha
            if beta<=alpha:#on arrete de considérer la position si elle n'améliore pas le score
                break
        return meilleur_score,meilleure_action

    else:
        # On fait la même chose ici mais pour le score minimisant
        pire_score =float('inf')
        pire_action= None
        for action in actions(etat):
            nouvel_etat =result(etat, action)  
            score, _ =minimax_alpha_beta(nouvel_etat, profondeur - 1, alpha, beta, True)
            if score <pire_score:
                pire_score=score
                pire_action=action
            beta=min(beta, pire_score)
            if beta<=alpha:
                break
        return pire_score,pire_action

def demander_coup_utilisateur(etat):
    while True:
        try:
            coup = input("Entrez votre coup sous la forme : ligne colonne ").strip()
            i, j = map(int, coup.split())  # Convertit l'entrée en deux entiers (ligne et colonne).
            coup = (i, j)

            if coup in actions(etat):
                return coup
            else:
                print("Le coup est pas possible veuillez réessayer.")

        except (ValueError, IndexError):
            print("Entrée invalide veuillez essayez à nouveau sous la forme : ligne colonne.")

def jouer():
    plateau=[[0 for _ in range(15)] for _ in range(15)]
    etat={"plateau": plateau,"tour": 1, "joueur": 1}  # On initialise le plateau et l'état

    print("Qui commence la partie ?")
    print("1.Vous")
    print("2.L'IA")
    choix=input("Entrez 1 ou 2 : ").strip()
    joueur_humain=1 if choix=="1" else 2 
    afficher_plateau(etat["plateau"])  #On affiche le plateau
    ia_a_joue_par_defaut=False
    while not Terminal_Test(etat):
        if etat["joueur"] == joueur_humain:
            action = demander_coup_utilisateur(etat)
        else:
            print("L'IA réfléchit..")
            if etat["tour"]==2 and joueur_humain==1 and not ia_a_joue_par_defaut:
                action = (7, 3)
                ia_a_joue_par_defaut=True
            else:
                profondeur=2  # Profondeur d'analyse de l'algorithme.
                _, action=minimax_alpha_beta(etat, profondeur,float('-inf'),float('inf'), True)
            print(f"L'IA joue : {action[0]} {action[1]}")
        etat =result(etat,action)#On met à jour le plateau après avoir jouer un coup
        afficher_plateau(etat["plateau"])

        if Terminal_Test(etat):
            # Si le jeu est terminé
            gagnant = 3 -etat["joueur"] 

            if gagnant==joueur_humain:
                print("Félicitations, vous avez gagné !")
            else:
                print("L'IA a gagné !")

            break


if __name__== "__main__":
    jouer()
