from typing import List, Tuple

from geometry import Point, Polygone, orientation
from .glouton import trouver_enveloppe_jarvis


# =============================================================================
# 1) Fonction publique
# =============================================================================
def trouver_enveloppe_diviser(points: List[Point]) -> Polygone:
    """
    Approche « diviser pour régner » pour l'enveloppe convexe.

    L'entrée peut être dans n'importe quel ordre : on commence donc par trier
    les points par abscisse puis on lance la récursion qui fusionne
    progressivement les enveloppes intermédiaires.
    """
    if not points:
        return []

    points_tries = sorted(points, key=lambda p: (p.x, p.y))
    return _diviser(points_tries)


# =============================================================================
# 2) Récursion principale
# =============================================================================
def _diviser(points_tries: List[Point]) -> Polygone:
    """Divise les points en deux moitiés, calcule leurs enveloppes, puis fusionne."""

    n = len(points_tries)

    # Cas de base : trop peu de points pour qu'une fusion compliquée se justifie.
    if n <= 5:
        return _enveloppe_petite_instance(points_tries)

    milieu = n // 2
    enveloppe_gauche = _diviser(points_tries[:milieu])
    enveloppe_droite = _diviser(points_tries[milieu:])

    return _fusionner_enveloppes(enveloppe_gauche, enveloppe_droite)


# =============================================================================
# 3) Enveloppe directe sur les petites instances
# =============================================================================
def _enveloppe_petite_instance(points: List[Point]) -> Polygone:
    """
    Pour <= 5 points on utilise Jarvis (très lisible). En cas de retour vide
    (moins de trois points distincts, par exemple), on renvoie simplement les
    points triés et sans doublons.
    """
    uniques = _points_uniques_ordonnees(points)

    if len(uniques) <= 2:
        return uniques

    hull = trouver_enveloppe_jarvis(uniques)
    return hull if hull else uniques


# =============================================================================
# 4) Fusion des enveloppes partielles
# =============================================================================
def _fusionner_enveloppes(env_gauche: Polygone, env_droite: Polygone) -> Polygone:
    """
    Fusionne deux enveloppes convexes (ordre anti-horaire) en recherchant
    les tangentes haute et basse qui servent de « ponts » entre elles.
    """
    if not env_gauche:
        return env_droite
    if not env_droite:
        return env_gauche

    # Si l'une des deux enveloppes est minuscule, on repasse par une
    # construction directe (monotone chain) pour garder un code limpide.
    if len(env_gauche) <= 2 or len(env_droite) <= 2:
        return _monotone_chain(env_gauche + env_droite)

    idx_gauche = max(range(len(env_gauche)), key=lambda k: env_gauche[k].x)
    idx_droite = min(range(len(env_droite)), key=lambda k: env_droite[k].x)

    i_haut, j_haut = _tangente_superieure(env_gauche, env_droite, idx_gauche, idx_droite)
    i_bas, j_bas = _tangente_inferieure(env_gauche, env_droite, idx_gauche, idx_droite)

    enveloppe: List[Point] = []

    # Parcours de la partie gauche (de la tangente haute vers la tangente basse).
    k = i_haut
    enveloppe.append(env_gauche[k])
    while k != i_bas:
        k = _suivant(k, len(env_gauche))
        enveloppe.append(env_gauche[k])

    # Parcours de la partie droite (de la tangente basse vers la tangente haute).
    k = j_bas
    enveloppe.append(env_droite[k])
    while k != j_haut:
        k = _suivant(k, len(env_droite))
        enveloppe.append(env_droite[k])

    return enveloppe


# =============================================================================
# 5) Recherche des tangentes
# =============================================================================
def _tangente_superieure(env_gauche: Polygone, env_droite: Polygone,
                         i: int, j: int) -> Tuple[int, int]:
    """
    Fait tourner i (gauche) dans le sens anti-horaire et j (droite) dans le sens
    horaire jusqu'à obtenir la tangente supérieure.
    """
    len_g = len(env_gauche)
    len_d = len(env_droite)

    while True:
        a_bouge = False

        while orientation(env_droite[j], env_gauche[i], env_gauche[_suivant(i, len_g)]) >= 0:
            i = _suivant(i, len_g)
            a_bouge = True

        while orientation(env_gauche[i], env_droite[j], env_droite[_precedent(j, len_d)]) <= 0:
            j = _precedent(j, len_d)
            a_bouge = True

        if not a_bouge:
            break

    return i, j


def _tangente_inferieure(env_gauche: Polygone, env_droite: Polygone,
                         i: int, j: int) -> Tuple[int, int]:
    """
    Fait tourner i (gauche) dans le sens horaire et j (droite) dans le sens
    anti-horaire jusqu'à obtenir la tangente inférieure.
    """
    len_g = len(env_gauche)
    len_d = len(env_droite)

    while True:
        a_bouge = False

        while orientation(env_droite[j], env_gauche[i], env_gauche[_precedent(i, len_g)]) <= 0:
            i = _precedent(i, len_g)
            a_bouge = True

        while orientation(env_gauche[i], env_droite[j], env_droite[_suivant(j, len_d)]) >= 0:
            j = _suivant(j, len_d)
            a_bouge = True

        if not a_bouge:
            break

    return i, j


# =============================================================================
# 6) Utilitaires
# =============================================================================
def _suivant(index: int, taille: int) -> int:
    return (index + 1) % taille


def _precedent(index: int, taille: int) -> int:
    return (index - 1 + taille) % taille


def _points_uniques_ordonnees(points: List[Point]) -> List[Point]:
    """Trie les points et supprime les doublons tout en conservant l'ordre."""
    vus = set()
    uniques = []
    for p in sorted(points, key=lambda pt: (pt.x, pt.y)):
        if p not in vus:
            uniques.append(p)
            vus.add(p)
    return uniques


def _monotone_chain(points: List[Point]) -> Polygone:
    """
    Mise en œuvre compacte de l'algorithme « monotone chain ».
    Sert de filet de sécurité pour les petits cas et garantit un résultat
    toujours trié dans l'ordre anti-horaire.
    """
    uniques = _points_uniques_ordonnees(points)

    if len(uniques) <= 2:
        return uniques

    # Construction de la chaîne inférieure.
    inferieure: List[Point] = []
    for p in uniques:
        while len(inferieure) >= 2 and orientation(inferieure[-2], inferieure[-1], p) <= 0:
            inferieure.pop()
        inferieure.append(p)

    # Construction de la chaîne supérieure.
    superieure: List[Point] = []
    for p in reversed(uniques):
        while len(superieure) >= 2 and orientation(superieure[-2], superieure[-1], p) <= 0:
            superieure.pop()
        superieure.append(p)

    # On retire le dernier point de chaque chaîne (il correspond au premier de l'autre chaîne).
    return inferieure[:-1] + superieure[:-1]
