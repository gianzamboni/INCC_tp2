# -*- coding: utf-8 -*-

import scrapy
import os
import pickle
import json
from bs4 import BeautifulSoup

def todasLasFechas():

	links = []

	if os.path.isfile("listaLinks"):
		linksFile = open("listaLinks", "rb")
		links = pickle.load(linksFile)
		linksFile.close()
	else:
		date = "20140702"
		year = int(date[0:4])
		month = int(date[4:6])
		day = int(date[6:8])

		prefijo = "http://www.clarin.com/archivo/pager.json?date={0}&page=1"
		while(date != "20161121"):
	 		links.append(prefijo.format(date))
	 		day += 1
	 		if(day == 32):
		 		day = 1
	 			month += 1

	 		if(month == 13):
	 			month = 1
	 			year += 1

	 		date = str(year) + str(month).zfill(2) + str(day).zfill(2)
		linksFile = open("listaLinks", "wb")
		pickle.dump(links, linksFile) 	
		linksFile.close()
	return links


def todasLasFechasPagina12():
	links = []
	date = "2014-07-02"
	year = 2014
	month = 07
	day = 02
	prefijoPais = "https://www.pagina12.com.ar/diario/elpais/index-{0}.html"
	prefijoEco = "https://www.pagina12.com.ar/diario/economia/index-{0}.html"
	prefijoSoc = "https://www.pagina12.com.ar/diario/sociedad/index-{0}.html"
	while(date != "2016-11-15"):
	 	links.append(prefijoPais.format(date))
	 	links.append(prefijoEco.format(date))
	 	links.append(prefijoSoc.format(date))
	 	day += 1
	 	if(day == 32):
	 		day = 1
	 		month += 1

	 	if(month == 13):
	 		month = 1
	 		year += 1

	 	date = str(year) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2)
	linksFile = open("listaLinks", "wb")
	pickle.dump(links, linksFile) 	
	linksFile.close()
	return links

def getLinks(news):
	htmlParseado = BeautifulSoup(news, 'html.parser')
	links = [ x.get('href') for x in htmlParseado.find_all('a') if x.get('href') != '' and x.get('href')[-1] == "l"]
	prefijo = "https://www.clarin.com"
	totalLinks = []
	for link in links:
		splittedLink = link.split("/")
		if(splittedLink[1] == "ieco" or splittedLink[1] == "politica" or splittedLink[1] == "opinion" or splittedLink[1] == "sociedad"):
			totalLinks.append((prefijo + link).encode("utf-8"))

	return totalLinks

DICCFECHAS = {}

def todasLasNoticias():
	
	global DICCFECHAS
	logFile = open("log", "ab")
	folder = "listasNoticias"
	noticias = []
	for filename in os.listdir(folder):
		f = open(os.path.join(folder, filename), "rb")
		noticiasDelArchivo = pickle.load(f)
		noticias.extend(noticiasDelArchivo)
		fecha = filename.split("&")[0]
		for link in noticiasDelArchivo:
			DICCFECHAS[link.split("/")[-1]] = fecha
		f.close()
	logFile.write(str(len(noticias)) + "\n")
	logFile.close()
	return noticias;


def getText(response, url):
	logFile = open("log", "ab")
	htmlParseado = BeautifulSoup(response, 'html.parser')
	divNota = htmlParseado.find("div", { "class" : "nota" })
	quotes = divNota.find_all("p", {"style" : "text-align: right;"})
	if(quotes != []):
		for element in quotes:
			element.extract()

	contenido = divNota.text.encode('utf-8')

	meta = htmlParseado.find("div", {"class" : "breadcrumb" }).find("ul").find_all("li")
	categoria = meta[1].text.encode('utf-8')
	fecha = DICCFECHAS[url.split("/")[-1]]
	
	titulos = htmlParseado.find("h1").text.encode('utf-8')
	titulos = titulos.replace(" ", "_")
	
	filename = fecha + "_" + categoria + "_" + titulos	
	file = open("NoticiasClarin/" + filename, "wb")
	file.write(contenido)
	file.close()
	logFile.write("Archivo " + filename + " guardado\n")
	return filename


def getNewsLinks(body, url):
	logFile = open("log", "ab")

	splittedUrl = url.split("/")
	fecha = splittedUrl[-1][6:16]
	categoria = splittedUrl[-2]
	prefijo = "https://www.pagina12.com.ar"
	
	listFile = open("listasNoticiasPagina12/" + fecha + "_" + categoria, "wb")

	pagina = BeautifulSoup(body, "html.parser")
	noticias = pagina.find_all("div", { "class" : "noticia" })
	linksNoticias = [ a.get('href') for a in [ h.find("a") for h in [n.find("h2") for n in noticias] ]]
	logFile.write(str(linksNoticias))
	
	totalLinks = [ prefijo + link for link in linksNoticias]
	pickle.dump(totalLinks, listFile)

	logFile.close()
	listFile.close()

class ClarinSpider(scrapy.Spider):
    name = "clarin"
    allowed_domains = ["clarin.com", "ieco.clarin.com"]
    start_urls = todasLasFechas()

    def parse(self, response):
        noticias = json.loads(response.body[1:-1])
        splittedUrl = response.url.split("=")
        filename = "listasNoticias/" + splittedUrl[-2] +  "." + splittedUrl[-1]
        counter = int(splittedUrl[-1])
        if(noticias['news'] != ""):
        	links = getLinks(noticias['news'])
         	splittedUrl[-1] = str(counter + 1)
         	finalUrl = "=".join(splittedUrl)
         	self.start_urls.append(finalUrl)

        	with open(filename, 'wb') as f:
        		pickle.dump(links, f)

class ClarinNoticiasSpider(scrapy.Spider):
    name = "clarinNoticias"
    allowed_domains = ["clarin.com"]
    start_urls = todasLasNoticias()

    def parse(self, response):
        getText(response.body, response.url)


class pagina12Spider(scrapy.Spider):
	name = "pagina12"
	allowed_domains = ["pagina12.com.ar"]
	start_urls = todasLasFechasPagina12()

	def parse(self, response):
		getNewsLinks(response.body, response.url)