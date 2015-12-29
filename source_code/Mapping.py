###################################
#       - Financial Music -       #
# Mapping Approach Implementation #
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

import math
from copy import copy

from Shared import *

# The signal bounds
signalBounds = 0.0, 1.5

# Tempo ranges
minTempo = 40
maxTempo = 240



# Static values. These values should not be tweaked!
BOUNDS_LOWER = 0
BOUNDS_UPPER = 1
SIGNAL_RANGE = signalBounds[BOUNDS_UPPER] - signalBounds[BOUNDS_LOWER]
TEMPO_RANGE = maxTempo - minTempo


# The next section of this code is concerned with defining the various signal processors
# used.

# Tempo signal processor.
# Note that in keeping with MIDI standards, a tempo will range somewhere between 40 and 240.
# Also, tempo will never have a processor skin applied to it
	
def signalProcessorTempo( signal ):
	
	tempo = int( abs( 100 - ( 100 / signal ) ) * TEMPO_SPEEDUP ) + 100
	
	if tempo > 240:
		tempo = 240
	elif tempo < 40:
		tempo = 40
		
	print tempo, "bpm"

	return tempo


# Statics to talk about major and minor keys
KEY_MAJOR = 0
KEY_MINOR = 1

def getOverallKey( signal ):

	if signal > 1.0:
		key = OCTAVE_MAJOR
		print signal, " : Major"
	else:
		key = OCTAVE_MINOR
		print signal, " : Minor"
	
	return key


# Key signal processor.
# Chooses the key based on the signal. As there are 12 notes in an octive
# (including accidentals), our output value will be between 0 and 11.
def signalProcessorKey( signal, referenceSignal ):
	
	# Choose the starting note of the key
	if signal <= signalBounds[BOUNDS_LOWER]:
		keyNote = 0
		
	elif signal >= signalBounds[BOUNDS_UPPER]:
		keyNote = 12
		
	else:
		signal = signal - signalBounds[BOUNDS_LOWER]
		keyNote = int( ( signal / SIGNAL_RANGE ) * 12 )
	
	# Choose whether the key will be major or minor
	if signal < referenceSignal:
		keySig = KEY_MINOR
	else:
		keySig = KEY_MAJOR
	
	return ( keyNote, keySig )


# This combines a set of signals into one
def signalCombinator( signals ):
	
	numberOfSignals = len( signals )
	signalCombinator = sum( signals )
	
	combinedSignal = signalCombinator / numberOfSignals
	
	return combinedSignal


# Produces a sequence of notes from a signal
def signalProcessorSequence( signal, referenceSignal, signalPriority ):
	
	# Get a signal variance against the reference signal
	if ( signal - referenceSignal ) > 0:
		signalVariance = signal - referenceSignal
	else:
		signalVariance = referenceSignal - signal
		
	# Check the variance against the scale cut of point
	if signalVariance <= CUT_OFF_SCALE:
		print "scale\t",
		musicalSequence = signalProcessorScale( signal, signalVariance, signalPriority, referenceSignal )
	elif signalVariance <= CUT_OFF_ARPEGGIO:
		print "arpeggio\t",
		musicalSequence = signalProcessorArpeggio( signal, signalVariance, signalPriority, referenceSignal )
	else:
		musicalSequence = signalProcessorBrokenChord( signal, signalVariance, signalPriority, referenceSignal )
		print "broken chord\t",
		
	# Return the musical sequence
	return musicalSequence



# Function to choose a start note within a max and min bounds
def getStartingNote( signalVariance, cutOff, signalPriority ):

	if signalVariance > 8.0:
		startNote = int( signalVariance / 12.0 ) % 12
	else:
		startNote = int( 12.0 / signalVariance ) % 12
		
	print "\n", startNote, " ",
		
	startNote = 20 + startNote + ( getStartingOctave( signalPriority ) * 12 )
	
	print getStartingOctave( signalPriority ), " ", startNote, " ",

	return startNote
	

