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

		prefijo = "http://www.clarin.com/ediciones-anteriores/"
		while(date != "20161121"):
	 		links.append(prefijo + date)
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

if __name__ == "__main__":
	todasLasFechas();
