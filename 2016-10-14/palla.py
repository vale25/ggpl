from pyplasm import *

b = CUBOID([1,2,3])
for i in range(1, 10):
	b = STRUCT([b,T(1)(4.0),b])
VIEW(b)
