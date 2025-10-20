#Classes pour généraliser l'implémentation 

from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


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





