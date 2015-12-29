###################################
#       - Financial Music -       #
#     L-System Implementation     #
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

from Shared import *
from Linden import *
from copy import copy
from copy import deepcopy

# Overide music sequencing to ensure it's in parallel
# (NOTE: DO NOT CHANGE THIS HERE, USE Settings.py)
MUSIC_SEQUENCING = 1

# Keymaps
OCTAVE_MAJOR = [0, 2, 4, 5, 7, 9, 11]
OCTAVE_MINOR = [0, 2, 3, 5, 7, 9, 10]




def produceMusic( axiom, startNote, keyMap ):
	
	# Keeps track of the current note
	currentNote = startNote

	# Keeps track of the last chord played
	lastChord = (0, 0, 0)

	# The string of output music
	outputMusic = []
	
	# The strings of chord notes
	outputChordsA = []
	outputChordsB = []
	outputChordsC = []
	
	# Harmonising notes
	outputMusicHarmony = []
	
	# The harmony key
	harmonyKey = keyMap[2]
	
	# Boolean value that applies haromy when true
	harmonize = 0
	
	# A stack
	noteStack = []
	
	for currentChar in axiom:
	
		# Stack operations
		if currentChar == '[':
			#print '[',
			noteStack.append( ( currentNote, harmonize, keyMap ) )
		elif currentChar == ']':
			#print ']',
			if len( noteStack ) > 0:
				stackItem = noteStack.pop()
				currentNote = stackItem[0]
				harmonize = stackItem[1]
				key = stackItem[2]
			else:
				print "Warning: A pop was attempted when stack empty."
			
		# Note operations
		elif currentChar == 'u':
			#print 'u',
			currentNote = pitchUp( currentNote, keyMap )
			outputMusic.append( currentNote )
			outputMusicHarmony = appendHarmony( outputMusicHarmony, currentNote, harmonize, harmonyKey, keyMap )
			currentChord = getChord( keyMap )
			appendChord = chordComparison( currentChord, lastChord )
			outputChordsA.append( appendChord[0] )
			outputChordsB.append( appendChord[1] )
			outputChordsC.append( appendChord[2] )
			lastChord = currentChord
		elif currentChar == 'd':
			#print 'd',
			currentNote = pitchDown( currentNote, keyMap )
			outputMusic.append( currentNote )
			outputMusicHarmony = appendHarmony( outputMusicHarmony, currentNote, harmonize, harmonyKey, keyMap )
			currentChord = getChord( keyMap )
			appendChord = chordComparison( currentChord, lastChord )
			outputChordsA.append( appendChord[0] )
			outputChordsB.append( appendChord[1] )
			outputChordsC.append( appendChord[2] )
			lastChord = currentChord
		elif currentChar == '/':
			#print '/',
			currentNote = doublePitchUp( currentNote, keyMap )
			outputMusic.append( currentNote )
			outputMusicHarmony = appendHarmony( outputMusicHarmony, currentNote, harmonize, harmonyKey, keyMap )
			currentChord = getChord( keyMap )
			appendChord = chordComparison( currentChord, lastChord )
			outputChordsA.append( appendChord[0] )
			outputChordsB.append( appendChord[1] )
			outputChordsC.append( appendChord[2] )
			lastChord = currentChord
		elif currentChar == '_':
			#print '_',
			currentNote = doublePitchDown( currentNote, keyMap )
			outputMusic.append( currentNote )
			outputMusicHarmony = appendHarmony( outputMusicHarmony, currentNote, harmonize, harmonyKey, keyMap )
			currentChord = getChord( keyMap )
			appendChord = chordComparison( currentChord, lastChord )
			outputChordsA.append( appendChord[0] )
			outputChordsB.append( appendChord[1] )
			outputChordsC.append( appendChord[2] )
			lastChord = currentChord
		elif currentChar == 's':
			#print 's',
			outputMusic.append( currentNote )
			outputMusicHarmony = appendHarmony( outputMusicHarmony, currentNote, harmonize, harmonyKey, keyMap )
			currentChord = getChord( keyMap )
			appendChord = chordComparison( currentChord, lastChord )
			outputChordsA.append( appendChord[0] )
			outputChordsB.append( appendChord[1] )
			outputChordsC.append( appendChord[2] )
			lastChord = currentChord
		elif currentChar == 'r':
			#print 'r',
			outputMusic.append( currentNote + keyMap[0] )
			outputMusicHarmony = appendHarmony( outputMusicHarmony, -3, harmonize, harmonyKey, keyMap )
			currentChord = getChord( keyMap )
			appendChord = chordComparison( currentChord, lastChord )
			outputChordsA.append( appendChord[0] )
			outputChordsB.append( appendChord[1] )
			outputChordsC.append( appendChord[2] )
			lastChord = currentChord
			
		# Key operations
		elif currentChar == '.':
			#print '.',
			keyOp = keyShiftUp( keyMap, 1, currentNote )
			keyMap = keyOp[0]
			currentNote = keyOp[1]
		elif currentChar == ',':
			#print ',',
			keyOp = keyShiftDown( keyMap, 1, currentNote )
			keyMap = keyOp[0]
			currentNote = keyOp[1]
		elif currentChar == 'j':
			keyMap = keySwitchMajor( keyMap )
		elif currentChar == 'n':
			keyMap = keySwitchMinor( keyMap )
			
		# Harmony Operations
		elif currentChar == '+':
			#print '+',
			harmonize = 1
		elif currentChar == '-':
			#print '-',
			harmonize = 0
			
	#print "\n"

	# Check that stack is empty at finish
	if len( noteStack ) > 0:
		print "Warning: Stack not empty."
	
	return ( outputMusic, outputMusicHarmony, outputChordsA, outputChordsB, outputChordsC )
	
	
