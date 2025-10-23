from typing import List
from geometry import Point, Polygone, orientation
from .glouton import trouver_enveloppe_glouton
from .sklansky import appliquer_scan_sklansky


# =============================================================================
# 1) Fonction publique
# =============================================================================
def trouver_enveloppe_diviser(points: list[Point]) -> Polygone:
    """
    Approche « diviser pour régner » pour l'enveloppe convexe.
    mais comme c'était dur de faire du récursif a l'infini on ne coupe que en deux
    1) on trie les points par coordonnée x croissante
    2) on divise en deux moitiés haut et bas
    3) on construit l'enveloppe convexe de chaque moitié avec lsklanski
    """
    if not points:
        return []

    P_tries = tri_par_coord(points)
    print(P_tries)
    enveloppe = appliquer_scan_sklansky(P_tries)

    return enveloppe
    

def tri_par_coord(points):

    n=len(points)
    ptExtrm=0

    #on cherhche le point le plus à gauche
    for i in range(n):
        if points[i].x < points[ptExtrm].x:
            ptExtrm=i 

    extreme = points[ptExtrm]

    Haut,Bas=[],[]

    for i in range(n):
        if points[i].y <= extreme.y:
            Bas.append(points[i])
        else: 
            Haut.append(points[i])

    #on trie les listes par ordonnées croissantes 
    Poly = sorted(Bas, key=lambda p: p.x)
    Haut = sorted(Haut, key=lambda p: p.x)

    #on complète le polygone avec sa partie haute 
    for p in reversed(Haut):
        Poly.append(p)
    
    return Poly