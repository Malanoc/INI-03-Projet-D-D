# INI-03-Projet-D-D

## 📜 Description

Créateur de personnage pour Donjons & Dragons 5e développé en Python avec une interface graphique moderne utilisant tkinter.

Ce projet permet de créer des fiches de personnage D&D complètes avec attribution des statistiques, choix d'équipement, sélection de compétences, et même un système de combat contre un Gobelin !

## 👥 Auteurs

- **Amin Torrisi**
- **Ruben Ten Cate**
- **Camille Bachmann**
- **Marc Schilter**

## 📅 Informations du projet

- **Date de création** : 16.09.2025
- **Dernière modification** : 06.10.2025
- **Version** : 2.0 (Interface Graphique)
- **Encodage** : UTF-8

## 🚀 Lancement de l'application

### Prérequis
- Python 3.10 ou supérieur
- tkinter (inclus par défaut avec Python)
- pdfrw (a importer)

### Commande

```bash
cd "Projet de Groupe"
python "Projet de groupe Amin Torrisi, Ruben Ten Cate, Camille Bachmann et Marc Schilter - GUI.py"
```

## ✨ Fonctionnalités

### 🎭 Création de personnage complète

1. **Nom du personnage**
   - Saisie libre avec valeur par défaut

2. **Choix de la race**
   - Humain
   - Elfe
   - Nain
   - Halfelin

3. **Choix de la classe**
   - Guerrier (PV: 10+CON, CA: 18)
   - Voleur (PV: 8+CON, CA: 11+DEX)
   - Clerc (PV: 8+CON, CA: 14+DEX)
   - Magicien (PV: 6+CON, CA: 10+DEX)

4. **Génération des statistiques**
   - **Méthode fixe** : Attribution manuelle des scores [15, 14, 13, 12, 10, 8]
   - **Méthode aléatoire** : Lancer de 3d6 pour chaque caractéristique
   - Calcul automatique des modificateurs

5. **Choix de l'historique**
   - Soldat
   - Acolyte
   - Criminel
   - Savant

6. **Sélection de l'équipement**
   
   **Armes par classe :**
   - **Guerrier** : Marteau de guerre, Épée longue, Fléau d'arme
   - **Magicien** : Bâton de combat, Dague, Gourdin
   - **Voleur** : Arc long, Dague, Rapière
   - **Clerc** : Lance, Masse d'arme, Hache
   
   **Bouclier :**
   - Disponible uniquement pour les armes à 1 main
   - Bonus de +2 à la CA

7. **Compétences**
   - **Guerrier, Magicien, Clerc** : 2 compétences
   - **Voleur** : 4 compétences
   - 18 compétences disponibles avec leur caractéristique associée

### 📊 Statistiques calculées automatiquement

- **Bonus de maîtrise** : +2
- **Classe d'armure (CA)** : Selon classe + armure + bouclier
- **Points de vie (PV)** : Selon classe + modificateur de Constitution
- **Bonus au touché** : Selon arme + bonus de maîtrise
- **Dés de dégâts** : Selon arme (d4, d6 ou d8)

### 💾 Export JSON

Sauvegarde complète de la fiche de personnage au format JSON avec :
- Toutes les caractéristiques et modificateurs
- Équipement complet
- Compétences sélectionnées
- Statistiques de combat

### ⚔️ Système de combat

Combat interactif tour par tour contre un **Gobelin** :
- **PV du Gobelin** : 15
- **CA du Gobelin** : 13
- **Bonus au touché** : +4
- **Dégâts** : 1d6+4

Système de combat complet avec :
- Jets d'attaque automatiques (d20 + bonus)
- Calcul des dégâts
- Gestion des points de vie
- Messages de victoire/défaite

## 🎨 Interface Graphique

