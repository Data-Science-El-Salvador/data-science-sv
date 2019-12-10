#!/usr/bin/env python
import sys

# Iniciamos ciertas variables que usaremos a lo largo del programa
# current_word es la palabra actual despues de cada iteracion - inicializada a None
current_word = None
# current_count es la cuenta de la palabra actual despues de cada iteracion - inicializada a 0
current_count = 0
# word es la palabra que leeremos de stdin - inicializada a None
word = None

# Por cada linea de stdin
for line in sys.stdin:
    # Removemos espacios en blanco a la derecha e izquierda de cada linea
    line = line.strip()

    # Dividimos la linea en dos variables, usando el caracter tabulador para dividir
    # Sabemos que la palabra y la cuenta estan delimitados por un tabulador
    word, count = line.split('\t', 1)

    # Convertimos la cuenta (actualmente una cadena o string) a un entero o int
    # Usamos un bloque try-except en caso que la cuenta no se pueda convertir a int
    try:
        count = int(count)
    except ValueError:
        # No queremos interrumpir el programa asi que continuamos con la siguiente iteracion
        continue

    # El condicional if aqui solo funciona porque mapreduce ordena los datos
    # por clave (en este caso por palabra) antes que es pasado al reducer
    # Primero evaluamos si la palabra actual es igual a la palabra en esta iteracion
    if current_word == word:
        # Si lo es, incrementamos su cuenta
        current_count += count
    else:
        # Si no lo es, y el valor de la palabra actual es un valor verdadero
        if current_word:
            # Escribimos los resultados a stdout
            print('%s\t%s' % (current_word, current_count))
        # Dado que la palabra en esta iteracion es diferente a la palabra actual
        # Asignamos esta palabra a la palabra actual, y su cuenta a la cuenta actual
        current_count = count
        current_word = word

# Por ultimo, imprimimos la palabra actual y su cuenta a stdout
if current_word == word:
    print('%s\t%s' % (current_word, current_count))