# Apply harmony as necessary
def appendHarmony( outputMusicHarmony, currentNote, harmonize, harmonyKey, keyMap ):
	print "appendHarmony."

	if harmonize and not( currentNote <= 0 ):
		harmonyNote = currentNote + harmonyKey
		if not harmonyNote in keyMap:
			pitchUp( harmonyNote, keyMap )
		outputMusicHarmony.append( harmonyNote )
	else:
		outputMusicHarmony.append( -3 )
		
	return outputMusicHarmony
	

# Returns the keyMap in a format that can be used by pitchUp() and pitchDown()
def getDefaultKeyMap( keyMap ):

	defaultKeyMap = []
	for currentNote in keyMap:
		defaultKeyMap.append( currentNote % 12 )
		
	return defaultKeyMap

	
# Get the next note up from the current note
def pitchUp( note, keyMap ):
	print "pitchUp.", note, keyMap
	
	keyMap = getDefaultKeyMap( keyMap )

	newNote = note + 1

	while ( newNote % 12 ) not in keyMap and newNote < 108:
		newNote = newNote + 1
		print newNote
		
	if newNote > 108:
		newNote = 108
	
	return newNote
	
	
# Get the next note down from the current note
def pitchDown( note, keyMap ):
	print "pitchDown.", note, keyMap
	
	keyMap = getDefaultKeyMap( keyMap )

	newNote = note - 1

	while ( newNote % 12 ) not in keyMap and newNote > 21:
		newNote = newNote - 1
		print newNote
		
	if newNote < 21:
		newNote = 21
	
	return newNote
	
	
# Get the second note up from the current note
def doublePitchUp( note, keyMap ):
	print "doublePitchUp.", note

	newNote = pitchUp( note, keyMap )
	newNote = pitchUp( newNote, keyMap )
	
	return newNote
	
	
# Get the second note down from the current note
def doublePitchDown( note, keyMap ):
	print "doublePitchDown.", note

	newNote = pitchDown( note, keyMap )
	newNote = pitchDown( newNote, keyMap )
	
	return newNote
	
	
