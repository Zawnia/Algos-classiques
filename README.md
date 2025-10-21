# Algorithmes classiques — Étude et comparaisons

Projet étudiant visant à **implémenter**, **tester** et **comparer** des algorithmes classiques en Python sur des problèmes ciblés.

## Statut du projet
- ✅ **Terminé** : Enveloppe convexe (plusieurs variantes)
- 🔜 **À venir** : Problème de la médiane (et comparaison avec d'autres approches)
- 🔜 **À venir** : Troisième problème à définir

## Objectifs
- Mesurer empiriquement le temps d'exécution et la complexité observée
- Visualiser les résultats pour valider les implémentations
- Documenter les compromis entre les différentes variantes d'un même problème

## Algorithmes implémentés

### 1) Enveloppe convexe
- **Graham Scan** : tri par angle polaire suivi d'une construction, complexité attendue **O(n log n)**
- **Gift Wrapping / Jarvis March** : parcours « glouton » depuis un point extrême, complexité **O(n·h)** où *h* est le nombre de points sur l'enveloppe
- **Sklansky (polygone simple)** : vérification du sens de rotation, complexité **O(n)**
- **Diviser pour régner** : calcul de deux enveloppes convexes puis fusion, récurrence **T(n) = 2T(n/2) + O(n) ⇒ O(n log n)**
- Variantes utilisant « 4 cadrans » et sélections par coordonnées/angles pour optimiser les performances en pratique

### 2) Sélection de la médiane
- Implémentation prévue de l'algorithme de **sélection en temps linéaire** (médiane des médianes)
- Comparaison avec l'approche par tri suivi d'un accès par index
- Notes internes sur l'idée de « pente médiane » pour le filtrage itératif

### 3) Algorithme à définir
- Candidats suggérés : **paire de points la plus proche**, **tri topologique**, ou **plus court chemin** pour diversifier les domaines étudiés

## Génération de données
- Un script de génération synthétique de données est disponible pour les tests

## Installation rapide

```bash
# 1) Création et activation de l'environnement virtuel
python -m venv .venv

# Sous Windows
.\.venv\Scripts\activate

# Sous macOS/Linux
source .venv/bin/activate

# 2) Installation des dépendances
pip install -r requirements.txt
```

## Structure du projet

```
Algos-classiques/
├── algorithms/          # Implémentations des algorithmes
│   ├── graham_scan.py   # Algorithme de Graham
│   ├── glouton.py       # Approche gloutonne (Jarvis)
│   ├── sklansky.py      # Algorithme de Sklansky
│   └── divide_conquer.py # Diviser pour régner
├── geometry.py          # Primitives géométriques
├── visualisation.py     # Outils de visualisation
├── cas_de_test.py       # Cas de test
└── main.py              # Point d'entrée principal
```

## Utilisation

```bash
# Exécuter le programme principal
python main.py
```

## Auteurs
Projet réalisé dans le cadre d'études en informatique.
