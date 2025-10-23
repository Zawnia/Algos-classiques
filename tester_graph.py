import time
import matplotlib.pyplot as plt
from typing import List
from cas_de_test import generer_points_aleatoires, generer_points_cercle, generer_points_carre
from visualisation import afficher_enveloppe
from algorithms.glouton import trouver_enveloppe_glouton
from algorithms.graham_scan import trouver_enveloppe_sklanski
from algorithms.divide_conquer import trouver_enveloppe_diviser


# =============================================================================
# PARTIE 1 : TEST VISUEL SIMPLE
# =============================================================================
print("--- Lancement du Test Visuel Simple ---")

# 1. Générer un nuage de points
N_VISUEL = 100
#points_visu = cas_de_test.generer_points_aleatoires(N_VISUEL)
points_visu = generer_points_cercle(N_VISUEL // 2) # Test "cercle"

# 2. Calculer l'enveloppe
enveloppe_visu = trouver_enveloppe_diviser(points_visu)
print(enveloppe_visu)

print(f"Test visuel (Jarvis) sur {len(points_visu)} points.")
print(f"Points sur l'enveloppe : {len(enveloppe_visu)}")

# 3. Afficher le résultat
afficher_enveloppe(
    points_visu, 
    enveloppe_visu, 
    f"Diviser en 2 ({len(enveloppe_visu)} points sur {len(points_visu)})"
)