# Shift the key up a semitone
def keyShiftUp( keyMap, shiftDistance, note ):
	print "keyShiftUp."

	newKey = []
	for currentNote in keyMap:
		newKey.append( currentNote + shiftDistance )
		
	shiftedNote = note + shiftDistance
		
	return ( newKey, shiftedNote )
	
	
# Shift the key up a semitone
def keyShiftDown( keyMap, shiftDistance, note ):
	print "keyShiftDown."

	newKey = []
	for currentNote in keyMap:
		newKey.append( currentNote - shiftDistance )
		
	shiftedNote = note - shiftDistance
		
	return ( newKey, shiftedNote )
	

# Generates a triad (three note chord) from a given key. Returns it as a tuple.
def getChord( keyMap ):
	print "getChord."

	chord = ( ( keyMap[0] + 60 ), ( keyMap[2] + 60 ), ( keyMap[4] + 60 ) )
	
	return chord
	
	
# Compares two chords
def chordComparison( currentChord, lastChord ):

	if ( currentChord == lastChord ) and not staccato:
			noteA = -2
			noteB = -2
			noteC = -2
	else:
		noteA = currentChord[0]
		noteB = currentChord[1]
		noteC = currentChord[2]
			
	appendChord = ( noteA, noteB, noteC )
	
	return appendChord
			
		
	
	
# Shift a keyMap into a minor key
def keySwitchMinor( keyMap ):
	print "keySwitchMinor."
	print keyMap

	if keyMap[2] == ( keyMap[1] + 2 ):
		keyMap[2] = keyMap[2] - 1
		keyMap[6] = keyMap[6] - 1
		
	print keyMap
	return keyMap
	
	
# Shift a keyMap into a major key
def keySwitchMajor( keyMap ):
	print "keySwitchMajor."
	print keyMap

	if keyMap[2] == ( keyMap[1] + 1 ):
		keyMap[2] = keyMap[2] + 1
		keyMap[6] = keyMap[6] + 1
	
	print keyMap
	return keyMap
	

# Generate an axiom of six grades from signals
def generateAxiomSixGrade( signals ):

	print signals

	axiom = []

	for currentSignal in signals:
			
			if currentSignal >= SIX_GRADE_A:
				currentGrade = 'A'
			elif currentSignal >= SIX_GRADE_B:
				currentGrade = 'B'
			elif currentSignal >= SIX_GRADE_C:
				currentGrade = 'C'
			elif currentSignal >= SIX_GRADE_D:
				currentGrade = 'D'
			elif currentSignal >= SIX_GRADE_E:
				currentGrade = 'E'
			else:
				currentGrade = 'F'
				
			axiom.append( currentGrade )
			
	return axiom
	
	
# Generate an axiom of six grades from signals
def generateAxiomTenGrade( signals ):

	axiom = []

	for currentSignal in signals:
			
			if currentSignal >= TEN_GRADE_A:
				currentGrade = 'A'
			elif currentSignal >= TEN_GRADE_B:
				currentGrade = 'B'
			elif currentSignal >= TEN_GRADE_C:
				currentGrade = 'C'
			elif currentSignal >= TEN_GRADE_D:
				currentGrade = 'D'
			elif currentSignal >= TEN_GRADE_E:
				currentGrade = 'E'
			elif currentSignal >= TEN_GRADE_F:
				currentGrade = 'F'
			elif currentSignal >= TEN_GRADE_G:
				currentGrade = 'G'
			elif currentSignal >= TEN_GRADE_H:
				currentGrade = 'H'
			elif currentSignal >= TEN_GRADE_I:
				currentGrade = 'I'
			else:
				currentGrade = 'J'
				
			axiom.append( currentGrade )
			
	return axiom
	
	
