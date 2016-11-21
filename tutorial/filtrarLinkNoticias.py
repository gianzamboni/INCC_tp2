import os
import json
from bs4 import BeautifulSoup

def filtrarNoticias():
	directory = "paginas/"
	totalLinks = []
	prefijo = "https://www.clarin.com"
	for filename in os.listdir(directory):
		f = open(directory + filename, "rb")
		page = json.load(f)
		news = page['news']
		htmlParseado = BeautifulSoup(news, 'html.parser')
		links = [ x.get('href') for x in htmlParseado.find_all('a') if x.get('href') != '']

		for link in links:
			splittedLink = link.split("/")
			if(splittedLink[1] == "ieco" or splittedLink[1] == "politica" or splittedLink[1] == "opinion" or splittedLink[1] == "sociedad"):
				if(link[-1] == "l"):
					totalLinks.append(prefijo + link + "\n")

	contenido = "".join(totalLinks)

	newLinksFile = open("linksNoticias", "wb")
	newLinksFile.write(contenido)

if __name__ == "__main__":
	filtrarNoticias()