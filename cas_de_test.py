import numpy as np
from typing import List
from geometry import Point

def generer_points_aleatoires(n: int, x_max: int = 100, y_max: int = 100) -> List[Point]:
    """
    Génère n points aléatoires dans un rectangle [0, x_max] x [0, y_max].
    """
    # Génère n paires (x, y)
    coords_x = np.random.rand(n) * x_max
    coords_y = np.random.rand(n) * y_max
    
    # Convertit les paires de coordonnées en objets Point
    return [Point(x, y) for x, y in zip(coords_x, coords_y)]

def generer_points_cercle(n: int, centre_x: int = 50, centre_y: int = 50, rayon: int = 40) -> List[Point]:
    """
    Génère n points distribués sur un cercle.
    C'est le PIRE CAS pour Jarvis (O(n*h) -> O(n^2) car h=n).
    """
    # Génère n angles entre 0 et 2*pi
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    
    # Calcule les positions x, y sur le cercle
    # On ajoute un petit "bruit" aléatoire pour éviter une colinéarité parfaite
    bruit = 0.9 + 0.2 * np.random.rand(n)
    coords_x = centre_x + (rayon * bruit) * np.cos(angles)
    coords_y = centre_y + (rayon * bruit) * np.sin(angles)
    
    return [Point(x, y) for x, y in zip(coords_x, coords_y)]

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