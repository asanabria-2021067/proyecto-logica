# Simulador de máquina de Turing determinista

Parcial #4 - Lógica Matemática

## Uso

```
python main.py <archivo_entrada> [archivo_salida] [--max-pasos N]
```

Si no se da archivo de salida, se guarda en `salidas/<nombre>_salida.txt`.
`--max-pasos` (por defecto 1000) es el límite del simulador para cortar las cadenas que ciclan.

```
python main.py entradas/acepta.txt
python main.py entradas/rechaza.txt
python main.py entradas/ciclo.txt --max-pasos 50
```

## Archivos

- `lector.py`: lee el archivo de texto con la 7-tupla y la cadena w.
- `validador.py`: revisa que la especificación cumpla la definición (delta como función).
- `maquina.py`: la función delta y el paso de una configuración a la siguiente.
- `main.py`: ejecuta la máquina y escribe las configuraciones.
- `entradas/`: máquina del inciso b con una cadena que acepta, una que rechaza y una que cicla.
- `salidas/`: configuraciones generadas.
