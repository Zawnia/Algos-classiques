#Classes pour généraliser l'implémentation 
from typing import List
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
    def __eq__(self, other) -> bool:
        """Permet de comparer deux points (utile pour les tests)."""
        if not isinstance(other, Point):
            return False
        # Utiliser une tolérance pour les flottants si nécessaire
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        """Permet d'utiliser les points dans un set() ou un dict()."""
        return hash((self.x, self.y))

Polygone = List[Point]

#Outils géométriques

def orientation(p: Point, q: Point, r: Point) -> float:
    """
    Calcule l'orientation de (p, q, r).
    > 0 : Virage à gauche
    < 0 : Virage à droite
    = 0 : Colinéaire
    """
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    return val

def distance_carre(p: Point, q: Point) -> float:
    """
    Calcule le carré de la distance euclidienne entre 2 points p et q.
    """
    return (q.x - p.x)**2 + (q.y - p.y)**2





