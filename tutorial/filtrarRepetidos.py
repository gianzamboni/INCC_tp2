import os, sys
import pickle
import json

def filtrarListas(archivoList):
	print(archivoList)
	f = open(archivoList, "rb")
	diccionario = {}
	contenido = pickle.load(f)
	f.close()
	for palabra in contenido:
		if diccionario.has_key(palabra):
			diccionario[palabra] += 1;
		else:
			diccionario[palabra] = 1;

	f = open(archivoList, "wb")
	lista = diccionario.keys()
	pickle.dump(diccionario.keys(), f)
	f.close()

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

	for filename in os.listdir(archivo):
		filtrarListas(os.path.join(archivo, filename))