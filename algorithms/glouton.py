from geometry import Point, orientation, distance_carre
from typing import List

def trouver_enveloppe_glouton(points: List[Point]) -> List[Point]:
    """
    Calcule l'enveloppe convexe d'un nuage de points
    en utilisant l'algorithme de la Marche de Jarvis (Glouton).
    """
    
    n = len(points)
    if n < 3:
        # On ne peut pas former un polygone avec moins de 3 points.
        return [] 

    # La liste des points de l'enveloppe que l'on va construire
    enveloppe = []

    # 1. TROUVER LE POINT DE DÉPART - Point le plus à gauche (O(1))
    point_depart = min(points, key=lambda p: (p.x, p.y))
    
    point_actuel = point_depart
    
    # On boucle tant qu'on n'est pas revenu au point de départ
    while True:
        
        # Ajouter le point actuel à notre enveloppe
        enveloppe.append(point_actuel)
        
        # 2. CHERCHER LE MEILLEUR CANDIDAT SUIVANT
        # On doit trouver le point 'candidat_suivant' qui forme l'angle le plus "à gauche" (anti-horaire) par rapport à 'point_actuel'.
        
        # On initialise le candidat avec n'importe quel point (sauf le point actuel)
        candidat_suivant = points[0]
        if candidat_suivant == point_actuel:
            candidat_suivant = points[1]

        # 3. TESTER TOUS LES AUTRES POINTS
        for point_teste in points:
            
            # On ne se compare pas à soi-même
            if point_teste == point_actuel:
                continue
            
            # On vérifie l'orientation du triplet :
            o = orientation(point_actuel, candidat_suivant, point_teste)
            
            if o > 0: # Virage à gauche
                # 'point_teste' est plus à gauche que 'candidat_suivant'.
                # Il devient donc notre nouveau meilleur candidat.
                candidat_suivant = point_teste
                
            elif o == 0: # Les points sont colinéaires
                # Si (point_actuel, candidat_suivant, point_teste) sont alignés,
                # on veut garder le point le plus éloigné du 'point_actuel'.
                # Cela permet de sauter les points qui sont "au milieu" d'un segment
                # de l'enveloppe.
                
                dist_c = distance_carre(point_actuel, candidat_suivant)
                dist_t = distance_carre(point_actuel, point_teste)
                
                if dist_t > dist_c:
                    candidat_suivant = point_teste

        # 4. MISE À JOUR
        # On a fini de tester tous les points. Le 'candidat_suivant' est le prochain point de l'enveloppe.

        point_actuel = candidat_suivant
        
        # 5. CONDITION D'ARRÊT
        # Si on est revenu au point de départ, on a fait le tour complet.
        if point_actuel == point_depart:
            break
            
    return enveloppe