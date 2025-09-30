# ==============================================================
#  Auteur        : Amin Torrisi, Ruben Ten Cate, Camille Bachmann et Marc Schilter
#  Date création : 16.09.2025
#  Dernière modif : 30.09.2025
#  Présentation : Script de création d'une fiche de personnage D&D basique
#                 en utilisant la programmation orientée objet (OOP).
#                 Possibilité de faire un export de cette dernière pour la sauvgarder.
#  Encodage : UTF-8
#  Version       : 1.0
# ==============================================================

#----------------Importations ----------------
from dataclasses import dataclass
import json
import random

# ------------------------- Catalogues  ------------------------- #
RACES = ["Humain", "Elfe", "Nain", "Halfelin"]
CLASSES = ["Guerrier", "Voleur", "Clerc", "Magicien"]
BACKGROUNDS = ["Soldat", "Acolyte", "Criminel", "Savant"]
SKILLS = ["Athlétisme (FOR)", "Acrobaties (DEX)", "Arcanes (INT)", "Discrétion (DEX)", "Dressage (SAG)", "Escamotage (DEX)", "Histoire (INT)", "Intimidation (CHA)", "Intuition (SAG)", "Investigation (INT)", "Médecine (SAG)", "Nature (INT)", "Perception (SAG)", "Persuasion (CHA)", "Religion (INT)", "Representation (CHA)", "Survie (SAG)", "Tromperie (CHA)"]
# Armes par classe
WEAPON_GUERRIER = ["Marteau de guerre (2 mains)", "Epée longue (1 main)", "Fléau d'arme (1 main)"]
WEAPON_MAGICIEN = ["Bâton de combat (2 mains)", "Dague (1 main)", "Gourdin (1 main)"]
WEAPON_VOLEUR = ["Arc long (2 mains)", "Dague (1 main)", "Rapière (1 main)"]
WEAPON_CLERC = ["Lance (2 mains)", "Masse d'arme (1 main)", "Hache (1 main)"]
# Options de bouclier
SHIELD = ["Equipé", "Non équipé"]

#----------------Listes [statistiques]----------------
CARACTERISTIQUES = ["\033[91mForce\033[0m", "\033[34mDextérité\033[0m", "\033[92mConstitution\033[0m", "\033[96mIntelligence\033[0m", "\033[95mSagesse\033[0m", "\033[94mCharisme\033[0m"]
#Liste scores des caracteristiques option méthode fixe
SCORES_FIXES = [15, 14, 13, 12, 10, 8]
METHODES_STAT = ["Méthode fixe", "Méthode aléatoire"]


# ------------------------- Modèle ------------------------- #
@dataclass
#Classe de données pour un personnage D&D.
class Character:
    name: str
    race: str
    classe: str
    force: int
    modif_force: int
    dexterite: int
    modif_dexterite: int
    constitution: int
    modif_constitution: int
    intelligence: int
    modif_intelligence: int
    sagesse: int
    modif_sagesse: int
    charisme: int
    modif_charisme: int
    background: str
    skills: list[str]
    weapon: str
    shield: str

    # Fonction pour afficher un résumé du personnage.
    def summary(self) -> str:
        return (
            "\n--- Résumé du personnage ---\n"
            f"Nom       : {self.name}\n"
            f"Race      : {self.race}\n"
            f"Classe    : {self.classe}\n"
            f"Force        : {self.force}\n"
            f"Modificateur de Force : {self.modif_force}\n"
            f"Dextérité    : {self.dexterite}\n"
            f"Modificateur de Dextérité : {self.modif_dexterite}\n"
            f"Constitution : {self.constitution}\n"
            f"Modificateur de Constitution : {self.modif_constitution}\n"
            f"Intelligence : {self.intelligence}\n"
            f"Modificateur d'Intelligence : {self.modif_intelligence}\n"
            f"Sagesse      : {self.sagesse}\n"
            f"Modificateur de Sagesse : {self.modif_sagesse}\n"
            f"Charisme     : {self.charisme}\n"
            f"Modificateur de Charisme : {self.modif_charisme}\n"
            f"Historique: {self.background}\n"
            f"Compétences : {self.skills}\n"
            f"Arme      : {self.weapon}\n"
            f"Bouclier  : {self.shield}\n"
        )

    # Fonction pour exporter la fiche de personnage en JSON.
    def to_json(self):
        data = {
            'name': self.name,
            'race': self.race,
            'classe': self.classe,
            'force': self.force,
            'modif_force': self.modif_force,
            'dexterite': self.dexterite,
            'modif_dexterite': self.modif_dexterite,
            'constitution': self.constitution,
            'modif_constitution': self.modif_constitution,
            'intelligence': self.intelligence,
            'modif_intelligence': self.modif_intelligence,
            'sagesse': self.sagesse,
            'modif_sagesse': self.modif_sagesse,
            'charisme': self.charisme,
            'modif_charisme': self.modif_charisme,
            'background': self.background,
            'skills': self.skills,
            'weapon': self.weapon,
            'shield': self.shield
        }
        #nom du fichier basé sur le nom du personnage
        filename = self.name + ".json"
        with open(filename, 'w', encoding="utf-8") as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))
        print(f"\n→ Fiche de personnage exportée vers {filename}")


