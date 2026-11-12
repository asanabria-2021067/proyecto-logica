"""
Verifica que la especificacion cumpla la Definicion 1:

    M = (Q, Sigma, Gamma, delta, q0, qaccept, qreject)

    1. Q es un conjunto finito de estados
    2. Sigma es el alfabeto de entrada y no contiene al blanco
    3. Gamma es el alfabeto de la cinta, blanco en Gamma y Sigma subconjunto de Gamma
    4. delta: Q x Gamma -> Q x Gamma x {L, R} es la funcion de transicion
    5. q0 en Q es el estado inicial
    6. qaccept en Q es el estado de aceptacion
    7. qreject en Q es el estado de rechazo, qreject != qaccept

Como la maquina es determinista, delta es una FUNCION: a cada par (q, a)
le toca exactamente un resultado. Por eso se revisa que no haya pares
repetidos ni pares sin definir (para los estados que no son de parada).
"""

DIRECCIONES = ("L", "R")


def revisar_repetidos(nombre, elementos, errores):
    vistos = set()
    for elemento in elementos:
        if elemento in vistos:
            errores.append(f"{nombre}: el elemento '{elemento}' esta repetido")
        vistos.add(elemento)


def validar(spec):
    """Devuelve una lista con todos los errores encontrados (vacia si todo esta bien)."""
    errores = []
    Q, Sigma, Gamma = spec["Q"], spec["Sigma"], spec["Gamma"]
    blanco = spec["Blanco"]
    q0, qaccept, qreject = spec["q0"], spec["qaccept"], spec["qreject"]

    # 1. Q
    if not Q:
        errores.append("Q no puede estar vacio")
    revisar_repetidos("Q", Q, errores)

    # 2 y 3. alfabetos
    if not Sigma:
        errores.append("Sigma no puede estar vacio")
    revisar_repetidos("Sigma", Sigma, errores)
    revisar_repetidos("Gamma", Gamma, errores)

    for simbolo in Gamma:
        if len(simbolo) != 1:
            errores.append(f"Gamma: el simbolo '{simbolo}' debe ser de un solo caracter")

    if len(blanco) != 1:
        errores.append(f"El blanco '{blanco}' debe ser de un solo caracter")
    if blanco not in Gamma:
        errores.append(f"El blanco '{blanco}' debe pertenecer a Gamma")
    if blanco in Sigma:
        errores.append(f"El blanco '{blanco}' no puede pertenecer a Sigma")
    for simbolo in Sigma:
        if simbolo not in Gamma:
            errores.append(f"Sigma no es subconjunto de Gamma: '{simbolo}' no esta en Gamma")

    # los nombres de estados no deben confundirse con simbolos de la cinta
    for estado in Q:
        if estado in Gamma:
            errores.append(f"El estado '{estado}' tiene el mismo nombre que un simbolo de Gamma")

    # 5, 6 y 7. estados especiales
    if q0 not in Q:
        errores.append(f"q0 = '{q0}' no pertenece a Q")
    if qaccept not in Q:
        errores.append(f"qaccept = '{qaccept}' no pertenece a Q")
    if qreject not in Q:
        errores.append(f"qreject = '{qreject}' no pertenece a Q")
    if qaccept == qreject:
        errores.append("qaccept y qreject deben ser estados distintos")

    # 4. delta es una funcion Q x Gamma -> Q x Gamma x {L, R}
    definidos = {}
    for q, a, p, b, d, linea in spec["delta"]:
        donde = f"delta, linea {linea}"
        if q not in Q:
            errores.append(f"{donde}: el estado '{q}' no pertenece a Q")
        if a not in Gamma:
            errores.append(f"{donde}: el simbolo '{a}' no pertenece a Gamma")
        if p not in Q:
            errores.append(f"{donde}: el estado '{p}' no pertenece a Q")
        if b not in Gamma:
            errores.append(f"{donde}: el simbolo '{b}' no pertenece a Gamma")
        if d not in DIRECCIONES:
            errores.append(f"{donde}: la direccion '{d}' debe ser L o R")
        if q in (qaccept, qreject):
            errores.append(
                f"{donde}: '{q}' es un estado de parada y no puede tener transiciones (Definicion 6)"
            )
        if (q, a) in definidos:
            errores.append(
                f"{donde}: delta({q}, {a}) ya estaba definida en la linea {definidos[(q, a)]}. "
                "Una maquina determinista no puede tener dos transiciones para el mismo par"
            )
        else:
            definidos[(q, a)] = linea

    # delta debe estar definida para todo (q, a) con q que no sea de parada
    for q in Q:
        if q in (qaccept, qreject):
            continue
        for a in Gamma:
            if (q, a) not in definidos:
                errores.append(f"delta({q}, {a}) no esta definida")

    # la cadena de entrada solo usa simbolos de Sigma
    for simbolo in spec["w"]:
        if simbolo not in Sigma:
            errores.append(f"La cadena w = '{spec['w']}' usa el simbolo '{simbolo}' que no esta en Sigma")
            break

    return errores
