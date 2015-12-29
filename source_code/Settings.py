###################################
#       - Financial Music -       #
#        Program  Settings        #
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


### Global Settings

# Declare whether music is played in parallel or in sequence
# (NOTE: MUST BE PARALLEL FOR L-SYSTEM IMPLEMENTATION)
# 0 = Sequential
# 1 = Parallel
MUSIC_SEQUENCING = 0

# Choose 0 output music to file or 1 output music to PlayMusic class
MUSIC_OUTPUT = 0

# Choose the instrument set to use
# pianos only = 1;
# Piano and strings = 2;
# orchestra = 3;
instrumentSet = 2

# Play the chords as staccato
# (note; only applies to L-System implementation)
# 1 = Staccato
# 0 = No staccato
staccato = 0

# The amount that the derived tempo should be speeded up by
TEMPO_SPEEDUP = 1.2


### Mapping Implementation Settings

# Cut off points for generating different types of musical sequences
CUT_OFF_SCALE = 0.15
CUT_OFF_ARPEGGIO = 0.3
CUT_OFF_BROKENCHORD = 0.45


# Upper and lower bounds for the start and end midi note
MIDI_BOUNDS_LOWER = 30
MIDI_BOUNDS_UPPER = 70


### L-System Implementation Settings

# Declare whether chords are played along with the melody
# 0 = No chords
# 1 = Chords
PLAY_CHORDS = 1

# Play a drum beat
# 1 = drums
# 0 = no drums
drums = 0

# Use 6 or 10 set system for L-Sytem
gradeSelect = 6

# L-System constants
S = ['u', 'd', '/', '_', 's', 'r', '+', '-', '.', ',', 'j', 'n']

# The minumum length of a sequence
minimumAxiomLength = 50

############# Six Grade L-System ###############

# 6-set grade boundries
SIX_GRADE_A = 1.25
SIX_GRADE_B = 1.15
SIX_GRADE_C = 1.05
SIX_GRADE_D = 0.95
SIX_GRADE_E = 0.85
SIX_GRADE_F = 0.75

# L-System variables (these are based on element 'gradings'
# with A being excellent and 'F' being awful ).
V_s = ['A', 'B', 'C', 'D', 'E', 'F']

# 'u' - Go up in pitch by 1
# '/' - Go up in pitch by 2
# 'd' - Go down in pitch by 1
# '_' - Go down in pitch by 2
# 's' - Stay on same note
# 'r' - Don't play anything
#
# '.' - Key up
# ',' - Key down
# 'j' - key major
# 'n' - key minor
#
# '+' - Turn on harmony
# '-' - Turn off harmony

# Generic rules for music generation in the L-System
sixGradeRuleA = ( 'A', 'j..uuuuB' )
sixGradeRuleB = ( 'B', '[..suud]C' )
sixGradeRuleC = ( 'C', 'uuu_uuu_C' )
sixGradeRuleD = ( 'D', 'ddd/ddd/D' )
sixGradeRuleE = ( 'E', '[,,sddu]D' )
sixGradeRuleF = ( 'F', 'n,,ddddE' )
P_s = [sixGradeRuleA, sixGradeRuleB, sixGradeRuleC, sixGradeRuleD, sixGradeRuleE, sixGradeRuleF]

############# Six Grade L-System ###############

# 10-set grade boundries
TEN_GRADE_A = 0.0
TEN_GRADE_B = 0.0
TEN_GRADE_C = 0.0
TEN_GRADE_D = 0.0
TEN_GRADE_E = 0.0
TEN_GRADE_F = 0.0
TEN_GRADE_G = 0.0
TEN_GRADE_H = 0.0
TEN_GRADE_I = 0.0
TEN_GRADE_J = 0.0

# L-System variables (these are based on element 'gradings'
# with A being excellent and 'J' being awful ).
V_t = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

# Generic rules for music generation in the L-System
tenGradeRuleA = ( 'A', 'A' )
tenGradeRuleB = ( 'B', 'B' )
tenGradeRuleC = ( 'C', 'C' )
tenGradeRuleD = ( 'D', 'D' )
tenGradeRuleE = ( 'E', 'E' )
tenGradeRuleF = ( 'F', 'F' )
tenGradeRuleG = ( 'G', 'G' )
tenGradeRuleH = ( 'H', 'G' )
tenGradeRuleI = ( 'I', 'G' )
tenGradeRuleJ = ( 'J', 'G' )
P_t = [sixGradeRuleA, sixGradeRuleB, sixGradeRuleC, sixGradeRuleD, sixGradeRuleE, sixGradeRuleF, tenGradeRuleG, tenGradeRuleH, tenGradeRuleI, tenGradeRuleJ]


### Genome Implementation Settings

# The weight multiplier
WEIGHT_MULTIPLIER = 1.5

# Set of financial buzz phrases
F_SET = ['NULL', 'Slump', 'Soar', 'Plunge', 'Boom']


# Sets of musical words
W1_SET = ['NULL', 'Descending', 'Ascending']
W2_SET = ['NULL', 'Major', 'Minor']
W3_SET = ['NULL', 'Scale', 'Crescendo', 'Chord']


# Define valid combinations
W_VALID = [ ( ['Descending', 'Ascending'], ['Major', 'Minor'], ['Scale', 'Crescendo'] ), ( ['NULL'], ['Major', 'Minor'], ['Chord'] ) ]