#!/usr/bin/env python
# Importamos el paquete sys para poder accesar stdin (entrada estandar)
import sys

# Iniciamos un for loop o bucle for cada linea en stdin
for line in sys.stdin:
    # Removemos espacios en blanco a la derecha e izquierda de cada linea
    line = line.strip()
    # Luego dividimos la linea en una lista. split por defecto usa espacios para dividir
    words = line.split()
    # Luego empezamos un nuevo for loop para cada palabra en la lista de palabras
    for word in words:
        # Escribimos los resultados a stdout (salida estandar);
        # Lo que escribamos aqui se convertira en la entrada para la fase reduce
        #
        # Delimitado por tabulador - aqui simplemente imprimimos la cuenta de cada palabra
        # La cual siempre sera 1
        print('%s\t%s' % (word, 1))
