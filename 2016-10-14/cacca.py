#def readParameters(file_name):
import csv
with open('provetta.csv', 'rb') as f:
	reader = csv.reader(f, delimiter=';', quotechar=',')
	for i, row in enumerate(reader):
		#print i
		if (i+1)%2.0==0:
			#print row[0]
			#print row[3]
			pillarSec = row[0]
			beamSec = row[1]
			pillarDistY = row[2]
			pillarDistX = row[3]
		else:
			for i in row:
				#print "ok"
				beamDistY.append(i)