# Function to choose an octave based on the signal's priority	
def getStartingOctave( signalPriority ):

	if signalPriority == 0:
		startOctave = 2
	elif signalPriority == 1:
		startOctave = 1
	elif signalPriority == 2:
		startOctave = 3
	elif signalPriority == 3:
		startOctave = 0
	elif signalPriority == 4:
		startOctave = 4
	elif signalPriority == 5:
		startOctave = -1

	return startOctave


# Scale templates
SCALE_MAJOR = [0, 2, 4, 5, 7, 9, 11, 12]
SCALE_MINOR = [0, 2, 3, 5, 7, 9, 10, 12]


# Produces a scale from a signal
def signalProcessorScale( signal, signalVariance, signalPriority, referenceSignal ):
	
	# Calculate the starting note for the scale
	startNote = getStartingNote( signalVariance, CUT_OFF_SCALE, signalPriority )
	
	# Produce a sequence of notes in a major scale from the start note for one octave
	scale = []
	if referenceSignal < 1.0:
		currentKey = SCALE_MINOR
	else:
		currentKey = SCALE_MAJOR
	for i in range( len ( currentKey ) ):
		scale.append( startNote + currentKey[i] )
		
	# Calculate whether the scale is ascending, or descending
	if signal < 1.0:
		scale.reverse()
	
	# return musicalSequence
	return scale


# Arpeggio templates
ARPEGGIO_MAJOR = [0, 4, 7, 12, 16, 19, 24]
ARPEGGIO_MINOR = [0, 3, 7, 12, 15, 19, 24]


# Produces an arpeggio from a signal
def signalProcessorArpeggio( signal, signalVariance, signalPriority, referenceSignal ):
	
	# Calculate the starting note for the arpeggio
	startNote = getStartingNote( signalVariance, CUT_OFF_ARPEGGIO, signalPriority )
	
	# Produce a sequence of notes in a major arpeggio from the start note for one octave
	arpeggio = []
	if referenceSignal < 1.0:
		currentKey = ARPEGGIO_MINOR
	else:
		currentKey = ARPEGGIO_MAJOR
	for i in range( len ( currentKey ) ):
		arpeggio.append( startNote + currentKey[i] )
		
	# Calculate whether the scale is ascending, or descending
	if signal < 1.0:
		arpeggio.reverse()
		
	# return musicalSequence
	return arpeggio


# Broken chord templates
BROKENCHORD_MAJOR = [0, 4, 7, 12, 4, 7, 12, 16, 7, 12, 16, 19, 12, 16, 19, 24]
BROKENCHORD_MINOR = [0, 3, 7, 12, 3, 7, 12, 15, 7, 12, 15, 19, 12, 15, 19, 24]

# Produces a broken chord from a signal
def signalProcessorBrokenChord( signal, signalVariance, signalPriority, referenceSignal ):
	
	# Calculate the starting note for the broken chord
	startNote = getStartingNote( signalVariance, CUT_OFF_BROKENCHORD, signalPriority )
	
	# Produce a sequence of notes in a minor broken chord from the start note for one octave
	brokenChord = []
	if referenceSignal < 1.0:
		currentKey = BROKENCHORD_MINOR
	else:
		currentKey = BROKENCHORD_MAJOR
	for i in range( len( currentKey ) ):
		brokenChord.append( startNote + currentKey[i] )
	
	# Calculate whether the scale is ascending, or descending
	if signal < 1.0:
		brokenChord.reverse()
		
	# return musicalSequence
	return brokenChord


# Template for notes in the octave of a generic key
OCTAVE_MAJOR = [0, 2, 4, 5, 7, 9, 11]
OCTAVE_MINOR = [0, 2, 3, 5, 7, 9, 10]

# Function to produce a complete scale for 12 octives
def createFullScale( octaveTemplate ):
	
	allNotes = []
	for i in range( 7 ):
		for currentNote in octaveTemplate:
			allNotes.append( ( currentNote + ( i * 12 ) ) + 24 )
			
	return allNotes


# Function to shift the key
def shiftKey( octaveTemplate, keyShift ):
	
	shiftedOctave = []
	for currentNote in octaveTemplate:
		shiftedOctave.append( ( currentNote + keyShift ) % 12 )
		
	shiftedOctave.sort()
		
	return shiftedOctave


