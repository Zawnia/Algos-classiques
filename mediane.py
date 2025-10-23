from majoritaire import maj_dico

def _find_kth_naive(k, T):
    """
    Trouve le k-ième plus petit élément en O(n^2).
    """

    # On itère sur chaque élément pour le tester comme candidat
    for x in T:
        # Pour chaque x, on compte combien sont <, ==, >
        lt_count = 0  # Compte les < x
        eq_count = 0  # Compte les == x

        # C'est cette boucle imbriquée qui crée le O(n^2)
        for y in T:
            if y < x:
                lt_count += 1
            elif y == x:
                eq_count += 1

        if lt_count <= k < (lt_count + eq_count):
            return x

    return None


def mediane_naif(T):
    """
    Calcule la médiane en O(n^2), deux boucles imbriquées.
    """
    n = len(T)

    if n == 0:
        raise ValueError("La liste vide n'a pas de médiane.")

    # Cas impair : on cherche l'élément du milieu
    if n % 2 == 1:
        k = n // 2
        return _find_kth_naive(k, T)

    # Cas pair : on cherche les 2 éléments centraux et on fait la moyenne
    else:
        k1 = n // 2 - 1
        k2 = n // 2

        # On doit appeler l'algo O(n^2) deux fois
        val1 = _find_kth_naive(k1, T)
        val2 = _find_kth_naive(k2, T)

        return (val1 + val2) / 2.0

