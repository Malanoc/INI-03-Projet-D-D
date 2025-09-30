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

from dataclasses import dataclass
import json

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


# ------------------------- Modèle ------------------------- #
@dataclass
#Classe de données pour un personnage D&D.
class Character:
    name: str
    race: str
    classe: str
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

    def __init__(self, races, classes, backgrounds, skills, weapon, shield):
        self.races = list(races)
        self.classes = list(classes)
        self.backgrounds = list(backgrounds)
        self.skills = list(skills)
        self.weapon = list(weapon)
        self.shield = list(shield)

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
        # Choix des compétences
        competences = []  # Liste pour stocker les compétences choisies
        for c in range(nbr_comp):  # Choix de 2 compétences
            skill = (self.ask_choice(f"\nChoisissez la compétence {c + 1} :", self.skills))
            competences.append(skill)  # Ajout de la compétence choisie à la liste
            self.skills.remove(skill)  # Empêche de choisir la même compétence
        # Choix du bouclier en fonction de l'arme
        match weapon:
            case "Marteau de guerre (2 mains)" | "Arc long (2 mains)" | "Bâton de combat (2 mains)" | "Lance (2 mains)":
                shield = "Non équipé"
            case _:
                shield = self.ask_choice("\nChoisissez si vous voulez équiper un bouclier :", self.shield)

        return Character(name=name, race=race, classe=classe, background=background, skills=competences, weapon=weapon, shield=shield)


# ------------------------- Programme principal ------------------------- #
def main():
    creator = CharacterCreator(RACES, CLASSES, BACKGROUNDS, SKILLS, WEAPON_GUERRIER + WEAPON_MAGICIEN + WEAPON_VOLEUR + WEAPON_CLERC, SHIELD)
    character = creator.run()
    print(character.summary())
    character.to_json()

if __name__ == "__main__":
    main()
