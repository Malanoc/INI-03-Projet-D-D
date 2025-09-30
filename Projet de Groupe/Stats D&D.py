#----------------Importations pour [statistiques]----------------
from tabulate import tabulate  #dans terminal : pip install tabulate
import random

#----------------Listes [statistiques]----------------

# Liste des caractéristiques avec des code couleurs ANSI
caracteristiques = ["\033[91mForce\033[0m", "\033[34mDextérité\033[0m", "\033[92mConstitution\033[0m", "\033[96mIntelligence\033[0m", "\033[95mSagesse\033[0m", "\033[94mCharisme\033[0m"]

#Liste scores des caracteristiques option méthode fixe
scores_fixes = [15, 14, 13, 12, 10, 8]

#----------------Fonctions[statistiques]----------------

#1 - Fonction du panel statistiques joueur (Choix de input avec la variable match)
def attribution_statistiques():
    choix_methode=int(input("Choisissez entre l'option [1] ou [2] :\n"))
    match choix_methode:
        case 1:
            print("Vous avez choisi la méthode fixe, veuillez a présent attribuer les scores définis aux 6 caractéristiques")
            methode_fixe()
        case 2:
            print(
                "Vous avez choisi la méthode aléatoire:\n"
                "Les scores vont être générés automatiquement par trois jets de dés 🎲 a 6 faces pour chaque caractéristique")
            methode_aleatoire()
        case _:
            print("⚠️ Veuillez choisir un chiffre entre 1 et 2")
            attribution_statistiques()

#2 - Définition de la fonction statistiques joueur (surtout du texte)
def statistiques_joueur():
    print("\n--------Statistiques du joueur--------")
    print("\nA présent vous allez définir un score pour chacunes \ndes 6 caractéristiques de votre personnage:")
    print("1. \033[91mForce\033[0m")
    print("2. \033[34mDextérité\033[0m")
    print("3. \033[92mConstitution\033[0m")
    print("4. \033[96mIntelligence\033[0m")
    print("5. \033[95mSagesse\033[0m")
    print("6. \033[94mCharisme\033[0m")

    print("\nVeuillez choisir entre deux méthodes pour attribuer les scores :")
    print("1. Méthode fixe")
    print("2. Méthode aléatoire")

#3 - définition modificateur
def calcul_modificateur(score):
    return (score - 10) // 2

#4 - définition de la méthode fixe
def methode_fixe():
    scores_fixes_choisis = {} #Ce dictionnaire sert a stocker les scores attribués à chaque caractéristique
    scores_disponibles = scores_fixes.copy() #.copy() sert a faire un copie indépendante de la liste scores_fixes pour pouvoir la modifier : retirer les scores disponibles de la liste originale puis faire une copie des éléments restants dans la liste

    for carac in caracteristiques: #boucle sur chaque caractéristique
        print(f"\nScores disponibles : {scores_disponibles}")
        while True:
            try: #L e try permet de gérer les erreurs si l’utilisateur entre autre chose qu’un nombre
                choix = int(input(f"Quel score voulez-vous attribuer à {carac} ? "))
                if choix in scores_disponibles: #vérifie que le score choisi est bien dans la liste des scores disponibles
                    scores_fixes_choisis[carac] = choix
                    scores_disponibles.remove(choix)
                    break # sort de la boucle while True pour passer a la prochaine caractéristique
                else:
                    print("Score invalide ou déjà utilisé. Essayez encore.")
            except ValueError: # Si l'utilisateur entre un texte ou un caractère non convertible en nombre entier, un message d'erreur est affiché.
                print("Veuillez entrer un nombre valide.")


    # Préparation des données pour un tableau visuel de caractéristiques
    # Colonne 1 : Pour chaque caractéristique dans la liste caracteristiques, prend le nom de la caractéristique (carac)
    # Colonne 2 : Le score attribué a la caractersitique
    # Colonne 3 : Affiche le modificateur calculé a partir du score avec un signe (+/-)

    tableau = [
        [carac, scores_fixes_choisis[carac], f"{calcul_modificateur(scores_fixes_choisis[carac]):+d}"]
        for carac in caracteristiques
    ]

    # Affichage du tableau
    print("\n📊 Tableau des caractéristiques :")
    print(tabulate(
        tableau,
        headers=[f"\033[1mCaractéristique\033[0m", f"\033[1mScore\033[0m", f"\033[1mModificateur\033[0m"],
        tablefmt="grid",
        colalign=("left", "center", "center") #Alignement du score et modifacateur dans les colonnes
    ))

#5 - définition de la méthode aléatoire

def methode_aleatoire():
    scores_aleatoires = {}  # Dictionnaire pour stocker les scores aléatoires

    # Boucle sur chaque caractéristique
    for carac in caracteristiques: # Pour chaque élément dans la liste caractéristique
        score = random.randint(3, 18)  # Génère un score aléatoire entre 1 et 20
        scores_aleatoires[carac] = score # Enregistre le score dans le dictionnaire scores_aleatoires
        print(f"{carac} → 🎲 {score}") # Affiche le résultat du score aléatoire

    # Préparation du tableau avec modificateurs
    tableau = [
        [carac, scores_aleatoires[carac], f"{calcul_modificateur(scores_aleatoires[carac]):+d}"]
        for carac in caracteristiques
    ]

    print("\n📊 Tableau des caractéristiques (Méthode aléatoire) :")
    print(tabulate(
        tableau,
        headers=[f"\033[1mCaractéristique\033[0m", f"\033[1mScore\033[0m", f"\033[1mModificateur\033[0m"],
        tablefmt="grid",
        colalign=("left", "center", "center")  # Alignement par colonne
    ))

#----afficher la séquence choix de statistiques du joueur----
statistiques_joueur()
attribution_statistiques()










