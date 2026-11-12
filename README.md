# Simulador de máquina de Turing determinista

Parcial #4 - MM3032 Lógica Matemática, sección 20 - Universidad del Valle de Guatemala

## Integrantes

- Angel Gabriel Sanabria Morales - 24725
- Javier Sebastián Alvarado Monzón - 24546
- Vernel Josué Hernández Cáceres - 24584
- Derek Friedhelm Coronado Chilin - 24732
- Ronald Manuel Catún Chacón - 19789

## Qué hace

El programa carga un archivo de texto con la 7-tupla de una máquina de Turing
M = (Q, Σ, Γ, δ, q0, qaccept, qreject) y una cadena de entrada w. Primero verifica
que la especificación sea correcta y luego ejecuta la máquina, guardando en un
archivo de texto todas las configuraciones con la notación vista en clase (u q v).

Se tomó la definición del documento del curso tal cual:

- La máquina es determinista, por eso δ es una función: δ: Q × Γ → Q × Γ × {L, R}.
  A cada par (estado, símbolo) le toca exactamente un resultado.
- Lo único que se guarda es la configuración: estado actual, contenido de la cinta y
  posición de la cabeza. No se usa caché, historial ni memoria fuera de la cinta.
- Si la cabeza está en el extremo izquierdo y δ indica L, la cabeza se queda en el mismo lugar.
- Cuando la cabeza pasa el final de la cadena, lee un blanco (ua qi equivale a ua qi ⊔).
- Las configuraciones de aceptación y rechazo son de parada y no producen más configuraciones.

## Requisitos

Python 3.8 o más reciente. No usa librerías externas.

## Cómo usarlo

```
python main.py <archivo_entrada> [archivo_salida] [--max-pasos N]
```

- `archivo_entrada`: archivo de texto con la máquina y la cadena.
- `archivo_salida` (opcional): dónde guardar las configuraciones. Si no se pone, se guarda en
  `salidas/<nombre_entrada>_salida.txt`.
- `--max-pasos N` (opcional, por defecto 1000): límite del simulador. Una máquina que cicla
  nunca para, entonces el simulador corta después de N pasos para que el archivo de salida
  sea finito. No es parte de la máquina.

Ejemplos (incisos c a h):

```
python main.py entradas/acepta.txt
python main.py entradas/rechaza.txt
python main.py entradas/ciclo.txt --max-pasos 50
```

Ejemplo del documento del curso (máquina M2, cadena 0000):

```
python main.py entradas/ejemplo_M2_documento.txt
```

## Formato del archivo de entrada

```
# las líneas que empiezan con # son comentarios
Q = {q1, q2, qaccept, qreject}
Sigma = {0, 1}
Gamma = {0, 1, X, _}
Blanco = _
q0 = q1
qaccept = qaccept
qreject = qreject
delta:
(q1, 0) = (q2, X, R)
(q1, 1) = (qreject, 1, R)
...
w = 0011
```

- Cada transición se escribe como δ(q, a) = (p, b, D), es decir `(q, a) = (p, b, D)`, con D igual a L o R.
- Los símbolos de Γ son de un solo carácter.
- `Blanco` indica qué símbolo de Γ es el blanco ⊔ (puede ser `_` o el mismo `⊔`).
- La cadena vacía se escribe `w = e` o `w =`.

## Verificaciones de la especificación

Antes de ejecutar, el programa revisa:

1. Q, Σ y Γ no están vacíos y no tienen elementos repetidos.
2. El blanco pertenece a Γ y no pertenece a Σ.
3. Σ es subconjunto de Γ.
4. q0, qaccept y qreject pertenecen a Q, y qaccept ≠ qreject.
5. Cada transición usa estados de Q, símbolos de Γ y dirección L o R.
6. δ es función: no hay dos transiciones para el mismo par (q, a).
7. δ está definida para todos los pares (q, a) con q distinto de qaccept y qreject.
8. qaccept y qreject no tienen transiciones de salida.
9. La cadena w solo usa símbolos de Σ.

Si algo falla, el programa muestra todos los errores encontrados y no ejecuta la máquina.

## Formato de la salida

```
Configuraciones:
C1 = q1000111
C2 = Xq200111
...
C26 = XXXYYY_qaccept_

Resultado: C26 es una configuracion de aceptacion. M acepta w.
```

Al inicio del archivo se repite la especificación de la máquina y la cadena de entrada.

## Máquina del inciso b

- Acepta L = {0ⁿ1ⁿ | n ≥ 1}.
- Rechaza las cadenas que empiezan con 0 y no son de la forma 0ⁿ1ⁿ.
- Las cadenas que empiezan con 1 entran a q5 y q6, que mueven la cabeza a la izquierda y a
  la derecha sin parar (ciclo infinito).

| Archivo | Cadena | Resultado |
|---|---|---|
| `entradas/acepta.txt` | 000111 | acepta en C26 |
| `entradas/rechaza.txt` | 00101 | rechaza en C15 |
| `entradas/ciclo.txt` | 10 | ciclo infinito (se cortó en 50 pasos) |

## Archivos

- `main.py`: punto de entrada; ejecuta la máquina y escribe las configuraciones.
- `lector.py`: lee el archivo de texto con la 7-tupla y la cadena w.
- `validador.py`: verifica la especificación según la definición.
- `maquina.py`: la función δ y el paso de una configuración a la siguiente.
- `entradas/`: archivos de entrada.
- `salidas/`: configuraciones generadas.
