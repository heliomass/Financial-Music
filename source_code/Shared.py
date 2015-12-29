###################################
#       - Financial Music -       #
#  Implementation Shared Library  #
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

import sys
import math
from copy import copy

from Settings import *

import AccountReader
import PlayMusic


# Function to prepare the accounts and return a list of pairs.
# If an error occurs, an empty list is returned.
def prepareAccounts():

	# Parse the command line parameters
	argv = sys.argv

	# Read in the accounts as an object
	if len( argv ) == 3:
		accountRaw = AccountReader.newAccountReader( argv[1], argv[2] )
	elif len( argv ) == 2:
		argvA = argv[1] + '1.csv'
		argvB = argv[1] + '2.csv'
		accountRaw = AccountReader.newAccountReader( argvA, argvB )
	else:
		accountRaw = AccountReader.newAccountReader()
	
	# Check that the account sheet balances
	#if not ( accountRaw.checkBalance( accountRaw.getColumn1() ) and accountRaw.checkBalance( accountRaw.getColumn2() ) ):
	#	return []
	
	# Read the account data into workable lists
	account1 = []
	for i in accountRaw.getColumn1():
		account1.append( i )
		
	account2 = []
	for i in accountRaw.getColumn2():
		account2.append( i )
	
	# Collate the accounts into a list of pairs, for easy comparison between values
	accounts = []
	for i in range( len( account1 ) ):
		current = account1[i], account2[i]
		accounts.append( current )

	# Finally, return the account data, properly formatted
	return accounts

	
# This function generates a list of signals from two accounts.
# The accounts are expected to be inputted as a list of pairs
def generateSignals( accounts ):
	
	# The list of signals:
	signals = []
	
	# Create ratios for each of the account elements
	counter = 0
	for currentAccount in accounts:
		if counter in [0, 1, 4]:
			newSignal = float( currentAccount[1] ) / float( currentAccount[0] )
		else:
			newSignal = float( currentAccount[0] ) / float( currentAccount[1] )
		signals.append( newSignal )
		counter = counter + 1
		
	# Finally, return the list of signals
	return signals
	

# Function to return the difference between two signals
def getDifference( signalA, signalB ):
	
	if signalA > signalB:
		difference = signalA - signalB
	elif signalA < signalB:
		difference = signalB - signalA
	else:
		difference = 0
		
	return difference

	
# Function to order the signals from most relevant to least relevant
def orderSignals( signals, referenceSignal ):

	signalsCopy = copy( signals )

	orderedSignals = []
	while len( signalsCopy ) > 0:
		currentBest = signalsCopy[0]
		for currentSignal in signalsCopy:
			if getDifference( currentSignal, 1.0 ) >= getDifference( currentBest, 1.0 ):
				currentBest = currentSignal
		orderedSignals.append( currentBest )
		signalsCopy.remove( currentBest )

	print orderedSignals
		
	# Encode the signal order
	signalOrderEncoding = []
	for currentSignal in signals:
		signalOrderEncoding.append( orderedSignals.index( currentSignal ) )
	
	return signalOrderEncoding

	
# Function to output the name of a note from a note value
def getNoteName( noteValue ):
	
	notes = ['c', 'cS', 'd', 'dS', 'e', 'f', 'fS', 'g', 'gS', 'a', 'aS', 'b']
	
	noteName = notes[noteValue % 12]
	
	return noteName
	
	
# Function to send the generated musical sequences over to the
# Java class PlayMusic
def playMusic( musicalSequences, tempo, sequencing, instrumentScheme ):

	# Check that musicalSequences is in the correct format
	formatCheck = 1
	for i in musicalSequences:
		for j in i:
			if type(j) != int:
				formatCheck = 0
				
	# If the format was good, we can pass it to Java to play
	if formatCheck:
		print musicalSequences
		PlayMusic.playMusicDirect( musicalSequences, tempo, instrumentScheme )
		
	else:
		print "Could not play music, as input was not in the correct format."
				
	return formatCheck


# Dumps the music to a CSV file
def dumpToFile( musicalSequences, tempo, sequencing, instrumentScheme ):
	
	# Check that musicalSequences is in the correct format
	formatCheck = 1
	for i in musicalSequences:
		for j in i:
			if type(j) != int:
				formatCheck = 0

	# If the format was good, we can write it
	if formatCheck:
		file = open( 'music_output.csv', 'w' )
		
		# Write the tempo first
		file.write( str ( tempo ) )
		file.write( "\n" )
		
		# Next write the instrument scheme
		file.write( str ( instrumentScheme ) )
		file.write( "\n" )
		
		# Now write the music
		for currentSequence in musicalSequences:
			for currentNote in currentSequence:
				file.write( str( currentNote ) )
				file.write( "," )
			if sequencing:
				file.write( "\n" )
			
		file.close()
		
	else:
		print "Could not play music, as input was not in the correct format."
				
	return formatCheck
	

# Outputs the music either to a CSV file or directly to the PlayMusic class
def outputMusic ( musicalSequences, tempo, sequencing, instrumentScheme = 1 ):

	if MUSIC_OUTPUT:
		formatCheck = playMusic( musicalSequences, tempo, sequencing, instrumentScheme )
	else:
		formatCheck = dumpToFile( musicalSequences, tempo, sequencing, instrumentScheme )
		
	return formatCheck
	
	
# Tree data structure
class Node:
    def __init__(self):
        self.nodeList = []
    def addNode(self, newNode):
        self.nodeList.append(newNode)
    def traverse(self):
        result = []
        for i in self.nodeList:
            result.append(i.traverse())
        return result