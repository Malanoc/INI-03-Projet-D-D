# ==============================================================
#  Auteur        : Amin Torrisi, Ruben Ten Cate, Camille Bachmann et Marc Schilter
#  Date création : 16.09.2025
#  Dernière modif : 16.09.2025
#  Présentation : Script de création d'une fiche de personnage D&D basique
#                 en utilisant la programmation orientée objet (OOP).
#                 Possibilité de faire un export de cette dernière pour la sauvgarder.
#  Encodage : UTF-8
#  Version       : 1.0
# ==============================================================

from dataclasses import dataclass

# ------------------------- Catalogues  ------------------------- #
RACES = ["Humain", "Elfe", "Nain", "Halfelin"]
CLASSES = ["Guerrier", "Voleur", "Clerc", "Magicien"]
BACKGROUNDS = ["Soldat", "Acolyte", "Criminel", "Savant"]



# ------------------------- Modèle ------------------------- #
@dataclass
#Classe de données pour un personnage D&D.
class Character:
    name: str
    race: str
    classe: str
    background: str

    # Fonction pour afficher un résumé du personnage.
    def summary(self) -> str:
        return (
            "\n--- Résumé du personnage ---\n"
            f"Nom       : {self.name}\n"
            f"Race      : {self.race}\n"
            f"Classe    : {self.classe}\n"
            f"Historique: {self.background}\n"
        )


# ------------------------- UI Console ------------------------- #
class CharacterCreator:
# Gestion du flux de création en console (I/O).
# Séparé du modèle pour faciliter les tests et d'autres interfaces.

    def __init__(self, races, classes, backgrounds):
        self.races = list(races)
        self.classes = list(classes)
        self.backgrounds = list(backgrounds)

    @staticmethod
    def ask_choice(label, options):
        print(label)
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")
        while True:
            s = input("Votre choix (numéro) : ").strip()
            if s.isdigit():
                idx = int(s)
                if 1 <= idx <= len(options):
                    return options[idx - 1]
            print("→ Entrée invalide, réessayez.")

    @staticmethod
    # Demande le nom du personnage, avec valeur par défaut si entrée vide.
    def ask_name(prompt="Nom du personnage : ", default="Clochard"):
        name = input(prompt).strip()
        return name if name else default

    # Fonction principal de création.
    def run(self) -> Character:
        print("\n=== Créateur de personnage D&D 5e — Choix de base (OOP) ===\n")

        name = self.ask_name()
        race = self.ask_choice("\nChoisissez une race :", self.races)
        classe = self.ask_choice("\nChoisissez une classe :", self.classes)
        background = self.ask_choice("\nChoisissez un historique :", self.backgrounds)

        return Character(name=name, race=race, classe=classe, background=background)


# ------------------------- Programme principal ------------------------- #
def main():
    creator = CharacterCreator(RACES, CLASSES, BACKGROUNDS)
    character = creator.run()
    print(character.summary())

if __name__ == "__main__":
    main()
