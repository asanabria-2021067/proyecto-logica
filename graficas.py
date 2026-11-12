"""
Graficas y tablas para demostrar el comportamiento de la maquina del inciso b).

Este script NO es parte del simulador. El simulador (main.py) no guarda
historial; aqui si se guardan las configuraciones, pero solo para poder
graficarlas despues.

Uso:
    pip install matplotlib
    python graficas.py

Genera las imagenes en la carpeta graficas/ y muestra las tablas en consola.
"""

import itertools
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from lector import leer_archivo
from maquina import MaquinaTuring

CARPETA = "graficas"
AZUL, NARANJA, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
TINTA, GRIS, REJILLA = "#1e1e1e", "#6b6b6b", "#e4e4e0"

plt.rcParams.update({
    # DejaVu Sans viene con matplotlib y tiene el simbolo del blanco
    "font.family": ["Times New Roman", "Liberation Serif", "DejaVu Sans"],
    "font.size": 11,
    "axes.edgecolor": GRIS,
    "axes.labelcolor": TINTA,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.color": GRIS,
    "ytick.color": GRIS,
    "axes.grid": True,
    "axes.axisbelow": True,
    "grid.color": REJILLA,
    "grid.linewidth": 0.8,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
})


def ejecutar(M, w, max_pasos):
    """Devuelve la lista de configuraciones (estado, cinta, cabeza) hasta parar o llegar al limite."""
    q, cinta, cabeza = M.configuracion_inicial(w)
    traza = [(q, list(cinta), cabeza)]
    while not M.es_de_parada(q) and len(traza) <= max_pasos:
        q, cinta, cabeza = M.paso(q, cinta, cabeza)
        traza.append((q, list(cinta), cabeza))
    return traza


def resultado(M, traza):
    q = traza[-1][0]
    if q == M.qaccept:
        return "acepta"
    if q == M.qreject:
        return "rechaza"
    return "cicla"


def tabla_delta(M):
    simbolos = M.Gamma
    print("\nTabla de la funcion delta")
    print("estado | " + " | ".join(simbolos))
    for q in M.Q:
        if M.es_de_parada(q):
            continue
        fila = []
        for a in simbolos:
            p, b, d = M.delta(q, a)
            fila.append(f"({p}, {b}, {d})")
        print(f"{q} | " + " | ".join(fila))


def grafica_cabeza_y_estados(M, casos):
    """Posicion de la cabeza y estado en cada paso, para las tres cadenas."""
    orden = [q for q in M.Q]
    fig, ejes = plt.subplots(2, 3, figsize=(12, 6.4), sharex="col")
    for col, (titulo, w, color, maximo) in enumerate(casos):
        traza = ejecutar(M, w, maximo)
        pasos = list(range(1, len(traza) + 1))
        cabezas = [c for _, _, c in traza]
        estados = [orden.index(q) for q, _, _ in traza]

        ax = ejes[0][col]
        ax.plot(pasos, cabezas, color=color, linewidth=2, marker="o", markersize=4)
        ax.set_title(f"{titulo}\nw = {w}", fontsize=12, color=TINTA)
        ax.set_ylabel("Posición de la cabeza" if col == 0 else "")
        ax.set_ylim(-0.5, max(cabezas) + 1)
        ax.yaxis.get_major_locator().set_params(integer=True)

        ax = ejes[1][col]
        ax.step(pasos, estados, where="post", color=color, linewidth=2)
        ax.plot(pasos, estados, "o", color=color, markersize=4)
        ax.set_yticks(range(len(orden)))
        ax.set_yticklabels(orden)
        ax.set_xlabel("Configuración Ci")
        ax.set_ylabel("Estado" if col == 0 else "")
        final = traza[-1][0]
        if M.es_de_parada(final):
            ax.annotate(final, (pasos[-1], estados[-1]), textcoords="offset points", xytext=(-8, 8),
                        ha="right", color=TINTA, fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(CARPETA, "cabeza_y_estados.png"))
    plt.close(fig)


def grafica_cinta(M, w, nombre):
    """Diagrama espacio-tiempo: cada fila es una configuracion y cada columna un cuadro de la cinta."""
    traza = ejecutar(M, w, 1000)
    ancho = max(len(c) for _, c, _ in traza)
    filas = len(traza)
    fig, ax = plt.subplots(figsize=(0.55 * ancho + 2.6, 0.27 * filas + 0.8))
    ax.grid(False)
    for i, (q, cinta, cabeza) in enumerate(traza):
        y = filas - 1 - i
        for j in range(ancho):
            simbolo = cinta[j] if j < len(cinta) else M.blanco
            es_cabeza = j == cabeza
            ax.add_patch(Rectangle((j, y), 1, 1, facecolor="#cde2fb" if es_cabeza else "white",
                                   edgecolor="#b5b5b0", linewidth=0.6))
            ax.text(j + 0.5, y + 0.5, simbolo, ha="center", va="center", fontsize=10,
                    color=TINTA, fontweight="bold" if es_cabeza else "normal")
        ax.text(-0.3, y + 0.5, f"C{i + 1}", ha="right", va="center", fontsize=9, color=GRIS)
        ax.text(ancho + 0.3, y + 0.5, q, ha="left", va="center", fontsize=9, color=TINTA)
    ax.set_xlim(-1.6, ancho + 2.2)
    ax.set_ylim(0, filas)
    ax.set_xticks([j + 0.5 for j in range(ancho)])
    ax.set_xticklabels([str(j) for j in range(ancho)])
    ax.tick_params(axis="x", length=0, labelsize=9)
    ax.set_yticks([])
    for lado in ("left", "bottom"):
        ax.spines[lado].set_visible(False)
    ax.set_xlabel("Cuadro de la cinta (el sombreado es la posición de la cabeza)", fontsize=10)
    fig.savefig(os.path.join(CARPETA, nombre))
    plt.close(fig)


