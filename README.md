# Jolis algorithmes classiques — étude et comparaisons

Projet étudiant visant à **implémenter**, **tester** et **comparer** des algorithmes classiques en Python sur des problèmes ciblés.

## Statut
- (Done) Enveloppe convexe (plusieurs variantes)
- (Soon) Problème de la médiane (et comparaison avec d’autres approches)
- (Soon) Troisième problème à définir

## Objectifs
- Mesurer empiriquement temps d’exécution et complexité observée.
- Visualiser les sorties pour valider les implémentations.
- Documenter les compromis entre variantes d’un même problème.

## Algorithmes prévus

### 1) Enveloppe convexe
- **Graham scan** : tri par angle + construction, complexité attendue **O(n log n)**. :contentReference[oaicite:0]{index=0}
- **Gift wrapping / Jarvis** : parcours « glouton » depuis un point extrême, **O(n·h)** avec *h* points sur l’enveloppe. :contentReference[oaicite:1]{index=1}
- **Sklansky (polygone simple)** : vérification du sens de rotation, **O(n)**. :contentReference[oaicite:2]{index=2}
- **Divide & Conquer** : deux enveloppes + jointure, récurrence **T(n)=2T(n/2)+O(n) ⇒ O(n log n)**. :contentReference[oaicite:3]{index=3}
- Variantes « 4 cadrans » et sélections par coordonnées/angles discutées pour optimiser la pratique. :contentReference[oaicite:4]{index=4}

### 2) Sélection de la médiane
- Implémentation prévue du **sélection en temps linéaire** (médiane des médianes) et comparaison avec tri + accès index. Notes internes sur l’idée de « pente médiane » pour filtrage itératif. :contentReference[oaicite:5]{index=5}

### 3) À définir
- Candidat suggéré : **plus proche paire de points**, **tri topologique**, ou **plus court chemin** pour varier les domaines.

## Données
- Génération synthétique disponible via un script (voir ci-dessous).

## Installation rapide

```bash
# 1) Création et activation du venv
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 2) Dépendances
pip install -r requirements.txt
