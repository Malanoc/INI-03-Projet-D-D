# ==============================================================
#  Auteur        : Amin Torrisi, Ruben Ten Cate, Camille Bachmann et Marc Schilter
#  Date création : 16.09.2025
#  Dernière modif : 09.10.2025
#  Présentation : Interface graphique pour la création d'une fiche de personnage D&D basique
#                 en utilisant la programmation orientée objet (OOP) et tkinter.
#                 Possibilité de faire un export de cette dernière pour la sauvgarder.
#  Encodage : UTF-8
#  Version       : 2.0 (GUI)
# ==============================================================

# ----------------Importations ----------------
#Verifier d'avoir bien installé les librairies
from dataclasses import dataclass
import random
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from pdfrw import PdfReader, PdfWriter, PdfDict, PdfObject, PdfName, PdfString
import subprocess
import os
import time

# --------------------------Variables pour le combat bonus----------------
# Profil du Gobelin
ennemi_name = "Gobelin" #nom
ennemi_hitpoint = 0 #point de vie set plus tard
ennemi_ca = 13 #classe d'armure
ennemi_touche = 4 #bonus au touché
ennemi_dice = 6 #d6 pour les dégats
ennemi_deg = 2 #bonus au dégats

# ------------------------- Catalogues  ------------------------- #
#races disponibles
RACES = ["Humain", "Elfe", "Nain", "Halfelin"]
#classes disponibles
CLASSES = ["Guerrier", "Voleur", "Clerc", "Magicien"]
#historiques disponibles
BACKGROUNDS = ["Soldat", "Acolyte", "Criminel", "Savant"]
#compétences disponibles
SKILLS = ["Athlétisme (FOR)", "Acrobaties (DEX)", "Arcanes (INT)", "Discrétion (DEX)", "Dressage (SAG)",
          "Escamotage (DEX)", "Histoire (INT)", "Intimidation (CHA)", "Intuition (SAG)", "Investigation (INT)",
          "Médecine (SAG)", "Nature (INT)", "Perception (SAG)", "Persuasion (CHA)", "Religion (INT)",
          "Representation (CHA)", "Survie (SAG)", "Tromperie (CHA)"]
# Armes par classe
WEAPON_GUERRIER = ["Marteau de guerre (2 mains)", "Epée longue (1 main)", "Fléau d'arme (1 main)"]
WEAPON_MAGICIEN = ["Bâton de combat (2 mains)", "Dague (1 main)", "Gourdin (1 main)"]
WEAPON_VOLEUR = ["Arc long (2 mains)", "Dague (1 main)", "Rapière (1 main)"]
WEAPON_CLERC = ["Lance (2 mains)", "Masse d'arme (1 main)", "Hache (1 main)"]
# Options de bouclier
SHIELD = ["Equipé", "Non équipé"]

# ----------------Listes [statistiques]----------------
#caractéristiques
CARACTERISTIQUES = ["Force", "Dextérité", "Constitution", "Intelligence", "Sagesse", "Charisme"]
# Liste scores des caracteristiques option méthode fixe
SCORES_FIXES = [15, 14, 13, 12, 10, 8]
#méthodes à choix
METHODES_STAT = ["Méthode fixe", "Méthode aléatoire"]


# ------------------------- Modèle ------------------------- #
@dataclass
# Classe de données pour un personnage D&D.
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
    maitrise: int
    ca: int
    pv: int
    touche: int
    de_degats: int
    bonusdeg: int

    # ------------------------- Fonction de combat (bonus) ------------------------- #
    def combat(self, nom_ennemi, pv_ennemi, ca_ennemi, touche_ennemi, de_degats_ennemi, deg_ennemi, combat_callback):
        """
        Fonction de combat avec callback pour l'interface graphique
        combat_callback est une fonction qui prend un message en paramètre et l'affiche
        """
        combat_callback(f"Vous rencontrez un {nom_ennemi} !\n")
        #lorsque le perso et le gobelin sont en vie
        while self.pv > 0 and pv_ennemi > 0:
            # Tour du personnage
            combat_callback("=== Votre tour d'attaque ===\n")
            #jet de touche
            touche_chara = random.randint(1, 20) + self.touche
            if touche_chara >= ca_ennemi:
                #touche réussie
                combat_callback(f"Vous touchez le {nom_ennemi} !\n")
                #jet degat
                degats = random.randint(1, self.de_degats) + self.bonusdeg
                pv_ennemi -= degats
                # Au cas ou on tue l ennemi à ce moment
                if pv_ennemi <= 0:
                    combat_callback(
                        f"Vous infligez {degats} points de dégâts au {nom_ennemi}. Il lui reste 0 points de vie.\n")
                    break
                else:
                    #ennemi blessé mais pas mort
                    combat_callback(
                        f"Vous infligez {degats} points de dégâts au {nom_ennemi}. Il lui reste {pv_ennemi} points de vie.\n")
            else:
                #attaque ratée
                combat_callback(f"Vous ratez votre attaque contre le {nom_ennemi}.\n")

            # Tour de l'ennemi
            combat_callback(f"\n=== Tour du {nom_ennemi} ===\n")
            #jet de touche
            touche_ad = random.randint(1, 20) + touche_ennemi
            if touche_ad >= self.ca:
                #attaque réussie
                combat_callback(f"Le {nom_ennemi} vous touche !\n")
                #jet dégat
                degats_ad = random.randint(1, de_degats_ennemi) + deg_ennemi
                self.pv -= degats_ad
                #si l'ennemi tue le pj
                if self.pv <= 0:
                    combat_callback(
                        f"Le {nom_ennemi} vous inflige {degats_ad} points de dégâts. Il vous reste 0 points de vie.\n")
                else:
                    #touché mais en vie
                    combat_callback(
                        f"Le {nom_ennemi} vous inflige {degats_ad} points de dégâts. Il vous reste {self.pv} points de vie.\n\n")
            else:
                #attaque ratée
                combat_callback(f"Le {nom_ennemi} rate son attaque contre vous.\n\n")

        # le combat se termine
        if self.pv <= 0:
            #pj mort
            combat_callback("\n=== DÉFAITE ===\nVous avez été vaincu !\n")
            return False
        else:
            #gobelin mort
            combat_callback(f"\n=== VICTOIRE ===\nVous avez vaincu le {nom_ennemi} !\n")
            return True

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
            f"Compétences : {', '.join(self.skills)}\n"
            f"Arme      : {self.weapon}\n"
            f"Bouclier  : {self.shield}\n"
            f"Bonus de maitrise : {self.maitrise}\n"
            f"Classe d'armure : {self.ca}\n"
            f"Points de vie : {self.pv}\n"
            f"Bonus/Malus au touché : {self.touche}\n"
            f"Type dé dégâts : {self.de_degats}\n"
            f"Bonus de dégâts : {self.bonusdeg}\n"
        )

    # Fonction pour exporter la fiche de personnage en JSON.
    def to_json(self):
        return {
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
            'shield': self.shield,
            'maitrise': self.maitrise,
            'ca': self.ca,
            'pv': self.pv,
            'touche': self.touche,
            'de_degats': self.de_degats,
            'bonusdeg': self.bonusdeg
        }


