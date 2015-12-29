####################
# Genome Prototypes
#
# Financial   Music
# Daniel Demby  '08
####################

# Static values
F_MAX = 4
W1_MAX = 4
W2_MAX = 3

# The weight multiplier
WEIGHT_MULTIPLIER = 1.5

# Godel numbering function
def godel(a, b, c):
    return float(2 ** a) * float(3 ** b) * float(5 ** c)

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

# Set of financial buzz phrases
F_SET = ['Slump', 'Soar', 'Plunge', 'Boom']

# Sets of musical words
W1_SET = ['Descending', 'Ascending', 'Major', 'Minor']
W2_SET = ['Scale', 'Crescendo', 'Chord']

# The set of all possible genes
GN = {}
for F in F_SET:
    for W1 in W1_SET:
        for W2 in W2_SET:
            GN[godel(F_SET.index(F), W1_SET.index(W1), W2_SET.index(W2))] = (F + ' ' + W1 + ' ' + W2)

# The set of all possible genes
#GN = [godel(F, W1, W2) for F in range(1, F_MAX) for W1 in range(1, W1_MAX) for W2 in range(1, W2_MAX)]
#GN.sort()

# The complete genome
# (ie; the set of all possible genes, with invalid genes removed)
GN_VALID = set([30.0, 600.0, 900.0, 54000.0])

# Sequence of correctness values for GN
GNC = {}
for x in GN:
    if x in GN_VALID: GNC[x] = 1.0
    else: GNC[x] = 0.0

print len(GN)
print len(GNC)
print GN
print ""
print GNC
print ""

for i in GN:
    #print GNC[i]
    if (GNC[i] == 1.0): print GN[i]