# Some notes
MIDDLE_C = 60
	
	
# Main function
def main():

	# Read in files to get account details
	accounts = prepareAccounts()
	
	# Generate signals from accounts
	signals = generateSignals( accounts )
	
	# Get an overal signal for the account
	compoundSignal = 0.0
	for currentSignal in signals:
		compoundSignal = compoundSignal + currentSignal
	compoundSignal = compoundSignal / len( signals )
	
	# Derive the starting key from the compound signal
	if compoundSignal >= 1.0:
		key = OCTAVE_MAJOR
	else:
		key = OCTAVE_MINOR
		
	# Derive the tempo
	tempo = int( abs( 100 - ( 100 / compoundSignal ) ) * TEMPO_SPEEDUP ) + 100
	if tempo > 240:
		tempo = 240
	elif tempo < 40:
		tempo = 40
	
	# Declare an L-System
	l_System = ()
	
	if gradeSelect == 6:
	
		# Generate the axiom from the signals
		w_s = generateAxiomSixGrade( signals )
			
		# Initialise the L-System
		l_System = getLSystem( V_s, S, w_s, P_s )
			
	elif gradeSelect == 10:
	
		# Generate the axiom from the signals
		w_t = generateAxiomTenGrade( signals )
			
		# Initialise the L-System
		l_System = getLSystem( V_t, S, w_t, P_t )
		
	else:
	
		print "gradeSelect in Settigs.py must be 6 or 10"
		
	print getAxiom( l_System )
		
	# Run L-System
	currentLength = len ( getAxiom( l_System ) )
	previousLength = 0
	while ( len( getAxiom( l_System ) ) <= minimumAxiomLength ) and not ( currentLength == previousLength ):
		l_System = runLSystem( l_System )
		print getAxiom( l_System )
		previousLength = currentLength
		currentLength = getAxiom( l_System )
		
	# Turn the results of the L-System into music
	sequences = produceMusic( getAxiom( l_System ), MIDDLE_C, key )
	print sequences[0], len( sequences[0] ), "\n"
	print sequences[1], len( sequences[1] ), "\n"
	if PLAY_CHORDS:
		outSequence = [sequences[0], sequences[1], sequences[2], sequences[3], sequences[4]]
	else:
		outSequence = [sequences[0], sequences[1]]
	outputMusic( outSequence, tempo, MUSIC_SEQUENCING, instrumentSet )
	

# Main execution code
if __name__ == "__main__":
	main()


### Test code below this point #############################

def test2( n ):

	V_t = ['A', 'B', 'C', 'D']
	S_t = ['u', 'd', 's', 'r', '+', '-']
	w_t = ['A', 'B', 'C', 'D', 'A', 'B', 'C']
	
	rule1 = ( 'A', 'uuuB' )
	rule2 = ( 'B', 'DC' )
	rule3 = ( 'C', 'dsdA' )
	rule4 = ( 'D', '[+CBA-]' )
	
	P_t = [rule1, rule2, rule3, rule4]
	
	t_System = getLSystem( V_t, S_t, w_t, P_t )
	print "start:\t", getAxiom( t_System ), "\n\n"
	
	for i in range( n ):
		t_System = runLSystem( t_System )
		print i + 1, ":\t", getAxiom( t_System ), "\n\n"
		
	sequences = produceMusic( getAxiom( t_System ), 48 )
	print sequences[0], len( sequences[0] ), "\n"
	print sequences[1], len( sequences[1] ), "\n"
	outSequence = [sequences[0], sequences[1]]
	outputMusic( outSequence, 120, MUSIC_SEQUENCING )


def test1():
	w = ['[', '[', 'u', 'u', ']', 's', '+', '[', 'd', 'd', 'r', 'r', 'A', 'd', '-', 'd', ']', 'd', 'u', 'u', ']', '+', 's', 'u', 's', 'u']
	s = 60
	sequences = produceMusic( w, s )
	print sequences[0], len( sequences[0] )
	print sequences[1], len( sequences[1] )
	outSequence = [sequences[0], sequences[1]]
	outputMusic( outSequence, 120, MUSIC_SEQUENCING )