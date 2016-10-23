from pyplasm import *
from larlib import *
import csv
import workshop_01

def ggpl_bone_structure(file_name):
	""" 
	creates a reinforced concrete structure
	:param file_name: csv file that provides values for the constructions of the structure
	:return: an HPC object
	"""
	beamDim = []
	pillarDim = []
	beamDist = []
	pillarDist = []
	frameDistancesX = []
	frameDistancesY = []
	frameDistancesZ = []

	# reads values from the csv file and put them into lists

	with open(file_name, 'r') as f:
		readerEven = csv.reader(f, delimiter=';', quotechar=',')
		for i, row in enumerate(readerEven):
			if (i+1)%2.0==0:
				beamDim.append((row[0].split(",")))
				pillarDim.append((row[1].split(",")))
				beamDist.append((row[2].split(",")))
				pillarDist.append((row[3].split(",")))
		
	with open(file_name, 'r') as f:
		readerOdd = csv.reader(f, delimiter=',')
		for i, row in enumerate(readerOdd):
			if (i+1)%2.0!=0:
				frameDistancesX.append(float(row[0]))
				frameDistancesY.append(float(row[1]))
				frameDistancesZ.append(float(row[2]))	

	# creates new lists and casts values from string to float 

	beamDimensions = []
	pillarDimensions = []
	beamDistances = []
	pillarDistances = []

	for i in range(0, len(beamDim)):
		beamDimensions.extend([(float(beamDim[i][0]), float(beamDim[i][1]))])

	for i in range(0, len(pillarDim)):
		pillarDimensions.extend([(float(pillarDim[i][0]), float(pillarDim[i][1]))])

	for i in range(0, len(beamDist)):
		beamDistances.append([])
		for j in range(0, len(beamDist[i])):
			beamDistances[i].extend([float(beamDist[i][j])])

	for i in range(0, len(pillarDist)):
		pillarDistances.append([])
		for j in range(0, len(pillarDist[i])):
			pillarDistances[i].extend([float(pillarDist[i][j])])
	
	# creates frames using an existing function from the previous workshop

	frames = [workshop_01.structureFrame(beamDimensions[0], pillarDimensions[0], beamDistances[0], pillarDistances[0])]
	for i in range(1, len(frameDistancesX)):
		frames.extend([T(1)(frameDistancesX[i-1]), workshop_01.structureFrame(beamDimensions[i], pillarDimensions[i], beamDistances[i], pillarDistances[i])])
	frames = STRUCT(frames)

	# creates beams between two frames

	def createBeams(x, dimensions, distancesY, distancesZ):
		beamsX = []
		beamsY = []
		beamsZ = []
		(y,z) = dimensions
		# Y
		for i in range(0, len(distancesY)):
			beamsY.extend([y, -distancesY[i]])

		for i in range(0, len(distancesZ)):
			beamsZ.extend([-distancesZ[i], z])

		beamsX.extend([-y, x])

		base = PROD([QUOTE(beamsX), QUOTE(beamsY)])

		beams = PROD([base, QUOTE(beamsZ)])
		return beams

	# creates beams between every frame

	xBeams = [createBeams(frameDistancesX[0], beamDimensions[0], pillarDistances[0], beamDistances[0])]

	for i in range(1, len(frameDistancesX)-1):
		xBeams.extend([T(1)(frameDistancesX[i-1]), createBeams(frameDistancesX[i], beamDimensions[i], pillarDistances[i], beamDistances[i])])
	xBeams = STRUCT(xBeams)

	final = STRUCT([frames, xBeams])
	return final


if __name__ == "__main__":
	s = ggpl_bone_structure("frame_data_448429.csv")
	VIEW(s)