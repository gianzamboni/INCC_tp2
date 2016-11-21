import scrapy
import os
import pickle
import json


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

		prefijo = "http://www.clarin.com/archivo/pager.json?date={0}&page={1}"
		while(date != "20161121"):
	 		links.append(prefijo.format(date, page)		)
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

class ClarinSpider(scrapy.Spider):
    name = "clarin"
    allowed_domains = ["clarin.com"]
    start_urls = todasLasFechas()

    def start_request():
    	return [scrapy.FormRequest()]

    def parse(self, response):
        noticias = json.loads(response.body_as_unicode())
        splittedUrl = response.url.split("=")
        filename = "paginas/" + splittedUrl[-2] +  "." + splittedUrl[-1]
        counter = int(splittedUrl[-1])
        if(noticias['news'] != ""):
        	splittedUrl[-1] = str(counter + 1)
        	finalUrl = "".join(splittedUrl)
        	start_urls.append(finalUrl)

        with open(filename, 'wb') as f:
            f.write(noticias.encode("utf-8"))