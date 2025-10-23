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

print(f"Test visuel (Jarvis) sur {len(points_visu)} points.")
print(f"Points sur l'enveloppe : {len(enveloppe_visu)}")

# 3. Afficher le résultat
afficher_enveloppe(
    points_visu, 
    enveloppe_visu, 
    f"Marche de Jarvis ({len(enveloppe_visu)} points sur {len(points_visu)})"
)


# =============================================================================
# PARTIE 2 : ANALYSE DE COMPLEXITÉ 
# =============================================================================
print("\n--- Lancement de l'Analyse de Complexité ---")

# Définir les algos à comparer.
# C'est MODULAIRE : ajoutez vos futurs algos ici !
algos_a_tester = [
    {
        "nom": "Jarvis (Cas Moyen, aléatoire)",
        "func": trouver_enveloppe_glouton,
        "generateur": generer_points_aleatoires
    },
    {
        "nom": "Jarvis (Pire Cas, cercle)",
        "func": trouver_enveloppe_glouton,
        "generateur": generer_points_cercle
    },
    {
         "nom": "Graham Scan (Cas Moyen)",
         "func": trouver_enveloppe_sklanski, 
         "generateur": generer_points_aleatoires
    },
    {
        "nom": "Diviser pour Régner (Cas Moyen)",
        "func": trouver_enveloppe_diviser,
        "generateur": generer_points_aleatoires
    },
    {
        "nom": "Diviser pour Régner (Pire cas)",
        "func": trouver_enveloppe_diviser,
        "generateur": generer_points_cercle
    }

]

# Définir les tailles de 'n' (nombre de points) à tester
tailles_n = [10, 50, 100, 250, 500, 750, 1000]

# Dictionnaire pour stocker tous les résultats
resultats_temps = {}

# --- Boucle de Test ---
for algo in algos_a_tester:
    nom_algo = algo["nom"]
    fonction_algo = algo["func"]
    generateur_points = algo["generateur"]
    
    print(f"\nTest de l'algorithme : {nom_algo}")
    
    temps_passes = [] # Liste pour les temps de cet algo
    
    for n in tailles_n:
        # 1. Générer les points
        points_test = generateur_points(n)
        
        # 2. Chronométrer l'exécution
        t_debut = time.perf_counter()
        fonction_algo(points_test)
        t_fin = time.perf_counter()
        
        temps_ecoule = t_fin - t_debut
        temps_passes.append(temps_ecoule)
        print(f"  n = {n:<5} -> {temps_ecoule:.6f} secondes")
    
    # Stocker les résultats pour le graphique
    resultats_temps[nom_algo] = temps_passes

# --- Affichage du Graphique de Complexité ---
plt.figure(figsize=(12, 8))

# Tracer une courbe pour chaque algo testé
for nom_algo, temps in resultats_temps.items():
    plt.plot(tailles_n, temps, 'o-', label=nom_algo, linewidth=2)

plt.xlabel("Nombre de points (n)", fontsize=14)
plt.ylabel("Temps d'exécution (secondes)", fontsize=14)
plt.title("Analyse de Complexité (Temps)", fontsize=16)
plt.legend()
plt.grid(True)
# plt.yscale('log') # Dé-commentez si les écarts sont trop grands !
plt.show()

