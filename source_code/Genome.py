###################################
#       - Financial Music -       #
# Genome Approach  Implementation #
#                                 #
#        - Daniel  Demby -        #
###################################
#  *Important Note* This file is  #
#  intended to be  compiled with  #
#  Jython 2.2  for Java 1.6.  It  #
#  will not  work with  standard  #
#  Python, and will also require  #
#  access  to   associated  Java  #
#  classes used for this project. #
###################################

from random import randrange
from copy import copy
from copy import deepcopy
from Shared import *
from Settings import *

# Static values
F_MAX = 4
W1_MAX = 4
W2_MAX = 3

# The weight multiplier
WEIGHT_MULTIPLIER = 1.5


# Godel numbering function
def godel( a, b, c, d ):
    return int( float(2 ** a) * float(3 ** b) * float(5 ** c) * float(7 ** d) )
    
def godelFromGene( encodedGene ):
	return godel( encodedGene[0], encodedGene[1], encodedGene[2], encodedGene[3] )

# Function to display the genome
def displayGenome( GN ):
	if len ( GN ) == 0:
		print "No genes found."
	else:
		for gene in GN:
			print gene, "\t: ", GN[gene]


# Generate the set of all possible genes
def generateGenes( F_SET, W1_SET, W2_SET, W3_SET ):
	GN = {}
	for F in F_SET[1:]:
	    for W1 in W1_SET:
	        for W2 in W2_SET:
	        	for W3 in W3_SET:
					GN[godel( F_SET.index( F ), W1_SET.index( W1 ), W2_SET.index( W2 ), W3_SET.index( W3 ) )] = [F, [W1, W2, W3]]
	return GN

	
# Generate the set of all valid genes (ie, those with valid musical sequences)
def getValidGenes( GN, W_VALID ):

	validCombinations = []
	for current in W_VALID:
		for i in current[0]:
			for j in current[1]:
				for k in current[2]:
					validCombinations.append([i, j, k])
	print validCombinations
			
	GN_VALID = {}
	for gene in GN:
		if GN[gene][1] in validCombinations:
			GN_VALID[gene] = GN[gene]
			
	return GN_VALID
	
	
# Produce a random set of genes with n members
def getRandomGeneSet( n, GN_VALID ):
	
	randomGenes = []
	
	for i in range( n ):
		geneIndex = 0
		while not geneIndex in GN_VALID:
			geneIndex = godel( randrange( len( F_SET ) ), randrange( len( W1_SET ) ), randrange( len( W2_SET ) ), randrange( len( W3_SET ) ) )
		print geneIndex
		randomGene = GN_VALID[geneIndex]
		randomGenes.append( randomGene )
		
	return randomGenes

	
# Generates an encoding for a gene
def generateEncoding( gene ):

	F_ENCODE = F_SET.index( gene[0] )
	W1_ENCODE = W1_SET.index( gene[1][0] )
	W2_ENCODE = W2_SET.index( gene[1][1] )
	W3_ENCODE = W3_SET.index( gene[1][2] )
	
	encoding = [ F_ENCODE, W1_ENCODE, W2_ENCODE, W3_ENCODE ]
	
	return encoding
	
	
# Generates encodings for a set of genes
def generateEncodings( genes ):

	encodings = []
	
	for gene in genes:
		encodings.append( generateEncoding( gene ) )
		
	return encodings
	
	
# Decodes a gene
def decodeGene( encoding ):

	gene = []
	
	gene.append( F_SET[encoding[0]] )
	
	musicAttributes = []
	musicAttributes.append( W1_SET[encoding[1]] )
	musicAttributes.append( W2_SET[encoding[2]] )
	musicAttributes.append( W3_SET[encoding[3]] )
	
	gene.append( musicAttributes )

	return gene
	
	
# Decodes several genes
def decodeGenes( encodings ):

	genes = []
	
	for code in encodings:
		decodedGene = decodeGene( code )
		genes.append( decodedGene )
		
	return genes
	
	
# Performs an single-random-gene new-allele mutation given an encoding
def mutateGene( gene, validGenes ):
	
	mutatedGene = copy( gene )
	while mutatedGene == gene:
	
		mutatedGeneCandidate = [0, 0, 0, 0]
		while not godelFromGene( mutatedGeneCandidate ) in GN_VALID:
	
			mutatedGeneCandidate = deepcopy( mutatedGene )
		
			# Choose the random allele
			alleleIndex = randrange( len ( gene ) )
			
			# Mutate this allele
			if alleleIndex == 0:
				mutatedGeneCandidate[0] = randrange( len ( F_SET ) )
			elif alleleIndex == 1:
				mutatedGeneCandidate[1] = randrange( len ( W1_SET ) )
			elif alleleIndex == 2:
				mutatedGeneCandidate[2] = randrange( len ( W2_SET ) )
			elif alleleIndex == 3:
				mutatedGeneCandidate[3] = randrange( len ( W3_SET ) )
				
		mutatedGene = deepcopy( mutatedGeneCandidate )
				
	return mutatedGene
	

# Performs an m-random-gene new-allele mutation on a set of genes
def mutateGeneSet( genes, m, validGenes ):

	mutatedGenes = deepcopy( genes )
	
	for i in range( m ):
	
		geneIndex = randrange( len ( genes ) )
		mutatedGenes[geneIndex] = mutateGene( mutatedGenes[geneIndex], validGenes )
		
	return mutatedGenes
	
	
# The weight multiplier
WEIGHT_MULTIPLIER = 1.5
	
# Generate evenly distributed weights for a genome
def generateGenomeWeights( genome ):

	weights = {}
	
	for gene in genome:
		weights[gene] = 1.0
		
	return weights
	
	
# Increase the weight of a gene
def increaseWeight( encodedGene, weights ):

	print encodedGene
	geneID = godelFromGene( encodedGene )
	weights[geneID] = weights[geneID] * WEIGHT_MULTIPLIER


#### Place test functions below this point ##############################################	


GN = generateGenes( F_SET, W1_SET, W2_SET, W3_SET )
displayGenome( GN )

print "\n=====================\n"

GN_VALID = getValidGenes( GN, W_VALID )
displayGenome( GN_VALID )
print len( GN_VALID ), " out of ", len( GN ), " genes are valid."

print "\n=====================\n"

print "Random genes:"
randomGenes = getRandomGeneSet( 5, GN_VALID )
for ff in randomGenes: print ff

print "\n=====================\n"
print "Encoding of random genes:"
encodingg = generateEncodings( randomGenes )
for ff in encodingg: print ff

print "\n=====================\n"
print "Encoding of mutated random genes:"
mutatedEncoding = mutateGeneSet( encodingg, 20, GN_VALID )
for ff in mutatedEncoding: print ff

print "\n=====================\n"
print "Mutated genes:"
decodedGenes = decodeGenes( mutatedEncoding )
for ff in decodedGenes: print ff

print "\n=====================\n"
print "Weight of genes:"
wei = generateGenomeWeights( GN_VALID )
print len( wei ), " ... ", wei

print "\n=====================\n"
print "New weights of genes:"
increaseWeight( mutatedEncoding[0], wei )
print wei