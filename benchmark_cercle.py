import math
import sys
import time
import random
from geometry import Point

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("ERREUR: 'matplotlib' est requis pour ce benchmark.")
    sys.exit(1)

# --- ÉTAPE 1 : Importe tes algorithmes ---
# NOTE : Renomme 'enveloppe_convexe' par le nom de TON fichier .py
try:
    from cas_de_test import generer_points_aleatoires, generer_points_cercle, generer_points_carre
    from visualisation import afficher_enveloppe
    from algorithms.glouton import trouver_enveloppe_glouton
    from algorithms.graham_scan import trouver_enveloppe_sklanski
    from algorithms.divide_conquer import trouver_enveloppe_diviser
except ImportError:
    print("ERREUR: Impossible d'importer les algos.")
    sys.exit(1)


#Constantes
NB_POINTS_CERCLE = 10000  
RAYON = 10 
ALGOS_A_TESTER = [
    trouver_enveloppe_glouton,
    trouver_enveloppe_sklanski,
]
COULEURS_PLOT = ['#FF0000', '#0000FF', '#00AA00', '#FF00FF', '#FFA500']


def generer_cercle_parfait(N, rayon):
    """
    Génère N points sur un cercle parfait en utilisant la trigonométrie.
    C'est le cas de test "idéal" où N = h (nb points sur l'enveloppe).
    """
    points = []
    for i in range(N):
        # Calcule l'angle pour ce point
        angle = (i / N) * 2 * math.pi


        # On ajoute une minuscule gigue (jitter) pour éviter une colinéarité verticale/horizontale parfaite peut perturber certains algos de tri.
        gigue = random.uniform(-1e-9, 1e-9)

        x = rayon * math.cos(angle) + gigue
        y = rayon * math.sin(angle) + gigue

        points.append(Point(x, y))

    return points


def lancer_benchmark_precision(algos, points):
    """
    Lance chaque algo sur la liste de points et stocke l'enveloppe trouvée.
    """
    print("Lancement du benchmark de précision sur un cercle...")
    print(f"Nombre total de points (N) : {len(points)}")
    print("-" * 40)

    resultats = {}

    for algo in algos:
        nom_algo = algo.__name__

        # Copie TRES importante, car Graham et Monotone trient la liste !
        points_copie = list(points)

        try:
            start_time = time.perf_counter()
            enveloppe_trouvee = algo(points_copie)
            duree = time.perf_counter() - start_time

            resultats[nom_algo] = enveloppe_trouvee
            print(f"  [OK] {nom_algo} (terminé en {duree * 1000:.2f} ms)")

        except Exception as e:
            print(f"  [ERREUR] {nom_algo} a levé une exception : {e}")
            resultats[nom_algo] = []  # Résultat vide en cas d'erreur

    return resultats


# --- ÉTAPE 5 : Analyse et Visualisation ---

def analyser_et_visualiser(resultats, points_cercle):
    """
    Calcule la précision (Métrique 1) et affiche le graphique (Métrique 2).
    """

    N = len(points_cercle)
    if N == 0: return

    print("\n" + "-" * 40)
    print("Analyse de la Précision (Points captés)")
    print(f"Objectif : {N} points (100%)")
    print("-" * 40)

    # --- 1. Analyse de la Précision (Texte) ---

    for i, (nom_algo, enveloppe) in enumerate(resultats.items()):

        # Le set() gère les algos qui répètent le premier point à la fin
        nb_points_uniques_captes = len(set(enveloppe))

        # Certains algos (Jarvis) peuvent répéter le premier point
        # On ajuste pour N ou N+1
        nb_points_attendus = N
        if len(enveloppe) == N + 1 and enveloppe[0] == enveloppe[-1]:
            nb_points_attendus = N + 1

        precision = (nb_points_uniques_captes / N) * 100

        # Affiche le résultat
        couleur = COULEURS_PLOT[i % len(COULEURS_PLOT)]
        print(f"  {nom_algo.ljust(20)}: {nb_points_uniques_captes} / {N} points   ({precision:.1f}%)")

    # --- 2. Visualisation (Graphique) ---

    print("\n... Génération du graphique 'benchmark_cercle.png' ...")

    plt.figure(figsize=(10, 10))

    # Sépare les points du cercle pour le scatter plot
    cercle_x = [p.x for p in points_cercle]
    cercle_y = [p.y for p in points_cercle]

    # Affiche les points originaux en gris
    plt.scatter(cercle_x, cercle_y, color='gray', s=30,
                label=f'Points originaux (N={N})', zorder=1)

    # Superpose chaque enveloppe trouvée
    for i, (nom_algo, enveloppe) in enumerate(resultats.items()):
        if not enveloppe:  # Si l'algo a échoué
            continue

        couleur = COULEURS_PLOT[i % len(COULEURS_PLOT)]

        # Sépare les points de l'enveloppe pour le plot
        # Assure-toi que l'enveloppe est "fermée" pour le tracé
        enveloppe_fermee = enveloppe + [enveloppe[0]]
        enveloppe_x = [p.x for p in enveloppe_fermee]
        enveloppe_y = [p.y for p in enveloppe_fermee]

        plt.plot(enveloppe_x, enveloppe_y, color=couleur, linewidth=2,
                 label=f'{nom_algo} ({len(enveloppe)} pts)', zorder=i + 2)

    plt.title(f"Précision des Enveloppes Convexes sur un Cercle Parfait (N={N})")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)

    # ESSENTIEL pour un cercle :
    plt.axis('equal')

    plt.savefig("benchmark_cercle.png")
    print("Graphique sauvegardé !")
    # plt.show() # Décommente pour afficher le graphique


# --- Point d'entrée principal ---
if __name__ == "__main__":
    points_test = generer_cercle_parfait(NB_POINTS_CERCLE, RAYON)

    resultats_des_algos = lancer_benchmark_precision(ALGOS_A_TESTER, points_test)

    analyser_et_visualiser(resultats_des_algos, points_test)