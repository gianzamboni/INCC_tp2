import os, sys

def filtrarArchivo(nombreArchivo):
	archivo = open(nombreArchivo)
	contenido = archivo.read()
	contenido = contenido.split("\n")
	diccionario = {}

	for palabra in contenido:
		if diccionario.has_key(palabra):
			diccionario[palabra] += 1;
		else:
			diccionario[palabra] = 1;

	sinRepetidos = diccionario.keys()
	sinRepetidosConEnter = [palabra + "\n" for palabra in sinRepetidos]
	contenidoSinRepetidos = "".join(sinRepetidosConEnter)
 

	print(contenidoSinRepetidos)
	
if __name__ == "__main__":
	listaArgumentos = sys.argv
	archivo = listaArgumentos[1]
	filtrarArchivo(archivo)