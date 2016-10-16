from pyplasm import *
from larlib import *

def structureFrame(beamDimensions, pillarDimensions, pillarDistances, beamDistances):
	""" 
	Creates a space frame of reinforced concrete including beams, pillars and footings
	:param beamDimensions: dimensions of beam section
	:param pillarDimensions: dimensions of pillar section
	:param pillarDistances: distances between axes of the pillars
	:param beamDistances: interstory heights
	:return: an HPC object
	"""

	(px, py) = pillarDimensions
	(bx, bz) = beamDimensions
	
	# PILLARS

	pillarY = []
	pillarZ = []

	for i in range(0, len(pillarDistances)):
		pillarY.extend([py, -pillarDistances[i]])

	pillarBase = PROD([QUOTE([px]), QUOTE(pillarY)])
	
	for i in range(0, len(beamDistances)):
		pillarZ.extend([beamDistances[i], -bz])

	pillars = PROD([pillarBase, QUOTE(pillarZ)])

	# BEAMS

	beamY = []
	beamZ = []

	for i in range(0, len(beamDistances)):
		beamZ.extend([-beamDistances[i], bz])

	for i in range(0, len(pillarDistances)-1):
		if i==0 or i==len(pillarDistances)-2:
			print(pillarDistances[i])
			beamY.append(pillarDistances[i]+py*3/2.0)
		else:
			beamY.append(pillarDistances[i]+py)
			print(pillarDistances[i])

	beamBase = PROD([QUOTE([bx]), QUOTE(beamY)])

	beams = PROD([beamBase, QUOTE(beamZ)])

	structure = STRUCT([pillars, beams])
	return structure

if __name__ == "__main__":
	s = structureFrame([1,1], [1,2], [3,6,2,3,6,8], [4,3,2,5,7,2])
	VIEW(s)