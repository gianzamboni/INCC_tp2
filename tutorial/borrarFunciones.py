import os, re

if __name__ == '__main__':
	logFile = open("log", "ab")
	folder = "NoticiasClarin"
	for filename in os.listdir(folder):
		noticias = open(os.path.join(folder, filename), "rb");
		contenido = noticias.read();
		noticias.close()
		noticias = open(os.path.join(folder, filename), "wb");

	logFile.close()