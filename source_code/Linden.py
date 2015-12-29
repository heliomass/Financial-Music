###################################
#                                 #
#     - L-System  Framework -     #
#                                 #
#        - Daniel  Demby -        #
#                                 #
###################################

import math
from copy import copy

# Formally defined L-System:
#
# V = set of replaceable variables
# S = set of non-replaceable variables
# w = start axiom
# P = set of production rules

# Reserved symbols (used for stack operations)
reservedSymbols = ['[', ']']

# Produce an L-System instance
# Returns a validated L-System, or an empty tuple if the L-System is invalid
# WARNING: Be sure to use strings, even for digits!
def getLSystem( V, S, w, P ):

	valid = 1

	# Check types are correct:
	if not( type( V ) == list ):
		print "L-System Error: V is not a list."
		valid = 0
	if not( type( S ) == list ):
		print "L-System Error: S is not a list."
		valid = 0
	if not( type( w ) == list ):
		print "L-System Error: w is not a list."
		valid = 0
	if not( type( P ) == list ):
		print "L-System Error: P is not a list."
		valid = 0
	if not( valid ):
		return ()

	# Check that V is not empty
	if V == []:
		print "L-System Error: No replaceable symbols were provided."
		return ()
		
	# Check that items of V and S are mutually exclusive
	for currentSymbol in V:
		if currentSymbol in S:
			print "L-System Error: Symbols in S and V must be mutually exclusive"
			return()
		
	# Check that no reserved symbols are being used
	for currentSymbol in V:
		if currentSymbol in reservedSymbols:
			print "L-System Error: You cannot use reserved symbols in V."
			return ()
	for currentSymbol in S:
		if currentSymbol in reservedSymbols:
			print "L-System Error: You cannot use reserved symbols in S."
			return ()
			
	# Now, add the reserved symbols to S before checking the contents of w
	S = S + reservedSymbols
		
	# Check that symbols are correct
	for currentSymbol in w:
		if not( currentSymbol in V ) and not( currentSymbol in S ):
			print "L-System Error: Start axiom contains members not in V or S."
			return ()
			
	# Check rules have been supplied
	if P == []:
		print "L-System Error: No rules were supplied."
		return ()
		
	# Check rules are in correct format
	for currentRule in P:
		if not( type( currentRule ) == tuple ):
			print "L-System Error: Rules are not given in the correct format."
			return ()
		elif not( len( currentRule ) == 2 ):
			print "L-System Error: Rules are not given in the correct format."
			return()
			
	# Check that rules replace only items in V
	for currentRule in P:
		if not( currentRule[0] in V ):
			print "L-System Error: Rules can only replace items in V."
			return ()
	
	return ( V, S, w, P )


# Run one application of the rules in the l system.
def runLSystem( lSystem ):

	# Members of the L-System
	V = lSystem[0]
	S = lSystem[1]
	w = lSystem[2]
	P = lSystem[3]
	
	# This will be the new axiom after the rules are applied to w
	newW = []
	
	# Iterate through each symbol in w
	for currentSymbol in w:
	
		newSymbol = currentSymbol
	
		# Iterate through each rule in P
		for currentRule in P:
		
			if currentSymbol in currentRule[0]:
				newSymbol = currentRule[1]
				
		# Add the new symbol to the list of new symbols
		newW = newW + list( newSymbol )
		
	return ( V, S, newW, P )
	
	
# Returns just the axiom from an L-System instance
def getAxiom( lSystem ):

	w = lSystem[2]
	
	return w
	

# Prints the L-System defination neatly on the screen
def displayLSystem( lSystem ):

	print "V =", lSystem[0]
	print "S =", lSystem[1]
	print "w =", lSystem[2]
	print "P =", lSystem[3]
	
	
##### Test functions below this point ####################

# Displays the first n Fibonacci Numbers
def displayFibonacci( n ):

	# Formal L-System definition for the Fibonacci Sequence
	V = ['A', 'B']
	S = []
	w = ['A']
	P = [('A', 'B'), ('B', 'AB')]
	
	# Initialise L-System
	fibonacciLSystem = getLSystem( V, S, w, P )
	
	# Apply the rules of the L-System n times
	for i in range( n ):
		
		# Apply the rules here!
		fibonacciLSystem = runLSystem( fibonacciLSystem )
		
		# Display the current length of the axiom. This will be the
		# Fibonacci number for n.
		print "n=", i, "\t: ", len (getAxiom( fibonacciLSystem ) )
