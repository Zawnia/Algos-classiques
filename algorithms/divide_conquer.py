# Fichier: algorithms/divide_conquer.py

from geometry import Point, Polygone, orientation
from typing import List
from algorithms.glouton import trouver_enveloppe_jarvis 

def fusionner_enveloppes(env_gauche: Polygone, env_droite: Polygone) -> Polygone:
    """
    Fusionne deux enveloppes convexes (gauche et droite) en O(n) 
    en trouvant les tangentes communes (le "pont").
    """
    
    # n_g = len(env_gauche)
    # n_d = len(env_droite)
    
    # 1. Trouver les points de départ pour le "pont"
    # Point le plus à droite de l'enveloppe gauche
    idx_g_droite = max(range(len(env_gauche)), key=lambda i: env_gauche[i].x)
    # Point le plus à gauche de l'enveloppe droite
    idx_d_gauche = min(range(len(env_droite)), key=lambda i: env_droite[i].x)

    # --- 2. TROUVER LA TANGENTE SUPÉRIEURE ---
    
    # Les indices courants
    i_g_haut = idx_g_droite
    i_d_haut = idx_d_gauche
    
    termine = False
    while not termine:
        termine = True
        
        # "Marcher" sur l'enveloppe gauche (sens anti-horaire)
        while True:
            i_g_haut_suivant = (i_g_haut + 1) % len(env_gauche)
            p_g_actuel = env_gauche[i_g_haut]
            p_g_suivant = env_gauche[i_g_haut_suivant]
            p_d_actuel = env_droite[i_d_haut]
            
            # Si le point suivant forme un virage à gauche (monte), on l'adopte
            if orientation(p_d_actuel, p_g_actuel, p_g_suivant) > 0:
                i_g_haut = i_g_haut_suivant
                termine = False # On a bougé, on doit re-vérifier l'autre côté
            else:
                break # On a trouvé le point tangent sur la gauche

        # "Marcher" sur l'enveloppe droite (sens horaire)
        while True:
            i_d_haut_precedent = (i_d_haut - 1 + len(env_droite)) % len(env_droite)
            p_d_actuel = env_droite[i_d_haut]
            p_d_precedent = env_droite[i_d_haut_precedent]
            p_g_actuel = env_gauche[i_g_haut]
            
            # Si le point précédent forme un virage à droite (monte), on l'adopte
            if orientation(p_g_actuel, p_d_actuel, p_d_precedent) < 0:
                i_d_haut = i_d_haut_precedent
                termine = False # On a bougé, on doit re-vérifier l'autre côté
            else:
                break # On a trouvé le point tangent sur la droite

    # --- 3. TROUVER LA TANGENTE INFÉRIEURE ---
    
    # On repart des points de départ
    i_g_bas = idx_g_droite
    i_d_bas = idx_d_gauche
    
    termine = False
    while not termine:
        termine = True
        
        # "Marcher" sur l'enveloppe gauche (sens horaire)
        while True:
            i_g_bas_precedent = (i_g_bas - 1 + len(env_gauche)) % len(env_gauche)
            p_g_actuel = env_gauche[i_g_bas]
            p_g_precedent = env_gauche[i_g_bas_precedent]
            p_d_actuel = env_droite[i_d_bas]
            
            # Si le point précédent forme un virage à droite (descend)
            if orientation(p_d_actuel, p_g_actuel, p_g_precedent) < 0:
                i_g_bas = i_g_bas_precedent
                termine = False
            else:
                break

        # "Marcher" sur l'enveloppe droite (sens anti-horaire)
        while True:
            i_d_bas_suivant = (i_d_bas + 1) % len(env_droite)
            p_d_actuel = env_droite[i_d_bas]
            p_d_suivant = env_droite[i_d_bas_suivant]
            p_g_actuel = env_gauche[i_g_bas]
            
            # Si le point suivant forme un virage à gauche (descend)
            if orientation(p_g_actuel, p_d_actuel, p_d_suivant) > 0:
                i_d_bas = i_d_bas_suivant
                termine = False
            else:
                break
                
    # --- 4. CONSTRUIRE L'ENVELOPPE FINALE ---
    
    nouvelle_enveloppe = []
    
    # 1. Partir du point de la tangente inf. gauche
    # et aller jusqu'au point de la tangente sup. gauche (sens anti-horaire)
    i = i_g_bas
    while i != i_g_haut:
        nouvelle_enveloppe.append(env_gauche[i])
        i = (i + 1) % len(env_gauche)
    nouvelle_enveloppe.append(env_gauche[i_g_haut]) # Ajouter le point de la tangente sup.
    
    # 2. Partir du point de la tangente sup. droite
    # et aller jusqu'au point de la tangente inf. droite (sens anti-horaire)
    i = i_d_haut
    while i != i_d_bas:
        nouvelle_enveloppe.append(env_droite[i])
        i = (i + 1) % len(env_droite)
    nouvelle_enveloppe.append(env_droite[i_d_bas]) # Ajouter le point de la tangente inf.

    return nouvelle_enveloppe


def trouver_enveloppe_diviser(points_tries_par_x: List[Point]) -> Polygone:
    """
    Calcule l'enveloppe convexe en utilisant l'approche "Diviser pour Régner".
    PRE-REQUIS : La liste 'points_tries_par_x' DOIT être triée par abscisse.
    """
    
    n = len(points_tries_par_x)
    
    # 1. CAS DE BASE
    if n <= 6:
        # On utilise Jarvis, qui n'a pas besoin de points triés
        return trouver_enveloppe_jarvis(points_tries_par_x)
        
    # 2. DIVISER
    milieu = n // 2
    points_gauche = points_tries_par_x[:milieu]
    points_droite = points_tries_par_x[milieu:]
    
    # 3. RÉGNER (Appels récursifs)
    enveloppe_gauche = trouver_enveloppe_diviser(points_gauche)
    enveloppe_droite = trouver_enveloppe_diviser(points_droite)
    
    # 4. FUSIONNER
    return fusionner_enveloppes(enveloppe_gauche, enveloppe_droite)