from geometry import Point, orientation, distance_carre
from typing import List
from functools import cmp_to_key

# On importe la fonction Sklansky réutilisable
from algorithms.sklansky import appliquer_scan_sklansky

def trouver_enveloppe_sklanski(points: List[Point]) -> List[Point]:
    """
    Calcule l'enveloppe convexe en utilisant le Parcours de Graham.
    Étape 1 : Tri par angle (O(n log n)) 
    Étape 2 : Scan "Sklansky" (O(n))
    """
    
    n = len(points)
    if n < 3:
        return []

    # === ÉTAPE 1 : TROUVER LE POINT DE DÉPART ET TRIER (O(n log n)) ===
    
    # 1. Trouver le point de départ : le plus bas, puis le plus à gauche
    point_depart = min(points, key=lambda p: (p.y, p.x))
    
    # 2. Fonction de comparaison pour le tri par angle
    def comparer_angles(p1: Point, p2: Point) -> int:
        o = orientation(point_depart, p1, p2)
        if o == 0:
            return -1 if distance_carre(point_depart, p1) < distance_carre(point_depart, p2) else 1
        return -1 if o > 0 else 1 # -1 si p1 est avant p2 (gauche)

    # 3. Trier les points (sans le point de départ) 
    points_sans_depart = [p for p in points if p != point_depart]
    points_tries = sorted(points_sans_depart, key=cmp_to_key(comparer_angles))
    
    # 4. Préparer la liste complète pour Sklansky
    # C'est le "polygone"  que Sklansky va nettoyer
    points_pour_scan = [point_depart] + points_tries

    # === ÉTAPE 2 : APPLIQUER LE SCAN SKLANSKY (O(n)) ===
    
    # On appelle simplement notre fonction réutilisable !
    enveloppe = appliquer_scan_sklansky(points_pour_scan)
    
    return enveloppe