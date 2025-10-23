import numpy as np
from typing import List
from geometry import Point
import random
import math

def generer_points_aleatoires(n: int, x_max: int = 100, y_max: int = 100) -> List[Point]:
    """
    Génère n points aléatoires dans un rectangle [0, x_max] x [0, y_max].
    """
    # Génère n paires (x, y)
    coords_x = np.random.rand(n) * x_max
    coords_y = np.random.rand(n) * y_max
    
    # Convertit les paires de coordonnées en objets Point
    return [Point(x, y) for x, y in zip(coords_x, coords_y)]

def generer_points_cercle(N, rayon=10):
    """
    Génère N points sur un cercle parfait en utilisant la trigonométrie.
    """
    points = []
    for i in range(N):
        # Calcule l'angle pour ce point
        angle = (i / N) * 2 * math.pi

        # Calcule les coordonnées x, y
        # On ajoute une minuscule gigue (jitter) pour éviter une colinéarité verticale/horizontale parfaite peut perturber certains algos de tri.
        #gigue = random.uniform(-1e-9, 1e-9)
        gigue = 0.0

        x = rayon * math.cos(angle) + gigue
        y = rayon * math.sin(angle) + gigue

        points.append(Point(x, y))

    return points

def generer_points_carre(n_par_cote: int, taille: int = 100) -> List[Point]:
    """
    Génère 4*(n-1) points formant un carré (juste les bords).
    """
    points = []
    # Côtés horizontal
    for i in range(n_par_cote):
        points.append(Point(i * taille / (n_par_cote-1), 0))
        points.append(Point(i * taille / (n_par_cote-1), taille))
    # Côtés vertical
    for i in range(1, n_par_cote - 1): # Sans les coins déjà faits
        points.append(Point(0, i * taille / (n_par_cote-1)))
        points.append(Point(taille, i * taille / (n_par_cote-1)))
        
    return points

def generer_points_colineaires(n: int, y_val: int = 50) -> List[Point]:
    """
    Génère n points sur une ligne horizontale.
    Pire cas (constant) pour Graham Scan.
    """
    coords_x = np.linspace(0, 100, n)
    return [Point(x, y_val) for x in coords_x]