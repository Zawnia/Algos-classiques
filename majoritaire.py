#Outil
def nb_occurence(x, t : list):
    """Renvoie le nombre d'occurences de x dans T en O(n)"""
    compteur = 0
    for element in t:
        if element == x:
            compteur += 1
    return compteur


#Algo naif : on compte le nb d'occurence de chaque elt
def maj_naif(t : list):
    """Renvoie la médiane de la liste t"""
    for x in t:
        if nb_occurence(x,t) > len(t) / 2 :
            return x
    return None


# Algo dico
def maj_dico(t : list):
    dico = {}
    for x in t:
        if x in dico :
            dico[x] += 1
        else :
            dico[x] = 1

    cle_max = max(dico, key=dico.get)
    val_max = dico[cle_max]

    if val_max > len(t)/2 :
        return cle_max
    else :
        return None

if __name__ == "__main__":

    # On suppose que ces fonctions existent
    algos_a_tester = [
        maj_naif,
        maj_dico
    ]

    # --- Cas de tests (entrée, sortie_attendue) ---
    # Seuil = floor(n / 2). La majorité doit apparaître > seuil.
    test_cases = [
        # 1. Cas standards (majorité existe)
        ([1, 2, 1, 1, 3], 1),  # Impair n=5, seuil=2. '1' (3 fois)
        ([1, 2, 1, 1], 1),  # Pair n=4, seuil=2. '1' (3 fois)
        ([5, 5, 5], 5),  # Tous identiques
        (['a', 'b', 'a'], 'a'),  # Non-numérique n=3, seuil=1. 'a' (2 fois)
        ([1, 2, 1, 2, 1], 1),  # Majorité juste (3 sur 5)

        # 2. Cas où la majorité n'existe pas
        ([1, 2, 3, 4, 5], None),  # Impair, aucun
        ([1, 2, 3, 1], None),  # Pawir n=4, seuil=2. '1' (2 fois) n'est PAS > 2
        ([1, 2, 2, 3, 3, 1], None),  # Pair n=6, seuil=3. Aucun n'a 4+
        (['a', 'b', 'c'], None),  # Impair, aucun

        # 3. Cas limites (très importants)
        ([42], 42),  # Un seul élément n=1, seuil=0. '42' (1 fois)
        ([5, 5], 5),  # Deux éléments identiques n=2, seuil=1. '5' (2 fois)
        ([5, 1], None),  # Deux éléments différents n=2, seuil=1.
        ([], None),  # Liste vide n=0.
    ]

    print("Démarrage des tests de correction (Élément Majoritaire)...")

    for algo in algos_a_tester:
        algo_name = algo.__name__
        print(f"\n--- Test de : {algo_name} ---")

        for input_list, expected in test_cases:
            list_copy = list(input_list)
            try:
                result = algo(list_copy)
                assert result == expected, f"Liste {input_list}: Attendu {expected}, Obtenu {result}"
                print(f"  PASS: {input_list} -> {expected}")
            except AssertionError as e:
                print(f"  FAIL: {e}")
            except Exception as e:
                print(f"  ERROR: {input_list} a levé une exception inattendue: {e}")

    print("\n--- Tests terminés ---")