# Function to produce a map of notes for a given key
def getKeyMap( octaveTemplate, keyShift ):
	
	keyMap = createFullScale( shiftKey( octaveTemplate, keyShift ) )
	
	return keyMap


# Function to force a note sequence to map its self to a keyMap
def mapToKey( musicalSequence, keyMap ):
	
	newMusicalSequence = []
	for currentNote in musicalSequence:
		newNote = currentNote
		while not( newNote in keyMap ):
			if ( newNote - 1 ) in keyMap:
				newNote = newNote - 1
			else:
				newNote = newNote + 1
		newMusicalSequence.append( newNote )
	
	return newMusicalSequence
	

# Main method
def main():

	# Read in files to get account details
	accounts = prepareAccounts()
	
	# Generate signals from accounts
	signals = generateSignals( accounts )
	
	# Generate a refernce signal via the combinator
	referenceSignal = signalCombinator( signals )
	
	# Use the reference signal to calculate the tempo
	tempo = signalProcessorTempo( referenceSignal )
	
	# Work out the key that the output will be in
	keySig = getOverallKey( referenceSignal )
	
	# Get an encoding for the signal priorities
	orderedSignalEncoding = orderSignals( signals, referenceSignal )
	
	# Create an empty list of musical sequences
	musicalSequences = []
	
	# Add a musical sequence for each signal
	for currentSignal in signals:
		signalPriority = orderedSignalEncoding[signals.index( currentSignal )]
		if currentSignal < 1.0:
			print ""
		musicalSequences.append( signalProcessorSequence( currentSignal, referenceSignal, signalPriority ) )
		
		
	# Force all musical sequences into the same key
	# if we are playing in parallel rather than in sequence
	if MUSIC_SEQUENCING:
		keyMap = getKeyMap( keySig, 0 )
		newMusicalSequences = []
		print keyMap
		for currentSequence in musicalSequences:
			print currentSequence
			currentSequence = mapToKey( currentSequence, keyMap )
			newMusicalSequences.append( currentSequence )
			print currentSequence, "\n\n"
		musicalSequences = newMusicalSequences
		
	# Otherwise, put each sequence into its own key
	#else:
	#	for currentSequence un musicalSequences:
	#		print currentSequence
	#		currentKeyMap = getKeyMap( keySig, 0 )
	#		print currentSequence, "\n\n"
		
	# Output the list of musical sequences
	outputMusic( musicalSequences, tempo, MUSIC_SEQUENCING, instrumentSet )
	
	print musicalSequences
	
	print "\n"
	

# Main execution code
if __name__ == "__main__":
	main()
	

#### Place test functions below this point ##############################################


def test():
	
	#testSequence = [x+24 for x in SCALE_MAJOR]
	#testSequence2 = [x+24 for x in BROKENCHORD_MAJOR]
	#	
	#a = getKeyMap( OCTAVE_MAJOR, 1 )
	#print a
	#
	#print testSequence2
	#	
	#b = mapToKey( testSequence2, a )
	#print b

	a = [78, 79, 102, 98, 97, 96]
	b = [a]
	#c = playMusic( b )
	#PlayMusic.playMusicDirect(b)
	
	#PlayMusic.test(b)
	
	#SoundTester.go()
	
	c = dumpToFile( b )


# Produce a list of signals
def testSignals():
	
	# Generate some signals from the account
	signals = generateSignals( prepareAccounts() )
	print signals
	
	# Generate a reference signal
	referenceSignal = signalCombinator(signals)
	
	# Generate some musical sequence from this signal, and print them to screen
	for currentSignal in signals:
		currentSequence = signalProcessorSequence( currentSignal, referenceSignal )
		print currentSequence

a = [4.2, 7.3, 0.01, 2.6, 0.3, 0.7, 0.6]

def testKeyShift():

	b = createFullScale( OCTAVE_MAJOR )
	c = [50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
	
	d = mapToKey( c, b )
	
	print c
	print "\n"
	print d


def testDif():

	e = prepareAccounts()
	print e
	print "\n"
	
	f = getRateOfChange( e )
	print f



