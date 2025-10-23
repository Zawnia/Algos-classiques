from geometry import Point, orientation, distance_carre
from typing import List

def trouver_enveloppe_glouton(points: List[Point]) -> List[Point]:
   
    n = len(points)
    if n < 3:
        return [] # On ne peut pas former un polygone avec moins de 3 points.

    enveloppe = []

    point_depart = min(points, key=lambda p: (p.x, p.y)) #point de départ - Point le plus à gauche (O(1))
    point_actuel = point_depart

    # On boucle tant qu'on n'est pas revenu au point de départ
    while True:
        
        enveloppe.append(point_actuel)

        candidat_suivant = points[0]
        if candidat_suivant == point_actuel:
            candidat_suivant = points[1]

        for point_teste in points:
            
            if point_teste == point_actuel:
                continue
            
            o = orientation(point_actuel, candidat_suivant, point_teste)
        
            if o > 0: # Virage à gauche
                candidat_suivant = point_teste
                
            elif o == 0: # Les points sont colinéaires
                # Si (point_actuel, candidat_suivant, point_teste) sont alignés, 
                # on veut garder le point le plus éloigné du 'point_actuel'.

                dist_c = distance_carre(point_actuel, candidat_suivant)
                dist_t = distance_carre(point_actuel, point_teste)

                if dist_t > dist_c:
                    candidat_suivant = point_teste

        point_actuel = candidat_suivant
        
        #Si on est revenu au point de départ, on a fait le tour complet.
        if point_actuel == point_depart:
            break
            
    return enveloppe