# Fichier: visualisation.py

import matplotlib.pyplot as plt
from typing import List
from geometry import Point

def afficher_enveloppe(points: List[Point], enveloppe: List[Point], titre: str):
    """
    Affiche un nuage de points et son enveloppe convexe de manière claire.
    
    - points: Tous les points du nuage (en bleu).
    - enveloppe: Les points de l'enveloppe (en rouge).
    - titre: Le titre du graphique.
    """
    
    # 1. Extraire les coordonnées de tous les points
    x_points = [p.x for p in points]
    y_points = [p.y for p in points]
    
    # 2. Extraire les coordonnées des points de l'enveloppe
    # On ajoute le premier point à la fin pour "fermer" le polygone
    enveloppe_fermee = enveloppe + [enveloppe[0]]
    x_env = [p.x for p in enveloppe_fermee]
    y_env = [p.y for p in enveloppe_fermee]
    
    # --- Création du graphique ---
    plt.figure(figsize=(10, 8)) # Une fenêtre de taille confortable
    
    # 3. Afficher tous les points
    plt.scatter(x_points, y_points, c='blue', alpha=0.6, label='Tous les points')
    
    # 4. Afficher l'enveloppe (la ligne)
    # 'r-o' signifie : 'r' (rouge) - (ligne continue) 'o' (points marqués)
    plt.plot(x_env, y_env, 'r-o', linewidth=2, label='Enveloppe Convexe')
    
    # 5. Mettre en valeur le point de départ (facultatif mais propre)
    if enveloppe:
        plt.scatter(
            enveloppe[0].x, enveloppe[0].y, 
            c='green', s=100, zorder=10, label='Point de départ'
        )
    
    # --- Configuration pour la lisibilité ---
    plt.title(titre, fontsize=16)
    plt.xlabel("Axe X")
    plt.ylabel("Axe Y")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # 6. ESSENTIEL : Rendre les axes égaux !
    # Sans cela, un carré ressemblera à un rectangle et les angles seront faux.
    plt.axis('equal')
    
    plt.show()