# ---------------- remplisseur pdf - Ruben ten Cate ------------------------- #

def remplir_fiche_pdf(raw_data, template_pdf='Fiche personnage D&D.pdf'):
    output_pdf = raw_data["name"] + "_remplie.pdf"
    data = {}
    checkbox_fields = {}

    # Mapping des clés JSON aux champs PDF
    json_to_pdf = {
        "name": "CharacterName",
        "race": "Race",
        "classe": "ClassLevel",
        "background": "Background",
        "force": "STR",
        "modif_force": "STRmod",
        "dexterite": "DEX",
        "modif_dexterite": "DEXmod",
        "constitution": "CON",
        "modif_constitution": "CONmod",
        "intelligence": "INT",
        "modif_intelligence": "INTmod",
        "sagesse": "WIS",
        "modif_sagesse": "WISmod",
        "charisme": "CHA",
        "modif_charisme": "CHAmod",
        "maitrise": "ProfBonus",
        "ca": "AC",
        "pv": "HPMax",
        "touche": "Wpn1 AtkBonus",
        "de_degats": "Wpn1 Damage",
        "weapon": "Wpn Name"
    }

    # Remplissage des champs simples
    for json_key, pdf_field in json_to_pdf.items():
        value = raw_data.get(json_key)
        if value is not None:
            data[pdf_field] = str(value)

    # Champ bouclier
    data["Equipment"] = "Bouclier équipé" if raw_data.get("shield") == "Equipé" else "Bouclier non équipé"

    # Compétences avec maîtrise et modificateur
    competence_map = {
        "Acrobaties (DEX)": ("Check Box 23", "modif_dexterite", "Acrobaties"),
        "Arcanes (INT)": ("Check Box 24", "modif_intelligence", "Arcanes"),
        "Athlétisme (FOR)": ("Check Box 25", "modif_force", "Athlétisme"),
        "Discrétion (DEX)": ("Check Box 26", "modif_dexterite", "Discrétion"),
        "Dressage (SAG)": ("Check Box 27", "modif_sagesse", "Dressage"),
        "Escamotage (DEX)": ("Check Box 28", "modif_dexterite", "Escamotage"),
        "Histoire (INT)": ("Check Box 29", "modif_intelligence", "Histoire"),
        "Intimidation (CHA)": ("Check Box 30", "modif_charisme", "Intimidation"),
        "Intuition (SAG)": ("Check Box 31", "modif_sagesse", "Intuition"),
        "Investigation (INT)": ("Check Box 32", "modif_intelligence", "Investigation"),
        "Médecine (SAG)": ("Check Box 33", "modif_sagesse", "Médecine"),
        "Nature (INT)": ("Check Box 34", "modif_intelligence", "Nature"),
        "Perception (SAG)": ("Check Box 35", "modif_sagesse", "Perception"),
        "Persuasion (CHA)": ("Check Box 36", "modif_charisme", "Persuasion"),
        "Religion (INT)": ("Check Box 37", "modif_intelligence", "Religion"),
        "Représentation (CHA)": ("Check Box 38", "modif_charisme", "Représentation"),
        "Survie (SAG)": ("Check Box 39", "modif_sagesse", "Survie"),
        "Tromperie (CHA)": ("Check Box 40", "modif_charisme", "Tromperie")
    }

    # Bonus de maîtrise selon la maîtrise du personnage

    try:
        prof_bonus = int(raw_data.get("maitrise", 0))
    except (TypeError, ValueError):
        prof_bonus = 0

    for skill, (checkbox_name, modif_key, field_name) in competence_map.items():
        try:
            modif = int(raw_data.get(modif_key, 0))
        except (TypeError, ValueError):
            modif = 0

        if skill in raw_data.get("skills", []):
            checkbox_fields[checkbox_name] = True
            data[field_name] = str(modif + prof_bonus)
        else:
            data[field_name] = str(modif)

    # Valeurs des caractéristiques
    saving_throws = {
        "force": ("Check Box 11", "ST Strength"),
        "dexterite": ("Check Box 18", "ST Dexterity"),
        "constitution": ("Check Box 19", "ST Constitution"),
        "intelligence": ("Check Box 20", "ST Intelligence"),
        "sagesse": ("Check Box 21", "ST Wisdom"),
        "charisme": ("Check Box 22", "ST Charisma")
    }

    for stat, (checkbox_name, field_name) in saving_throws.items():
        if raw_data.get(f"save_{stat}") == "Oui":
            checkbox_fields[checkbox_name] = True
        try:
            value = int(raw_data.get(f"modif_{stat}", 0))
            data[field_name] = str(value)
        except (TypeError, ValueError):
            data[field_name] = "0"

    data["ProficienciesLang"] = ""

    # Remplissage du PDF
    template = PdfReader(template_pdf)
    if template.Root.AcroForm:
        template.Root.AcroForm.update(PdfDict(NeedAppearances=PdfObject('true')))

    for page in template.pages:
        annotations = page['/Annots']
        if annotations:
            for annotation in annotations:
                if annotation['/Subtype'] == '/Widget' and annotation['/T']:
                    key = annotation['/T'][1:-1].strip()
                    if key in data:
                        annotation.update(PdfDict(V=PdfString.encode(data[key])))
                    elif key in checkbox_fields:
                        annotation.update(PdfDict(AS=PdfName('Yes')))

    PdfWriter().write(output_pdf, template)
    time.sleep(0.5)
    if os.path.exists(output_pdf):
        print("✅ PDF généré :", output_pdf)
        subprocess.Popen([output_pdf], shell=True)
    else:
        print("❌ Échec : le fichier n’a pas été créé.")