def mediane_par_tri(t : list): #O(nlogn)
    t = sorted(t) #O(nlogn)
    n = len(t)

    if not t :
        raise ValueError("La médiane d'une liste vide n'est pas défine")

    if n% 2 == 0 : #tableau pair
        return (t[n//2] + t[(n//2)-1])/2
    else :
        return t[n//2]

def quicksort(T):
    """
    Trie la liste T en place et la retourne.
    Optimisations : médiane-de-trois, partition de Hoare, insertion sort pour petits segments, pile explicite.
    """
    n = len(T)
    if n < 2:
        return T

    INSERTION_CUTOFF = 24

    def insertion_sort(a, lo, hi):
        for i in range(lo + 1, hi + 1):
            x = a[i]
            j = i - 1
            while j >= lo and a[j] > x:
                a[j + 1] = a[j]
                j -= 1
            a[j + 1] = x

    def median3(a, i, j, k):
        # renvoie l'indice de la médiane de a[i], a[j], a[k]
        x, y, z = a[i], a[j], a[k]
        if x < y:
            if y < z:   return j
            if x < z:   return k
            return i
        else:
            if x < z:   return i
            if y < z:   return k
            return j

    def hoare_partition(a, lo, hi):
        m = (lo + hi) // 2
        p = median3(a, lo, m, hi)
        pivot = a[p]

        i = lo - 1
        j = hi + 1
        while True:
            i += 1
            while a[i] < pivot:
                i += 1
            j -= 1
            while a[j] > pivot:
                j -= 1
            if i >= j:
                return j
            a[i], a[j] = a[j], a[i]

    # tri explicite à l'aide d'une pile pour éviter la récursion profonde
    stack = [(0, n - 1)]
    while stack:
        lo, hi = stack.pop()

        while hi - lo + 1 > INSERTION_CUTOFF:
            p = hoare_partition(T, lo, hi)
            # traiter d'abord le plus petit segment pour limiter la pile
            if p - lo < hi - (p + 1):
                stack.append((p + 1, hi))
                hi = p
            else:
                stack.append((lo, p))
                lo = p + 1

        # petits segments : insertion sort
        insertion_sort(T, lo, hi)

    return T

def rang_k_tri(k, t):
    t = quicksort(t)

    if not t :
        raise ValueError("La médiane d'une liste vide n'est pas défine")

    return t[k]


#--- Médianes des médianes ---

#Tri par insertion, rapide pour les petites listes, utilisé dans l'algo suivant
def tri_insertion(arr):
    """
    Trie une liste en place en utilisant le tri par insertion.
    """

    for i in range(1, len(arr)):
        key = arr[i]

        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key


def _find_kth_bfprt(k : int, t : list):
    n = len(t)

    #cas de sortie
    if len(t) < 10:
        t = sorted(t)
        return t[k]

    # on divise la liste en blocs de 5 (O(n)) on les trie (O(n))
    liste_des_medianes = []
    for i in range(0, n, 5):
        chunk = t[i:i+5] #récupère par bloc de 5

        tri_insertion(chunk) #on trie
        liste_des_medianes.append(chunk[(len(chunk) - 1) // 2]) #pour gérer le cas du dernier paquet pas complet

    #On recurre
    k_pivot = len(liste_des_medianes) // 2 #on prend la médiane comme pivot
    alpha = _find_kth_bfprt(k_pivot, liste_des_medianes) #appel récursif pour trouver alpha

    def partitionner(t : list, alpha):
        p, egal, g = [], [], []
        for i in t:
            if i < alpha :
                p.append(i)
            elif i > alpha :
                g.append(i)
            else :
                egal.append(i)

        return p,egal,g

    P, E, G = partitionner(t, alpha)

    #Récursion sur p ou g
    if k < len(P):
        return _find_kth_bfprt(k, P)

    elif k < len(P) + len(E):
        return alpha

    else:
        return _find_kth_bfprt(k - len(P) - len(E), G)


def mediane_des_medianes(t_input):
    """
    on applique _find_kth_bfprt au cas de la médiane
    """
    n = len(t_input)

    # 1. Gérer le cas de la liste vide (pour la batterie de test)
    if n == 0:
        raise ValueError("La liste vide n'a pas de médiane.")

    # 2. Cas impair : simple, on trouve l'élément du milieu
    if n % 2 == 1:
        k = n // 2
        # On fait une copie pour garantir que la liste originale n'est pas mutée
        return _find_kth_bfprt(k, list(t_input))

        # 3. Cas pair : il faut trouver deux éléments et faire la moyenne
    else:
        k1 = n // 2 - 1
        k2 = n // 2

        # On doit appeler l'algo DEUX fois (sur des copies), c'est chiant
        val1 = _find_kth_bfprt(k1, list(t_input))
        val2 = _find_kth_bfprt(k2, list(t_input))

        # Retourne la moyenne
        return (val1 + val2) / 2.0

def mediane_quicksort(t : list):
    n = len(t)

    if not t :
        raise ValueError("La médiane d'une liste vide n'est pas défine")

    if n% 2 == 0 : #tableau pair
        return (t[n//2] + t[(n//2)-1])/2
    else :
        return t[n//2]
    pass


import random  # Nécessaire pour un meilleur pivot


def elt_rg(k, t): #
    """
    Trouve l'élément de rang k (indexé à 0) dans la liste t. Fonctionne comme le quicksort, c'est un divide and coquer
    """
    if not t:
        # Cas de base : liste vide
        return None  # Ou lever une erreur

    # Choisir un pivot aléatoire évite le pire cas O(n^2) si la liste est déjà triée.
    alpha = random.choice(t)

    # Partition en 3 groupes (Petits, Égaux, Grands)
    P, E, G = [], [], []
    for x in t:
        if x < alpha:
            P.append(x)
        elif x == alpha:
            E.append(x)
        else:
            G.append(x)

    n_p = len(P)
    n_e = len(E)


    if k < n_p:
        # Le k-ième élément est dans le groupe P. On cherche le même k dans cette sous-liste.
        return elt_rg(k, P)

    elif k < n_p + n_e:
        # Le k-ième élément est dans le groupe E. C'est le pivot lui-même.
        return alpha

    else:
        # Le k-ième élément est dans le groupe G. On ajuste k en soustrayant tous les éléments de P et E.
        return elt_rg(k - n_p - n_e, G)


if __name__ == "__main__":

    # Définition tes cas de tests
    # (entrée, sortie_attendue)
    test_cases = [
        ([3, 1, 5, 2, 4], 3),  # Impair simple
        ([5, 1, 4, 2], 3.0),  # Pair simple (moyenne de 2 et 4)
        ([4, 1, 3, 3, 5], 3),  # Impair avec doublons
        ([1, 5, 2, 5], 3.5),  # Pair avec doublons (moyenne de 2 et 5)
        ([10, 20, 30], 20),  # Déjà trié
        ([30, 20, 10], 20),  # Trié inverse
        ([42], 42),  # Un seul élément
        ([5, 1], 3.0),  # Deux éléments
    ]

    list_of_algos = [mediane_naif, mediane_des_medianes]

    print("Démarrage des tests de correction...")

    for algo in list_of_algos:
        algo_name = algo.__name__
        print(f"\n--- Test de : {algo_name} ---")

        # 1. Tests sur les listes non vides
        for input_list, expected in test_cases:
            # Copie pour éviter la mutation (important pour 'mediane_par_tri')
            list_copy = list(input_list)
            try:
                result = algo(list_copy)
                assert result == expected, f"Liste {input_list}: Attendu {expected}, Obtenu {result}"
                print(f"  PASS: {input_list}")
            except AssertionError as e:
                print(f"  FAIL: {e}")
            except Exception as e:
                print(f"  ERROR: {input_list} a levé une exception inattendue: {e}")

        # 2. Test spécifique de la liste vide
        try:
            algo([])
            print("  FAIL: La liste vide [] n'a pas levé d'erreur.")
        except ValueError:
            # C'est le comportement attendu
            print("  PASS: La liste vide [] a levé ValueError (attendu).")
        except Exception as e:
            # Une autre exception a été levée
            print(f"  FAIL: La liste vide [] a levé {type(e).__name__} au lieu de ValueError.")

    print("\n--- Tests terminés ---")



