# ------------------------- UI Console ------------------------- #
class CharacterCreator:
# Gestion du flux de création en console (I/O).
# Séparé du modèle pour faciliter les tests et d'autres interfaces.

    def __init__(self, races, classes, backgrounds, weapon, shield, stat_fix, methodes_stat, skills):
        self.races = list(races)
        self.classes = list(classes)
        self.backgrounds = list(backgrounds)
        self.skills = list(skills)
        self.weapon = list(weapon)
        self.shield = list(shield)
        self.stat_fix = list(stat_fix)
        self.methodes_stat = list(methodes_stat)

    @staticmethod
    def ask_choice(label, options):
        print(label)
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")
        while True:
            s = input("Votre choix (numéro) : ").strip()
            # Gestions des erreurs
            if s.isdigit():
                idx = int(s)
                if 1 <= idx <= len(options):
                    return options[idx - 1]
            print("→ Entrée invalide, réessayez.")

    @staticmethod
    # Demande le nom du personnage, avec valeur par défaut si entrée vide.
    def ask_name(prompt="Nom du personnage : ", default="Super-Clochard"):
        name = input(prompt).strip()
        return name if name else default

    # Fonction principal de création.
    def run(self) -> Character:
        print("\n=== Créateur de personnage D&D 5e — Choix de base (OOP) ===\n")

        name = self.ask_name()
        race = self.ask_choice("\nChoisissez une race :", self.races)
        classe = self.ask_choice("\nChoisissez une classe :", self.classes)

        # Choix de la méthode de définition des statistiques
        methodes = self.ask_choice("\nChoisissez une méthode :", METHODES_STAT)
        match methodes:

            case "Méthode fixe":
                print("Vous avez choisi la méthode fixe, veuillez a présent attribuer les scores définis aux 6 caractéristiques")
                # utiliser la méthode fixe
                force = self.ask_choice("\nChoisissez un score pour la Force :", SCORES_FIXES)
                SCORES_FIXES.remove(force)  # Retirer le score choisi pour ne pas le réutiliser
                dexterite = self.ask_choice("\nChoisissez un score pour la Dextérité :", SCORES_FIXES)
                SCORES_FIXES.remove(dexterite)
                constitution = self.ask_choice("\nChoisissez un score pour la Constitution :", SCORES_FIXES)
                SCORES_FIXES.remove(constitution)
                intelligence = self.ask_choice("\nChoisissez un score pour l'Intelligence :", SCORES_FIXES)
                SCORES_FIXES.remove(intelligence)
                sagesse = self.ask_choice("\nChoisissez un score pour la Sagesse :", SCORES_FIXES)
                SCORES_FIXES.remove(sagesse)
                charisme = self.ask_choice("\nChoisissez un score pour le Charisme :", SCORES_FIXES)
                SCORES_FIXES.remove(charisme)

            case "Méthode aléatoire": #a finir
                print(
                    "Vous avez choisi la méthode aléatoire:\n"
                    "Les scores vont être générés automatiquement par trois jets de dés 🎲 a 6 faces pour chaque caractéristique")
                
                # utiliser la méthode aléatoire
                def roll_dice():
                    rolls = [random.randint(1, 6) for _ in range(3)]
                    return sum(rolls)
                force = roll_dice()
                dexterite = roll_dice()
                constitution = roll_dice()
                intelligence = roll_dice()
                sagesse = roll_dice()
                charisme = roll_dice()

        # calcul modificateur
        modif_force = int((force - 10) // 2)
        modif_dexterite = int((dexterite - 10) // 2)
        modif_constitution = int((constitution - 10) // 2)
        modif_intelligence = int((intelligence - 10) // 2)
        modif_sagesse = int((sagesse - 10) // 2)
        modif_charisme = int((charisme - 10) // 2)

        background = self.ask_choice("\nChoisissez un historique :", self.backgrounds)
        # Choix de l'arme en fonction de la classe
        match classe:
            case "Guerrier":
                weapon = self.ask_choice("\nChoisissez une arme :", WEAPON_GUERRIER)
                nbr_comp = 2  # Nombre de compétences à choisir pour le guerrier
            case "Magicien":
                weapon = self.ask_choice("\nChoisissez une arme :", WEAPON_MAGICIEN)
                nbr_comp = 2  # Nombre de compétences à choisir pour le magicien
            case "Voleur":
                weapon = self.ask_choice("\nChoisissez une arme :", WEAPON_VOLEUR)
                nbr_comp = 4  # Nombre de compétences à choisir pour le voleur
            case "Clerc":
                weapon = self.ask_choice("\nChoisissez une arme :", WEAPON_CLERC)
                nbr_comp = 2  # Nombre de compétences à choisir pour le clerc
                
        # Choix du bouclier en fonction de l'arme
        match weapon:
            case "Marteau de guerre (2 mains)" | "Arc long (2 mains)" | "Bâton de combat (2 mains)" | "Lance (2 mains)":
                shield = "Non équipé"
            case _:
                shield = self.ask_choice("\nChoisissez si vous voulez équiper un bouclier :", self.shield)

        # Choix des compétences
        competences = []  # Liste pour stocker les compétences choisies
        for c in range(nbr_comp):  # Choix de 2 compétences
            skill = (self.ask_choice(f"\nChoisissez la compétence {c + 1} :", self.skills))
            competences.append(skill)  # Ajout de la compétence choisie à la liste
            self.skills.remove(skill)  # Empêche de choisir la même compétence

        return Character(
            name=name, 
            race=race, 
            classe=classe, 
            background=background, 
            weapon=weapon, 
            shield=shield, 
            force=force, 
            dexterite=dexterite,  
            constitution=constitution,  
            intelligence=intelligence, 
            sagesse=sagesse,  
            charisme=charisme, 
            modif_force=modif_force, 
            modif_dexterite=modif_dexterite,
            modif_constitution=modif_constitution,
            modif_intelligence=modif_intelligence, 
            modif_sagesse=modif_sagesse, 
            modif_charisme=modif_charisme,
            skills=competences)


# ------------------------- Programme principal ------------------------- #
def main():
    creator = CharacterCreator(RACES, CLASSES, BACKGROUNDS, WEAPON_GUERRIER + WEAPON_MAGICIEN + WEAPON_VOLEUR + WEAPON_CLERC, SHIELD, SCORES_FIXES, METHODES_STAT, SKILLS)
    character = creator.run()
    print(character.summary())
    character.to_json()


if __name__ == "__main__":
    main()

