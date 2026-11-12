"""
Maquina de Turing determinista, siguiendo la definicion vista en clase.

Lo unico que se guarda es lo que define una configuracion (Definicion 2):
el estado actual, el contenido de la cinta y la posicion de la cabeza.
No hay historial, cache ni memoria fuera de la cinta.
"""


class MaquinaTuring:
    def __init__(self, spec):
        self.Q = spec["Q"]
        self.Sigma = spec["Sigma"]
        self.Gamma = spec["Gamma"]
        self.blanco = spec["Blanco"]
        self.q0 = spec["q0"]
        self.qaccept = spec["qaccept"]
        self.qreject = spec["qreject"]
        # la tabla de delta: (q, a) -> (p, b, D)
        self.tabla = {(q, a): (p, b, d) for q, a, p, b, d, _ in spec["delta"]}

    def delta(self, q, a):
        """delta: Q x Gamma -> Q x Gamma x {L, R}"""
        return self.tabla[(q, a)]

    def configuracion_inicial(self, w):
        """Definicion 3: la configuracion inicial es q0 w (cabeza en el primer cuadro)."""
        cinta = list(w) if w else [self.blanco]
        return self.q0, cinta, 0

    def es_de_parada(self, q):
        """Definicion 6: aceptacion y rechazo no producen mas configuraciones."""
        return q == self.qaccept or q == self.qreject

    def paso(self, q, cinta, cabeza):
        """
        Una configuracion produce la siguiente:
          - izquierda:  ua qi bv  produce  u qj acv     si delta(qi, b) = (qj, c, L)
          - derecha:    ua qi bv  produce  uac qj v     si delta(qi, b) = (qj, c, R)
          - borde izq:  qi bv     produce  qj cv        si delta(qi, b) = (qj, c, L)
          - final:      ua qi     equivale a ua qi blanco
        """
        b = cinta[cabeza]
        qj, c, direccion = self.delta(q, b)
        cinta[cabeza] = c

        if direccion == "R":
            cabeza += 1
            if cabeza == len(cinta):
                cinta.append(self.blanco)  # despues de la cadena todo es blanco
        elif cabeza > 0:
            cabeza -= 1
        # si la cabeza ya esta en el extremo izquierdo y va a L, se queda en el mismo lugar

        return qj, cinta, cabeza


def escribir_configuracion(q, cinta, cabeza):
    """Notacion u q v: la cabeza esta sobre el primer simbolo de v."""
    return "".join(cinta[:cabeza]) + q + "".join(cinta[cabeza:])