# ------------------------- Interface Graphique ------------------------- #
class CharacterCreatorGUI:
    """
    Interface graphique pour la création de personnage D&D
    Utilise tkinter pour créer une interface utilisateur complète
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Créateur de personnage D&D 5e")
        self._center_window(800, 600)
        self.root.configure(bg='#2c3e50')

        # Variables pour stocker les choix de l'utilisateur
        self.character_data = {}
        self.available_scores = SCORES_FIXES.copy()
        self.available_skills = SKILLS.copy()
        self.selected_skills = []

        # Frame principal avec scrollbar
        self.main_canvas = tk.Canvas(root, bg='#2c3e50')
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.main_canvas.yview)

        # centrer le frame dans le canvas (Ruben)
        self.center_frame = tk.Frame(self.main_canvas, bg='#2c3e50')
        self.canvas_window = self.main_canvas.create_window(
            (self.root.winfo_width() // 2, 0), window=self.center_frame, anchor="n"
        )

        self.main_canvas.bind("<Configure>", self._resize_canvas)

        self.center_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )

        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Démarrer la création de personnage
        self.show_welcome_screen()

    def _resize_canvas(self, event):
        canvas_width = event.width
        self.main_canvas.itemconfig(self.canvas_window, width=canvas_width)
        self.main_canvas.coords(self.canvas_window, canvas_width // 2, 0)

    def _center_window(self, width, height):
        """Centre la fenêtre sur l'écran"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def clear_frame(self):
        """Efface tous les widgets du frame centré"""
        for widget in self.center_frame.winfo_children():
            widget.destroy()

    def show_welcome_screen(self):
        """Écran d'accueil"""
        self.clear_frame()

        title = tk.Label(self.center_frame,
                         text="Créateur de personnage D&D 5e",
                         font=("Arial", 24, "bold"),
                         bg='#2c3e50',
                         fg='#ecf0f1')
        title.pack(pady=30)

        subtitle = tk.Label(self.center_frame,
                            text="Bienvenue dans le créateur de personnage\nChoix de base (OOP)",
                            font=("Arial", 14),
                            bg='#2c3e50',
                            fg='#bdc3c7',
                            justify='center')
        subtitle.pack(pady=20)

        start_button = tk.Button(self.center_frame,
                                 text="Commencer la création",
                                 command=self.ask_name,
                                 font=("Arial", 14),
                                 bg='#27ae60',
                                 fg='white',
                                 padx=30,
                                 pady=15,
                                 cursor='hand2')
        start_button.pack(pady=30)

    def ask_name(self):
        """Demande le nom du personnage"""
        self.clear_frame()

        title = tk.Label(self.center_frame,
                         text="Nom du personnage",
                         font=("Arial", 18, "bold"),
                         bg='#2c3e50',
                         fg='#ecf0f1')
        title.pack(pady=20)

        name_entry = tk.Entry(self.center_frame,
                              font=("Arial", 14),
                              width=30)
        name_entry.pack(pady=20)
        name_entry.insert(0, "Super-Clochard")
        name_entry.focus()

        def on_continue():
            name = name_entry.get().strip()
            if not name:
                name = "Super-Clochard"
            self.character_data['name'] = name
            self.ask_race()

        continue_button = tk.Button(self.center_frame,
                                    text="Continuer",
                                    command=on_continue,
                                    font=("Arial", 12),
                                    bg='#3498db',
                                    fg='white',
                                    padx=20,
                                    pady=10,
                                    cursor='hand2')
        continue_button.pack(pady=20)

        # Permettre de valider avec Entrée
        name_entry.bind('<Return>', lambda e: on_continue())

    def ask_race(self):
        """Demande la race du personnage"""
        self.clear_frame()

        title = tk.Label(self.center_frame,
                         text="Choisissez une race",
                         font=("Arial", 18, "bold"),
                         bg='#2c3e50',
                         fg='#ecf0f1')
        title.pack(pady=20)

        for race in RACES:
            btn = tk.Button(self.center_frame,
                            text=race,
                            command=lambda r=race: self.select_race(r),
                            font=("Arial", 12),
                            bg='#34495e',
                            fg='white',
                            width=20,
                            padx=10,
                            pady=10,
                            cursor='hand2')
            btn.pack(pady=5)

    def select_race(self, race):
        """Enregistre la race et passe à la classe"""
        self.character_data['race'] = race
        self.ask_classe()

    def ask_classe(self):
        """Demande la classe du personnage"""
        self.clear_frame()

        title = tk.Label(self.center_frame,
                         text="Choisissez une classe",
                         font=("Arial", 18, "bold"),
                         bg='#2c3e50',
                         fg='#ecf0f1')
        title.pack(pady=20)

        for classe in CLASSES:
            btn = tk.Button(self.center_frame,
                            text=classe,
                            command=lambda c=classe: self.select_classe(c),
                            font=("Arial", 12),
                            bg='#34495e',
                            fg='white',
                            width=20,
                            padx=10,
                            pady=10,
                            cursor='hand2')
            btn.pack(pady=5)

    def select_classe(self, classe):
        """Enregistre la classe et passe à la méthode de stats"""
        self.character_data['classe'] = classe
        self.ask_stat_method()

    def ask_stat_method(self):
        """Demande la méthode de génération des statistiques"""
        self.clear_frame()

        title = tk.Label(self.center_frame,
                         text="Choisissez une méthode de génération des statistiques",
                         font=("Arial", 18, "bold"),
                         bg='#2c3e50',
                         fg='#ecf0f1')
        title.pack(pady=20)

        # Méthode fixe
        fixed_frame = tk.Frame(self.center_frame, bg='#34495e', relief='raised', bd=2)
        fixed_frame.pack(pady=10, padx=20, fill='x')

        fixed_title = tk.Label(fixed_frame,
                               text="Méthode fixe",
                               font=("Arial", 14, "bold"),
                               bg='#34495e',
                               fg='#ecf0f1')
        fixed_title.pack(pady=10)

        fixed_desc = tk.Label(fixed_frame,
                              text="Attribuez les scores définis [15, 14, 13, 12, 10, 8]\naux 6 caractéristiques",
                              font=("Arial", 10),
                              bg='#34495e',
                              fg='#bdc3c7')
        fixed_desc.pack(pady=5)

        fixed_button = tk.Button(fixed_frame,
                                 text="Choisir la méthode fixe",
                                 command=self.use_fixed_method,
                                 font=("Arial", 12),
                                 bg='#3498db',
                                 fg='white',
                                 padx=20,
                                 pady=10,
                                 cursor='hand2')
        fixed_button.pack(pady=10)

        # Méthode aléatoire
        random_frame = tk.Frame(self.center_frame, bg='#34495e', relief='raised', bd=2)
        random_frame.pack(pady=10, padx=20, fill='x')

        random_title = tk.Label(random_frame,
                                text="Méthode aléatoire",
                                font=("Arial", 14, "bold"),
                                bg='#34495e',
                                fg='#ecf0f1')
        random_title.pack(pady=10)

        random_desc = tk.Label(random_frame,
                               text="Les scores seront générés automatiquement\npar trois jets de dés 🎲 à 6 faces pour chaque caractéristique",
                               font=("Arial", 10),
                               bg='#34495e',
                               fg='#bdc3c7')
        random_desc.pack(pady=5)

        random_button = tk.Button(random_frame,
                                  text="Choisir la méthode aléatoire",
                                  command=self.use_random_method,
                                  font=("Arial", 12),
                                  bg='#e74c3c',
                                  fg='white',
                                  padx=20,
                                  pady=10,
                                  cursor='hand2')
        random_button.pack(pady=10)

    def use_fixed_method(self):
        """Utilise la méthode fixe pour les statistiques"""
        self.character_data['stat_method'] = 'fixe'
        self.available_scores = SCORES_FIXES.copy()
        self.ask_stat_assignment('force', 0)

    def use_random_method(self):
        """Utilise la méthode aléatoire pour les statistiques"""
        self.character_data['stat_method'] = 'aléatoire'

        def roll_dice():
            #jet de dé pour définir les cara
            rolls = [random.randint(1, 6) for _ in range(3)]
            return sum(rolls)

        #cara définie par un jet de dé
        self.character_data['force'] = roll_dice()
        self.character_data['dexterite'] = roll_dice()
        self.character_data['constitution'] = roll_dice()
        self.character_data['intelligence'] = roll_dice()
        self.character_data['sagesse'] = roll_dice()
        self.character_data['charisme'] = roll_dice()

        self.show_generated_stats()

    def ask_stat_assignment(self, stat_name, index):
        """Demande l'attribution d'un score fixe à une caractéristique"""
        self.clear_frame()

        # Liste des caractéristiques
        stats_list = ['force', 'dexterite', 'constitution', 'intelligence', 'sagesse', 'charisme']
        display_names = ['Force', 'Dextérité', 'Constitution', 'Intelligence', 'Sagesse', 'Charisme']

        title = tk.Label(self.center_frame,
                         text=f"Choisissez un score pour {display_names[index]}",
                         font=("Arial", 18, "bold"),
                         bg='#2c3e50',
                         fg='#ecf0f1')
        title.pack(pady=20)

        info = tk.Label(self.center_frame,
                        text=f"Scores disponibles : {', '.join(map(str, self.available_scores))}",
                        font=("Arial", 12),
                        bg='#2c3e50',
                        fg='#bdc3c7')
        info.pack(pady=10)

        for score in self.available_scores:
            btn = tk.Button(self.center_frame,
                            text=str(score),
                            command=lambda s=score: self.select_stat(stat_name, s, index),
                            font=("Arial", 14, "bold"),
                            bg='#34495e',
                            fg='white',
                            width=10,
                            padx=10,
                            pady=10,
                            cursor='hand2')
            btn.pack(pady=5)

    def select_stat(self, stat_name, score, index):
        """Enregistre le score de la caractéristique et passe à la suivante"""
        self.character_data[stat_name] = score
        self.available_scores.remove(score)

        stats_list = ['force', 'dexterite', 'constitution', 'intelligence', 'sagesse', 'charisme']

        if index < 5:
            self.ask_stat_assignment(stats_list[index + 1], index + 1)
        else:
            self.show_generated_stats()

    def show_generated_stats(self):
        """Affiche les statistiques générées"""
        self.clear_frame()

        title = tk.Label(self.center_frame,
                         text="Statistiques générées",
                         font=("Arial", 18, "bold"),
                         bg='#2c3e50',
                         fg='#ecf0f1')
        title.pack(pady=20)

        # Modif des stats selon les races choisies
        if self.character_data['race'] == "Humain":
            self.character_data['force'] += 1
            self.character_data['dexterite'] += 1
            self.character_data['constitution'] += 1
            self.character_data['intelligence'] += 1
            self.character_data['sagesse'] += 1
            self.character_data['charisme'] += 1
        elif self.character_data['race'] == "Elfe":
            self.character_data['dexterite'] += 2
            self.character_data['intelligence'] += 1  # en principe sous-race haut elfe dans les règles originales
        elif self.character_data['race'] == "Nain":
            self.character_data['constitution'] += 2
            self.character_data['force'] += 2  # en principe sous-race nain des montagnes dans les règles originales
        elif self.character_data['race'] == "Halfelin":
            self.character_data['dexterite'] += 2
            self.character_data[
                'charisme'] += 1  # en principe sous-race halfelin pieds-léger dans les règles originales

        # Calcul des modificateurs
        self.character_data['modif_force'] = int((self.character_data['force'] - 10) // 2)
        self.character_data['modif_dexterite'] = int((self.character_data['dexterite'] - 10) // 2)
        self.character_data['modif_constitution'] = int((self.character_data['constitution'] - 10) // 2)
        self.character_data['modif_intelligence'] = int((self.character_data['intelligence'] - 10) // 2)
        self.character_data['modif_sagesse'] = int((self.character_data['sagesse'] - 10) // 2)
        self.character_data['modif_charisme'] = int((self.character_data['charisme'] - 10) // 2)

        stats_frame = tk.Frame(self.center_frame, bg='#34495e', relief='raised', bd=2)
        stats_frame.pack(pady=10, padx=50, fill='x')

        stats = [
            ('Force', self.character_data['force'], self.character_data['modif_force']),
            ('Dextérité', self.character_data['dexterite'], self.character_data['modif_dexterite']),
            ('Constitution', self.character_data['constitution'], self.character_data['modif_constitution']),
            ('Intelligence', self.character_data['intelligence'], self.character_data['modif_intelligence']),
            ('Sagesse', self.character_data['sagesse'], self.character_data['modif_sagesse']),
            ('Charisme', self.character_data['charisme'], self.character_data['modif_charisme'])
        ]

        for stat_name, value, modifier in stats:
            stat_line = tk.Label(stats_frame,
                                 text=f"{stat_name}: {value} (Modificateur: {modifier:+d})",
                                 font=("Arial", 12),
                                 bg='#34495e',
                                 fg='#ecf0f1')
            stat_line.pack(pady=5)

        continue_button = tk.Button(self.center_frame,
                                    text="Continuer",
                                    command=self.ask_background,
                                    font=("Arial", 12),
                                    bg='#3498db',
                                    fg='white',
                                    padx=20,
                                    pady=10,
                                    cursor='hand2')
        continue_button.pack(pady=20)

    def ask_background(self):
        """Demande l'historique du personnage"""
        self.clear_frame()

        title = tk.Label(self.center_frame,
                         text="Choisissez un historique",
                         font=("Arial", 18, "bold"),
                         bg='#2c3e50',
                         fg='#ecf0f1')
        title.pack(pady=20)

        for background in BACKGROUNDS:
            btn = tk.Button(self.center_frame,
                            text=background,
                            command=lambda b=background: self.select_background(b),
                            font=("Arial", 12),
                            bg='#34495e',
                            fg='white',
                            width=20,
                            padx=10,
                            pady=10,
                            cursor='hand2')
            btn.pack(pady=5)

    def select_background(self, background):
        """Enregistre l'historique et passe au choix d'arme"""
        self.character_data['background'] = background
        self.ask_weapon()

    def ask_weapon(self):
        """Demande le choix de l'arme en fonction de la classe"""
        self.clear_frame()

        title = tk.Label(self.center_frame,
                         text="Choisissez une arme",
                         font=("Arial", 18, "bold"),
                         bg='#2c3e50',
                         fg='#ecf0f1')
        title.pack(pady=20)

        # Déterminer les armes disponibles selon la classe
        classe = self.character_data['classe']
        if classe == "Guerrier":
            weapons = WEAPON_GUERRIER
        elif classe == "Magicien":
            weapons = WEAPON_MAGICIEN
        elif classe == "Voleur":
            weapons = WEAPON_VOLEUR
        elif classe == "Clerc":
            weapons = WEAPON_CLERC

        for weapon in weapons:
            btn = tk.Button(self.center_frame,
                            text=weapon,
                            command=lambda w=weapon: self.select_weapon(w),
                            font=("Arial", 12),
                            bg='#34495e',
                            fg='white',
                            width=30,
                            padx=10,
                            pady=10,
                            cursor='hand2')
            btn.pack(pady=5)

    def select_weapon(self, weapon):
        """Enregistre l'arme et passe au choix du bouclier"""
        self.character_data['weapon'] = weapon

        # Vérifier si l'arme nécessite 2 mains (pas de bouclier possible)
        two_handed_weapons = ["Marteau de guerre (2 mains)", "Arc long (2 mains)",
                              "Bâton de combat (2 mains)", "Lance (2 mains)"]

        if weapon in two_handed_weapons:
            self.character_data['shield'] = "Non équipé"
            self.calculate_combat_stats()
            self.ask_skills()
        else:
            self.ask_shield()

    def ask_shield(self):
        """Demande si le personnage équipe un bouclier"""
        self.clear_frame()

        title = tk.Label(self.center_frame,
                         text="Voulez-vous équiper un bouclier ?",
                         font=("Arial", 18, "bold"),
                         bg='#2c3e50',
                         fg='#ecf0f1')
        title.pack(pady=20)

        for shield in SHIELD:
            btn = tk.Button(self.center_frame,
                            text=shield,
                            command=lambda s=shield: self.select_shield(s),
                            font=("Arial", 12),
                            bg='#34495e',
                            fg='white',
                            width=20,
                            padx=10,
                            pady=10,
                            cursor='hand2')
            btn.pack(pady=5)

    def select_shield(self, shield):
        """Enregistre le choix du bouclier et calcule les stats de combat"""
        self.character_data['shield'] = shield
        self.calculate_combat_stats()
        self.ask_skills()

    def calculate_combat_stats(self):
        """Calcule les statistiques de combat (CA, PV, touché, dégâts)"""
        classe = self.character_data['classe']
        weapon = self.character_data['weapon']
        shield = self.character_data['shield']

        modif_constitution = self.character_data['modif_constitution']
        modif_force = self.character_data['modif_force']
        modif_dexterite = self.character_data['modif_dexterite']

        maitrise = 2
        ca = 10

        # Calcul des PV et CA de base selon la classe
        if classe == "Guerrier":
            pv = 10 + modif_constitution
            ca = 18  # Armure de plaques
            nbr_comp = 2
        elif classe == "Magicien":
            pv = 6 + modif_constitution
            ca += modif_dexterite
            nbr_comp = 2
        elif classe == "Voleur":
            pv = 8 + modif_constitution
            ca = ca + 1 + modif_dexterite  # Armure de cuir
            nbr_comp = 4
        elif classe == "Clerc":
            pv = 8 + modif_constitution
            ca = ca + 4 + modif_dexterite  # Armure de mailles
            nbr_comp = 2

        # Bonus de CA si bouclier équipé
        if shield == "Equipé":
            ca += 2

        # Calcul du bonus au touché et des dégâts selon l'arme + bonus au dégat
        weapon_stats = {
            "Marteau de guerre (2 mains)": (modif_force + maitrise, 8, modif_force),
            "Epée longue (1 main)": (modif_force + maitrise, 8, modif_force),
            "Fléau d'arme (1 main)": (modif_force + maitrise, 8, modif_force),
            "Bâton de combat (2 mains)": (modif_dexterite + maitrise, 6, modif_force),
            "Dague (1 main)": (modif_dexterite + maitrise, 4, modif_dexterite),
            "Gourdin (1 main)": (modif_dexterite + maitrise, 6, modif_force),
            "Arc long (2 mains)": (modif_dexterite + maitrise, 8, modif_dexterite),
            "Rapière (1 main)": (modif_dexterite + maitrise, 8, modif_dexterite),
            "Lance (2 mains)": (modif_force + maitrise, 6, modif_force),
            "Masse d'arme (1 main)": (modif_force + maitrise, 6, modif_force),
            "Hache (1 main)": (modif_force + maitrise, 6, modif_force)
        }

        touche, de_degats, bonusdeg = weapon_stats.get(weapon, (0, 0))

        # Enregistrer les statistiques
        self.character_data['maitrise'] = maitrise
        self.character_data['ca'] = ca
        self.character_data['pv'] = pv
        self.character_data['touche'] = touche
        self.character_data['de_degats'] = de_degats
        self.character_data['bonusdeg'] = bonusdeg
        self.character_data['nbr_comp'] = nbr_comp

    def ask_skills(self):
        """Demande le choix des compétences"""
        self.clear_frame()

        nbr_comp = self.character_data['nbr_comp']

        title = tk.Label(self.center_frame,
                         text=f"Choisissez vos compétences ({len(self.selected_skills)}/{nbr_comp})",
                         font=("Arial", 18, "bold"),
                         bg='#2c3e50',
                         fg='#ecf0f1')
        title.pack(pady=20)

        info = tk.Label(self.center_frame,
                        text=f"Sélectionnez {nbr_comp} compétences pour votre personnage",
                        font=("Arial", 12),
                        bg='#2c3e50',
                        fg='#bdc3c7')
        info.pack(pady=10)

        # Frame pour les compétences sélectionnées
        if self.selected_skills:
            selected_frame = tk.Frame(self.center_frame, bg='#27ae60', relief='raised', bd=2)
            selected_frame.pack(pady=10, padx=50, fill='x')

            selected_label = tk.Label(selected_frame,
                                      text="Compétences sélectionnées :",
                                      font=("Arial", 12, "bold"),
                                      bg='#27ae60',
                                      fg='white')
            selected_label.pack(pady=5)

            for skill in self.selected_skills:
                skill_label = tk.Label(selected_frame,
                                       text=f"✓ {skill}",
                                       font=("Arial", 10),
                                       bg='#27ae60',
                                       fg='white')
                skill_label.pack(pady=2)

        # Frame avec scrollbar pour les compétences disponibles
        skills_frame = tk.Frame(self.center_frame, bg='#2c3e50')
        skills_frame.pack(pady=10, fill='both', expand=True)

        for skill in self.available_skills:
            btn = tk.Button(skills_frame,
                            text=skill,
                            command=lambda s=skill: self.select_skill(s),
                            font=("Arial", 11),
                            bg='#34495e',
                            fg='white',
                            width=30,
                            padx=10,
                            pady=8,
                            cursor='hand2')
            btn.pack(pady=3)

    def select_skill(self, skill):
        """Enregistre une compétence sélectionnée"""
        nbr_comp = self.character_data['nbr_comp']

        if len(self.selected_skills) < nbr_comp:
            self.selected_skills.append(skill)
            self.available_skills.remove(skill)

            if len(self.selected_skills) == nbr_comp:
                self.character_data['skills'] = self.selected_skills
                self.create_character()
            else:
                self.ask_skills()

    def create_character(self):
        """Crée l'objet Character et affiche le résumé"""
        character = Character(
            name=self.character_data['name'],
            race=self.character_data['race'],
            classe=self.character_data['classe'],
            force=self.character_data['force'],
            modif_force=self.character_data['modif_force'],
            dexterite=self.character_data['dexterite'],
            modif_dexterite=self.character_data['modif_dexterite'],
            constitution=self.character_data['constitution'],
            modif_constitution=self.character_data['modif_constitution'],
            intelligence=self.character_data['intelligence'],
            modif_intelligence=self.character_data['modif_intelligence'],
            sagesse=self.character_data['sagesse'],
            modif_sagesse=self.character_data['modif_sagesse'],
            charisme=self.character_data['charisme'],
            modif_charisme=self.character_data['modif_charisme'],
            background=self.character_data['background'],
            skills=self.character_data['skills'],
            weapon=self.character_data['weapon'],
            shield=self.character_data['shield'],
            maitrise=self.character_data['maitrise'],
            ca=self.character_data['ca'],
            pv=self.character_data['pv'],
            touche=self.character_data['touche'],
            de_degats=self.character_data['de_degats'],
            bonusdeg=self.character_data['bonusdeg']
        )

        self.character = character
        self.show_summary()

    def show_summary(self):
        """Affiche le résumé du personnage"""
        self.clear_frame()

        title = tk.Label(self.center_frame,
                         text="Fiche de personnage créée !",
                         font=("Arial", 20, "bold"),
                         bg='#2c3e50',
                         fg='#27ae60')
        title.pack(pady=20)

        # Zone de texte pour le résumé
        summary_text = scrolledtext.ScrolledText(self.center_frame,
                                                 width=70,
                                                 height=25,
                                                 font=("Courier", 10),
                                                 bg='#ecf0f1',
                                                 fg='#2c3e50',
                                                 wrap=tk.WORD)
        summary_text.pack(pady=10, padx=20)
        summary_text.insert(tk.END, self.character.summary())
        summary_text.config(state=tk.DISABLED)

        # Boutons d'action
        buttons_frame = tk.Frame(self.center_frame, bg='#2c3e50')
        buttons_frame.pack(pady=20)

        export_button = tk.Button(buttons_frame,
                                  text="Exporter en JSON",
                                  command=self.export_character,
                                  font=("Arial", 12),
                                  bg='#3498db',
                                  fg='white',
                                  padx=20,
                                  pady=10,
                                  cursor='hand2')
        export_button.grid(row=0, column=0, padx=10)

        combat_button = tk.Button(buttons_frame,
                                  text="Combat contre le Gobelin !",
                                  command=self.start_combat,
                                  font=("Arial", 12),
                                  bg='#e74c3c',
                                  fg='white',
                                  padx=20,
                                  pady=10,
                                  cursor='hand2')
        combat_button.grid(row=0, column=1, padx=10)

        new_char_button = tk.Button(buttons_frame,
                                    text="Nouveau personnage",
                                    command=self.restart,
                                    font=("Arial", 12),
                                    bg='#95a5a6',
                                    fg='white',
                                    padx=20,
                                    pady=10,
                                    cursor='hand2')
        new_char_button.grid(row=0, column=2, padx=10)

    # -------------- Fonctions d'export PDF et JSON - Ruben ten Cate ----------------- #

    def export_character(self):
        """Exporte le personnage en JSON et en PDF"""
        if not hasattr(self, "character"):
            messagebox.showerror("Erreur", "Aucun personnage à exporter.")
            return

        data = self.character.to_json()
        json_filename = f"{self.character.name}.json"
        pdf_filename = f"{self.character.name}_remplie.pdf"

        # Export JSON
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Export PDF
        try:
            remplir_fiche_pdf(data)
        except Exception as e:
            messagebox.showerror("Erreur PDF", f"Le PDF n’a pas pu être généré :\n{e}")
            return

        # Confirmation
        messagebox.showinfo("Export réussi",
                            f"Fiche exportée en JSON ({json_filename}) et en PDF ({pdf_filename})")

    # --------------- Combat simple contre un gobelin - Camille Bachmann ------------------------- #

    def start_combat(self):
        """Lance le combat contre le gobelin"""
        self.clear_frame()

        title = tk.Label(self.center_frame,
                         text="⚔️ COMBAT CONTRE LE GOBELIN ⚔️",
                         font=("Arial", 20, "bold"),
                         bg='#2c3e50',
                         fg='#e74c3c')
        title.pack(pady=20)

        # Zone de texte pour le log de combat
        self.combat_log = scrolledtext.ScrolledText(self.center_frame,
                                                    width=70,
                                                    height=20,
                                                    font=("Courier", 10),
                                                    bg='#ecf0f1',
                                                    fg='#2c3e50',
                                                    wrap=tk.WORD)
        self.combat_log.pack(pady=10, padx=20)

        # Bouton pour attaquer
        self.attack_button = tk.Button(self.center_frame,
                                       text="⚔️ Attaquer !",
                                       command=self.process_combat_turn,
                                       font=("Arial", 14, "bold"),
                                       bg='#e74c3c',
                                       fg='white',
                                       padx=30,
                                       pady=15,
                                       cursor='hand2')
        self.attack_button.pack(pady=20)

        # Initialiser les variables de combat
        self.combat_enemy_hp = ennemi_hitpoint + random.randint(1,6) + random.randint(1,6) #2d6 pv redéfinis à chaque combat
        self.combat_player_hp = self.character.pv
        self.combat_finished = False

        self.log_combat(f"Vous rencontrez un {ennemi_name} !\n")
        self.log_combat(f"Vos PV: {self.combat_player_hp} | PV du {ennemi_name}: {self.combat_enemy_hp}\n")
        self.log_combat("=" * 50 + "\n\n")

    def log_combat(self, message):
        """Ajoute un message au log de combat"""
        self.combat_log.config(state=tk.NORMAL)
        self.combat_log.insert(tk.END, message)
        self.combat_log.see(tk.END)
        self.combat_log.config(state=tk.DISABLED)
        self.combat_log.update()

    def process_combat_turn(self):
        #similaire à ce qui est expliqué tout en haut
        """Traite un tour de combat"""
        if self.combat_finished:
            return

        # Tour du joueur
        self.log_combat("=== Votre tour d'attaque ===\n")
        touche_chara = random.randint(1, 20) + self.character.touche

        if touche_chara >= ennemi_ca:
            self.log_combat(f"Vous touchez le {ennemi_name} !\n")
            degats = random.randint(1, self.character.de_degats) + self.character.bonusdeg
            self.combat_enemy_hp -= degats

            if self.combat_enemy_hp <= 0:
                self.log_combat(
                    f"Vous infligez {degats} points de dégâts au {ennemi_name}. Il lui reste 0 points de vie.\n\n")
                self.log_combat("=" * 50 + "\n")
                self.log_combat(f"🎉 VICTOIRE ! 🎉\nVous avez vaincu le {ennemi_name} !\n")
                self.combat_finished = True
                self.attack_button.config(text="Retour au résumé", command=self.show_summary)
                return
            else:
                self.log_combat(
                    f"Vous infligez {degats} points de dégâts au {ennemi_name}. Il lui reste {self.combat_enemy_hp} points de vie.\n\n")
        else:
            self.log_combat(f"Vous ratez votre attaque contre le {ennemi_name}.\n\n")

        # Tour de l'ennemi
        self.log_combat(f"=== Tour du {ennemi_name} ===\n")
        touche_ad = random.randint(1, 20) + ennemi_touche

        if touche_ad >= self.character.ca:
            self.log_combat(f"Le {ennemi_name} vous touche !\n")
            degats_ad = random.randint(1, ennemi_dice) + ennemi_deg
            self.combat_player_hp -= degats_ad

            if self.combat_player_hp <= 0:
                self.log_combat(
                    f"Le {ennemi_name} vous inflige {degats_ad} points de dégâts. Il vous reste 0 points de vie.\n\n")
                self.log_combat("=" * 50 + "\n")
                self.log_combat(f"💀 DÉFAITE 💀\nVous avez été vaincu !\n")
                self.combat_finished = True
                self.attack_button.config(text="Retour au résumé", command=self.show_summary)
                return
            else:
                self.log_combat(
                    f"Le {ennemi_name} vous inflige {degats_ad} points de dégâts. Il vous reste {self.combat_player_hp} points de vie.\n\n")
        else:
            self.log_combat(f"Le {ennemi_name} rate son attaque contre vous.\n\n")

        self.log_combat(f"Vos PV: {self.combat_player_hp} | PV du {ennemi_name}: {self.combat_enemy_hp}\n")
        self.log_combat("=" * 50 + "\n\n")

    def restart(self):
        """Redémarre la création de personnage"""
        self.character_data = {}
        self.available_scores = SCORES_FIXES.copy()
        self.available_skills = SKILLS.copy()
        self.selected_skills = []
        self.show_welcome_screen()


# ------------------------- Programme principal ------------------------- #
def main():
    root = tk.Tk()
    app = CharacterCreatorGUI(root)
    root.mainloop()

#Lancement du programme
if __name__ == "__main__":
    main()