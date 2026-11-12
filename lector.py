"""
Lector del archivo de especificacion de la maquina de Turing.

Formato del archivo (las lineas que empiezan con # son comentarios):

    Q = {q1, q2, qaccept, qreject}
    Sigma = {0, 1}
    Gamma = {0, 1, X, _}
    Blanco = _
    q0 = q1
    qaccept = qaccept
    qreject = qreject
    delta:
    (q1, 0) = (q2, X, R)
    ...
    w = 0011

Solo lee el texto y lo pasa a estructuras de Python.
Si la especificacion tiene sentido o no lo revisa validador.py.
"""

import re

# delta(q, a) = (p, b, D)
PATRON_TRANSICION = re.compile(
    r"^\(\s*([^,\s]+)\s*,\s*([^,\s]+)\s*\)\s*=\s*\(\s*([^,\s]+)\s*,\s*([^,\s]+)\s*,\s*([^,\s)]+)\s*\)$"
)

CAMPOS = ["Q", "Sigma", "Gamma", "Blanco", "q0", "qaccept", "qreject", "w"]


class ErrorLectura(Exception):
    pass


def leer_conjunto(texto, num_linea):
    texto = texto.strip()
    if not (texto.startswith("{") and texto.endswith("}")):
        raise ErrorLectura(f"Linea {num_linea}: un conjunto debe ir entre llaves, por ejemplo {{a, b}}")
    contenido = texto[1:-1].strip()
    if contenido == "":
        return []
    return [elemento.strip() for elemento in contenido.split(",")]


def leer_archivo(ruta):
    """Devuelve un diccionario con los componentes tal como vienen en el archivo."""
    with open(ruta, encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    spec = {"delta": []}  # delta es una lista de (q, a, p, b, D, num_linea)
    leyendo_delta = False

    for num_linea, linea in enumerate(lineas, start=1):
        linea = linea.strip()
        if linea == "" or linea.startswith("#"):
            continue

        if linea.lower().startswith("delta"):
            leyendo_delta = True
            continue

        coincide = PATRON_TRANSICION.match(linea)
        if leyendo_delta and coincide:
            q, a, p, b, d = coincide.groups()
            spec["delta"].append((q, a, p, b, d, num_linea))
            continue

        if "=" not in linea:
            raise ErrorLectura(f"Linea {num_linea}: no se entiende '{linea}'")

        nombre, valor = linea.split("=", 1)
        nombre = nombre.strip()
        valor = valor.strip()

        if nombre not in CAMPOS:
            if leyendo_delta:
                raise ErrorLectura(
                    f"Linea {num_linea}: la transicion debe tener la forma (q, a) = (p, b, D)"
                )
            raise ErrorLectura(f"Linea {num_linea}: componente desconocido '{nombre}'")

        leyendo_delta = False
        if nombre in spec:
            raise ErrorLectura(f"Linea {num_linea}: el componente '{nombre}' esta repetido")

        if nombre in ("Q", "Sigma", "Gamma"):
            spec[nombre] = leer_conjunto(valor, num_linea)
        else:
            spec[nombre] = valor

    # la cadena vacia se puede escribir como w = (nada) o w = e
    if spec.get("w") in ("e", "ε"):
        spec["w"] = ""

    faltantes = [campo for campo in CAMPOS if campo not in spec]
    if faltantes:
        raise ErrorLectura("Faltan componentes en el archivo: " + ", ".join(faltantes))

    return spec