### Design moderne
- **Thème sombre professionnel** (palette gris-bleu)
- **Boutons colorés** avec codes couleur intuitifs
- **Navigation fluide** avec scrollbars
- **Polices lisibles** (Arial pour l'interface, Courier pour les textes)
- **Feedback visuel** sur les interactions

### Expérience utilisateur
- ✅ Navigation intuitive étape par étape
- ✅ Validation instantanée des choix
- ✅ Affichage persistant des informations
- ✅ Zone de texte scrollable pour le résumé
- ✅ Log de combat en temps réel
- ✅ Possibilité de créer plusieurs personnages

## 📁 Structure du projet

```
INI-03-Projet-D-D/
├── .gitignore
├── README.md
└── Projet de Groupe/
    └── Projet de groupe Amin Torrisi, Ruben Ten Cate, Camille Bachmann et Marc Schilter - GUI.py
```

## 🛠️ Architecture technique

### Programmation Orientée Objet

**Classe `Character` (Dataclass)**
```python
@dataclass
class Character:
    # Identité
    name, race, classe, background
    
    # Caractéristiques + modificateurs
    force, modif_force
    dexterite, modif_dexterite
    constitution, modif_constitution
    intelligence, modif_intelligence
    sagesse, modif_sagesse
    charisme, modif_charisme
    
    # Équipement et compétences
    weapon, shield, skills
    
    # Statistiques de combat
    maitrise, ca, pv, touche, de_degats
```

**Classe `CharacterCreatorGUI`**
- Gestion de l'interface graphique tkinter
- Navigation entre les différentes étapes
- Gestion de l'état de création
- Système de combat interactif

### Catalogues de données
- `RACES` : Liste des races disponibles
- `CLASSES` : Liste des classes disponibles
- `BACKGROUNDS` : Liste des historiques
- `SKILLS` : 18 compétences avec caractéristique associée
- `WEAPON_*` : Armes par classe
- `SCORES_FIXES` : Scores pour la méthode fixe

## 🎮 Guide d'utilisation

1. **Lancez l'application** → Écran d'accueil
2. **Cliquez sur "Commencer"** → Entrez le nom
3. **Sélectionnez race et classe** → Boutons colorés
4. **Choisissez la méthode de stats** → Fixe ou aléatoire
5. **Attribuez les scores** → Selon la méthode choisie
6. **Sélectionnez historique** → 4 options disponibles
7. **Choisissez arme et bouclier** → Selon votre classe
8. **Sélectionnez vos compétences** → 2 ou 4 selon la classe
9. **Admirez votre personnage** → Résumé complet
10. **Exportez et combattez** → JSON + Combat contre Gobelin

## 💡 Conseils de jeu

### Recommandations par classe

**🗡️ Guerrier**
- Priorisez Force et Constitution
- Haute CA (18) = tank parfait
- Bons PV (10+CON)
- Idéal pour le combat rapproché

**🎯 Voleur**
- Priorisez Dextérité
- 4 compétences = polyvalence maximale
- Attaques à distance avec l'Arc long
- Parfait pour l'esquive et la discrétion

**🛡️ Clerc**
- Équilibrez Sagesse et Constitution
- Bonne CA avec armure de mailles
- Versatile en combat et soutien

**📚 Magicien**
- Priorisez Intelligence
- CA basse = restez en arrière
- PV faibles = évitez le combat rapproché
- Compensez avec la stratégie

## 🐛 Dépannage

### L'interface ne se lance pas
- Vérifiez que Python 3.10+ est installé : `python --version`
- Sur Linux, installez tkinter : `sudo apt-get install python3-tk`
- Sur macOS, réinstallez Python depuis python.org
- Vérifiez que les libraries nécessaires soient importées

### Erreur d'encodage
- Le projet utilise UTF-8
- Assurez-vous que votre terminal supporte UTF-8

## 📝 Notes de développement

### Technologies utilisées
- **Python 3.10+** : Langage principal
- **tkinter** : Interface graphique
- **dataclasses** : Modélisation des données
- **json** : Export des fiches
- **random** : Génération aléatoire (combat, dés)

### Bonnes pratiques appliquées
- ✅ Programmation Orientée Objet
- ✅ Séparation Modèle/Vue (MVC)
- ✅ Code commenté et documenté
- ✅ Gestion d'erreurs
- ✅ Interface utilisateur intuitive
- ✅ Git workflow propre


Projet réalisé dans le cadre du module **INI-03** -

---

**Bon jeu et que les dés vous soient favorables ! 🎲**

---

## 📊 Répartition du travail

**Marc:**
- Création du personnage de base (Race, classe, background, nom) + test des entrées de l'utilisateur pour chaque fonction.
- Création de la structure orientée objet et fonctions de bases
- Création du Repo GitHub
- Création et conception du diagramme de flux

**Camille:**
- Création du système de séléction de l'équipement et compétences
- Création du système de sauvegarde de la fiche en format json
- Ajout du combat et des caractéristiques associées
- Ajout de l'influence de la race sur les caractéristiques
- Création et conception du diagramme de flux

**Ruben:** 
- Création du système de séléction des caractéristiques
- Création d'un lancé aléatoire des valeurs pour les caratéristique du personnage
- Calcul des modificateurs
- Création de l'exportation en fichier pdf interactif

**Amin:**
- Adaptation du script pour un interface graphique
- Création de l'interface graphique
- Explication de Git Hub à Ruben et Camille

**Tâche commune à tous:**
- Tests des fonctions
- Gestions des branches du repo GitHub

---
## 📜 Regles
**Voici certaines règles de D&D pour mieux comprendre le code. Elles ne sont pas respectées à 100%, sinon ce serait beaucoup trop complexe. Les règles peuvent être trouvées en ligne sur aide-dd par exemple.**
 - **Les classes :** correspond au "métier" du personnage. Chaque classe a des spécificités selon ce qu'elle maîtrise (est capable d'utiliser). Les points de vie dépendent par exemple de la classe.
 - **Les races :** correspond à l'appartenance raciale du personnage. Chaque race possède des spécificités et influent sur les statistiques.
 - Les armes : les armes proposées par classe sont des armes qui peuvent être maniées par les personnages de la classe en question. Chaque arme possède un type de dé de dégât (1d6, 1d8, 1d4...) qui permet de randomiser le nombre de dégâts que l'adversaire recevra après l'attaque. Certaines armes attaquent avec la force et d'autre la dextérité.
 - **Les historiques :** correspond à l'origine du personnage, de quel milieu il provient, ce qu'il faisait avant de partir à l'aventure... Cela donne un apperçu général du personnage et certaines maîtrises et compétences supplémentaires. Dans notre code, l'historique est purement décoratif, il n'a aucun impact réel sur le personnage.
 - **Les statistiques et les modificateurs :** les statistiques représentent les capacités générales innées du personnage sur divers point de vue. Elles définissent les valeurs des modificateurs. Les modificateurs sont eux, directement utilisés dans divers calculs définissant la réussite d'une compétence, d'une attaque ou encore la capacité d'esquive et la puissance de frappe.
 - **Le bonus de maîtrise :** bonus qui augmente selon le niveau. Il est ajouté pour toutes les compétences et attaques maîtrisées.
 - **Les compétences :** servent à effectuer divers actions dans le jeu de base. On utilise un d20, ajoute le modificateur lié à la compétence et le bonus de maîtrise si le personnage la maîtrise.
 - **La classe d'armure (CA) :** La CA définit la protection générale d'un individu en prenant en compte l'armure équipée, le bouclier et la capacité innée d'esquive (qui peut être limitée ou supprimée selon l'armure portée).
 - **Le jet de touche d'une attaque :** On lance 1d20 et y ajoute le modificateur lié à l'arme (For ou dex) ainsi que le bonus de maîtrise si l'arme est maîtrisée. On compare le résultat avec la CA de l'adversaire. L'attaque réussit lorsque le résultat est supérieur ou égal à la CA, sinon l'attaque échoue.
 - **Le jet de dégât :** On lance le dé de dégât de l'arme et y ajoute le modificateur correspondant.

## 📝 Sources :

  - https://www.youtube.com/watch?v=wxnXNcU-YBQ&list=PLjrnnc4BZaRCR5eOXSTAgKJpBl62Y7o45 - Pour apprendre Tkinter
  - Chat gpt - Pour le ReadME
  - W3schools
  - Copilot
  - Divers livres de règles sur D&D
