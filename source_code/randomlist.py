from random import randrange

def generateList( n ):
	
	slst = []
	for i in range( n ):
		k = randrange( n )
		while k in slst:
			k = randrange( n )
		slst.append( k )
		
	flst = []
	for j in slst:
		flst.append( j + 1 )
		
	for l in flst:
		print l
	