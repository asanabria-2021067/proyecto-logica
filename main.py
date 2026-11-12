"""
Simulador de una maquina de Turing determinista.

Uso:
    python main.py <archivo_entrada> [archivo_salida] [--max-pasos N]

Ejemplo:
    python main.py entradas/acepta.txt salidas/acepta_salida.txt

El limite de pasos es del simulador, no de la maquina: sirve para que la
salida de una cadena que cicla sea un archivo finito.
"""

import os
import sys

from lector import ErrorLectura, leer_archivo
from maquina import MaquinaTuring, escribir_configuracion
from validador import validar

MAX_PASOS_DEFECTO = 1000


def describir_maquina(spec):
    lineas = [
        "M = (Q, Sigma, Gamma, delta, q0, qaccept, qreject)",
        "Q = {" + ", ".join(spec["Q"]) + "}",
        "Sigma = {" + ", ".join(spec["Sigma"]) + "}",
        "Gamma = {" + ", ".join(spec["Gamma"]) + "}",
        f"Blanco = {spec['Blanco']}",
        f"q0 = {spec['q0']}",
        f"qaccept = {spec['qaccept']}",
        f"qreject = {spec['qreject']}",
        "delta:",
    ]
    for q, a, p, b, d, _ in spec["delta"]:
        lineas.append(f"    delta({q}, {a}) = ({p}, {b}, {d})")
    return lineas


def simular(spec, salida, max_pasos):
    M = MaquinaTuring(spec)
    w = spec["w"]

    for linea in describir_maquina(spec):
        salida.write(linea + "\n")
    salida.write(f"\nCadena de entrada: w = {w if w else 'e (cadena vacia)'}\n")
    salida.write("\nConfiguraciones:\n")

    q, cinta, cabeza = M.configuracion_inicial(w)
    i = 1
    salida.write(f"C{i} = {escribir_configuracion(q, cinta, cabeza)}\n")

    while not M.es_de_parada(q) and i <= max_pasos:
        q, cinta, cabeza = M.paso(q, cinta, cabeza)
        i += 1
        salida.write(f"C{i} = {escribir_configuracion(q, cinta, cabeza)}\n")

    salida.write("\n")
    if q == M.qaccept:
        resultado = f"C{i} es una configuracion de aceptacion. M acepta w."
    elif q == M.qreject:
        resultado = f"C{i} es una configuracion de rechazo. M rechaza w."
    else:
        resultado = (
            f"Despues de {max_pasos} pasos M no llego a {M.qaccept} ni a {M.qreject}. "
            "La maquina esta en un ciclo infinito, se detuvo la simulacion."
        )
    salida.write("Resultado: " + resultado + "\n")
    return resultado


def main():
    argumentos = sys.argv[1:]
    max_pasos = MAX_PASOS_DEFECTO
    if "--max-pasos" in argumentos:
        indice = argumentos.index("--max-pasos")
        max_pasos = int(argumentos[indice + 1])
        del argumentos[indice : indice + 2]

    if not argumentos:
        print(__doc__)
        sys.exit(1)

    ruta_entrada = argumentos[0]
    if len(argumentos) > 1:
        ruta_salida = argumentos[1]
    else:
        nombre = os.path.splitext(os.path.basename(ruta_entrada))[0]
        ruta_salida = os.path.join("salidas", nombre + "_salida.txt")

    try:
        spec = leer_archivo(ruta_entrada)
    except (ErrorLectura, OSError) as error:
        print(f"Error al leer el archivo: {error}")
        sys.exit(1)

    errores = validar(spec)
    if errores:
        print("La especificacion de la maquina de Turing NO es correcta:")
        for error in errores:
            print("  - " + error)
        sys.exit(1)
    print("La especificacion de la maquina de Turing es correcta.")

    carpeta = os.path.dirname(ruta_salida)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    with open(ruta_salida, "w", encoding="utf-8") as salida:
        resultado = simular(spec, salida, max_pasos)

    print(resultado)
    print(f"Configuraciones guardadas en: {ruta_salida}")


if __name__ == "__main__":
    main()