def pasos_por_n(M, n_max):
    datos = []
    for n in range(1, n_max + 1):
        traza = ejecutar(M, "0" * n + "1" * n, 100000)
        datos.append((n, len(traza)))
    return datos


def grafica_pasos(datos):
    ns = [n for n, _ in datos]
    pasos = [p for _, p in datos]
    fig, ax = plt.subplots(figsize=(7, 3.8))
    ax.plot(ns, pasos, color=AZUL, linewidth=2, marker="o", markersize=6, label="Configuraciones medidas")
    curva = [2 * n * n + 2 * n + 2 for n in ns]
    ax.plot(ns, curva, color=TINTA, linewidth=1, linestyle="--", label="2n² + 2n + 2")
    for n, p in datos[-1:]:
        ax.annotate(f"{p}", (n, p), textcoords="offset points", xytext=(-6, 6), ha="right", fontsize=10)
    ax.set_xlabel("n en la cadena 0ⁿ1ⁿ")
    ax.set_ylabel("Configuraciones hasta qaccept")
    ax.set_xticks(ns)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(os.path.join(CARPETA, "pasos_vs_n.png"))
    plt.close(fig)


def clasificar(M, largo_max, limite):
    conteo = []
    for largo in range(0, largo_max + 1):
        c = {"acepta": 0, "rechaza": 0, "cicla": 0}
        for tupla in itertools.product(M.Sigma, repeat=largo):
            w = "".join(tupla)
            c[resultado(M, ejecutar(M, w, limite))] += 1
        conteo.append((largo, c["acepta"], c["rechaza"], c["cicla"]))
    return conteo


def grafica_clasificacion(conteo):
    largos = [l for l, *_ in conteo]
    total = [a + r + c for _, a, r, c in conteo]
    series = [("Acepta", 1, AZUL), ("Rechaza", 2, NARANJA), ("Cicla", 3, AQUA)]
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    ancho = 0.26
    for k, (nombre, idx, color) in enumerate(series):
        xs = [l + (k - 1) * (ancho + 0.02) for l in largos]
        ys = [100 * fila[idx] / t for fila, t in zip(conteo, total)]
        ax.bar(xs, ys, width=ancho, color=color, label=nombre)
        if nombre == "Acepta":
            for x, y, fila in zip(xs, ys, conteo):
                if fila[idx]:
                    ax.annotate(f"{fila[idx]} de {sum(fila[1:])}", (x, y), textcoords="offset points",
                                xytext=(0, 3), ha="center", fontsize=8, color=TINTA)
    ax.set_xticks(largos)
    ax.set_xlabel("Largo de la cadena w")
    ax.set_ylabel("% de las cadenas de ese largo")
    ax.set_ylim(0, 105)
    ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.12))
    fig.tight_layout()
    fig.savefig(os.path.join(CARPETA, "clasificacion.png"))
    plt.close(fig)


def main():
    os.makedirs(CARPETA, exist_ok=True)
    M = MaquinaTuring(leer_archivo("entradas/acepta.txt"))

    tabla_delta(M)

    casos = [("Acepta", "000111", AZUL, 1000),
             ("Rechaza", "00101", NARANJA, 1000),
             ("Cicla (primeras 20)", "10", AQUA, 19)]
    grafica_cabeza_y_estados(M, casos)
    grafica_cinta(M, "000111", "cinta_acepta.png")
    grafica_cinta(M, "00101", "cinta_rechaza.png")

    datos = pasos_por_n(M, 10)
    grafica_pasos(datos)
    print("\nn | configuraciones hasta qaccept | 2n^2 + 2n + 2")
    for n, p in datos:
        print(f"{n} | {p} | {2 * n * n + 2 * n + 2}")

    conteo = clasificar(M, 8, 2000)
    grafica_clasificacion(conteo)
    print("\nlargo | total | acepta | rechaza | cicla")
    for largo, a, r, c in conteo:
        print(f"{largo} | {a + r + c} | {a} | {r} | {c}")

    print(f"\nGraficas guardadas en la carpeta {CARPETA}/")


if __name__ == "__main__":
    main()
