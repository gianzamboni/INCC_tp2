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

class ClarinSpider(scrapy.Spider):
    name = "clarin"
    allowed_domains = ["clarin.com"]
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
