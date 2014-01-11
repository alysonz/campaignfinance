names = open("namesConsolidated.txt","r")
namesFormat = open("namesFormat.txt","w")
for line in names:
	items = line.split("|")
	line = "|".join(items)
	line = line.rstrip()
	namesFormat.write("%s\n" % (line))
