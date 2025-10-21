from geometry import Point, orientation
from typing import List

def appliquer_scan_sklansky(polygone_ordonne: List[Point]) -> List[Point]:
    """
    Calcule l'enveloppe convexe d'un polygone simple (ou d'une liste 
    de points déjà triés par angle) en temps linéaire O(n).
    
    C'est la routine "Sklansky" utilisée dans Graham et d'autres algos.
    Elle utilise une pile pour éliminer les virages "rentrants".
    """
    
    # La pile qui contiendra l'enveloppe finale
    # On commence avec les deux premiers points du polygone
    pile = []
    
    # Cas particulier : si le polygone est vide ou a peu de points
    if len(polygone_ordonne) < 2:
        return polygone_ordonne
        
    pile.append(polygone_ordonne[0])
    pile.append(polygone_ordonne[1])
    
    # On parcourt tous les autres points à partir du troisième
    for i in range(2, len(polygone_ordonne)):
        point_teste = polygone_ordonne[i]
        
        # Tant qu'on a au moins 2 points dans la pile ET que le triplet (avant-dernier, dernier, point_teste) forme un virage à droite (orientation <= 0),
        # c'est que le dernier point est inutile.
        
        while len(pile) >= 2:
            avant_dernier = pile[-2]
            dernier = pile[-1]
            
            o = orientation(avant_dernier, dernier, point_teste)
            
            if o <= 0: # Virage à droite ou colinéaire
                # Le point 'dernier' est à l'intérieur ou sur le segment
                # On le supprime de la pile ("étape retour" )
                pile.pop()
            else:
                # C'est un virage à gauche, c'est bon
                break
        
        # On a fini de nettoyer, on peut ajouter le 'point_teste' à la pile ("étape aller" )
        pile.append(point_teste)
        
    return pile