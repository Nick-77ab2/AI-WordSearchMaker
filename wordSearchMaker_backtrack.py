#===============================================================================
#  Word Search Constructor
#===============================================================================
import sys,random, copy
#============================================================================
# get_arg() returns command line arguments.
#============================================================================
def get_arg(index, default=None):
    '''Returns the command-line argument, or the default if not provided'''
    return sys.argv[index] if len(sys.argv) > index else default



#--------------------------------------------------------------------------------

class Grid:

	#----------------------------------------------------------------------------
	# Grid: 
	# A NUM_ROWS x NUM_COLS grid of characters
	#----------------------------------------------------------------------------

	def __init__(self, nRows, nCols):
		self.NUM_ROWS = nRows
		self.NUM_COLS = nCols
		self.grid = [[" " for cols in range(nCols)] for rows in range(nRows)]

	def __getitem__(self, index):
		return self.grid[index]

	def __str__(self):
		#========================================================================
		# Prints Puzzle 
		#========================================================================
	    out = "+" + "---+"*self.NUM_ROWS + "\n"
	    for i in range(self.NUM_ROWS):
		    for j in range(self.NUM_COLS):
			    out += "| " + self.grid[i][j] + " "
		    out += "|" + "\n"
		    out += "+" + "---+"*self.NUM_COLS + "\n"
	    return out
#========================================================================
# State 
# Holds the current "state" of the grid and words
#========================================================================
class State:

    def __init__(self, grid, words):
        self.grid=grid
        self.words=words
        
    def __str__(self):
        out = self.grid.__str__()
        out += "\n list of words:\n"
        for i in self.words:
            out+= i + ", "
            out+="\n"
        return out


#Create and define rule class and its functions.
class Rule:
    def __init__(self, word, row, col, dh, dv):
        self.word=word
        self.row=row
        self.col=col
        self.dh=dh
        self.dv=dv

    #return the position and direction of the word being placed.
    def __str__(self):
        output="Place the word " + '"' + self.word + '"' + "in the grid starting at position (" + str(self.row) + "," + str(self.col) + ") and proceeding in the direction [" + str(self.dh) + "," + str(self.dv) + "].\n"
        return output
    #-----------------------------------------------------------------------------
    # APPLYRULE
    #apply the rule to the state, does not check preconditions.
    #-----------------------------------------------------------------------------
    def applyRule(self,state):
        newState=copy.deepcopy(state)
        #set required values to variables, create new grid, reduce the wordlist for resulting state by 1
        wordlen=len(self.word)
        words=newState.words
        words.remove(self.word)
        newGrid=newState.grid
        word=self.word
        i=0
        #add word to location in direction for as long as possible (just making sure it doesn't crash the program, despite making sure of it in precondition beforehand)
        while i < wordlen:
            newrowpos= self.row + (i * self.dv)
            newcolpos= self.col + (i * self.dh)
            if 0 <= newrowpos <= newState.grid.NUM_ROWS and 0 <= newcolpos <= newState.grid.NUM_COLS:
                newGrid[newrowpos][newcolpos]=word[i]
            i+=1 
        return State(newGrid, words)
#-----------------------------------------------------------------------------------------------------------------------------------------------------
# PRECONDITION
# Precondition: word does not extend beyond edge of grid if dh==1: if row + len(word) > Grid.NUM_ROWS etc. (will occur in applyRule)
# Precondition: word does not conflict with existing words in grid
#-----------------------------------------------------------------------------------------------------------------------------------------------------
    def precondition(self,state):
        #check directions
        direction=[self.dh,self.dv]
        length=len(self.word)
        if  (direction[0] == 1 and (length + self.col) > state.grid.NUM_COLS) or \
            (direction[0] == -1 and (length - 1) > self.col) or \
            (direction[1] == 1 and (length + self.row) > state.grid.NUM_ROWS) or \
            (direction[1] == -1 and (length - 1) > self.row):
                return False
        #compare Grid to newGrid cell by cell. Make sure of non-switched and empty to filled.
        temp=self.applyRule(state)
        for i in range(0, state.grid.NUM_ROWS):
            for j in range(0, state.grid.NUM_COLS):
                oldVal=state.grid[i][j]
                newVal=temp.grid[i][j]
                if oldVal !=' ' and newVal !=oldVal:
                    return False
        return True
#--------------------------------------------------------------------------------
# DETERMINING ALL CANDIDATES
# determines all candidates for the specified word and returns a list of them.
#--------------------------------------------------------------------------------
def allCandidates(word, state):
    possibilities=[]
    #create all possible rules
    for r in range(0, state.grid.NUM_ROWS):    
        for c in range(0, state.grid.NUM_COLS):
            for h in range(-1, 2):
                for v in range(-1, 2):
                    if v==0 and h==0:
                        continue
                    rule = Rule(word,r,c,h,v)
                    if rule.precondition(state):
                        possibilities.append(rule)
    return possibilities

#--------------------------------------------------------------------------------
# GOAL STATE
#--------------------------------------------------------------------------------
def goal(state):
    if state.words == []:
        return True

#============================================================================
# Flail Wildly strategy
#============================================================================
def flailWildly(state):
    count = -1
    stuck = False
    while (not goal(state) ) and (not stuck):
        count = count + 1
        print("\n[%d] ======\n     state:\n%s" %(count,state))
        print("\n" + state.words[0] + "\n")
        rules = allCandidates(state.words[0],state)
        print("     There are %d applicable rules" %(len(rules)) )
        if len(rules)==0:
            stuck = True
        else:
            r = random.randint(0,len(rules)-1)
            state = rules[r].applyRule(state)
            print("%s\n" %(rules[r]))
            print(str(state))
		
    if stuck:
        print("Stopped with state: %s" %state )
    else:
        print("\nGoal reached\n\n")
#============================================================================
# Backtracking Strategy
#What each part does is made obvious by it's verbose section.
#============================================================================
backCalls=0
fails=0
def backTrack (stateList, isVerbose):
    state = stateList[0]
    depthBound=len(theWords)+2
    global fails,backCalls
    #Check if member of statelist is duplicate
    for i in range(1, len(stateList)):
        if(stateList[i]==state):
            if isVerbose:
                print("This state has already been reached before.")
            return 'Failed-1'
    if(len(state.words)>0 and allCandidates(state.words[0],state)==0):
        if isVerbose:
            print("There were not any viable places to place the word within the bounds of the rules.")
        return 'Failed-2'
    if(goal(state)):
        return 'NULL'
    if(len(stateList)>depthBound):
        if isVerbose:
            print("The depth of the backTrack states is longer than the depthbound.")
        return 'Failed-3'
    
    ruleSet = allCandidates(state.words[0],state)
    if (ruleSet=='NULL'):
        if isVerbose:
            print("The ruleSet has a NULL value.")
        return 'Failed-4'
    
    for rule in ruleSet:
        newState = Rule.applyRule(rule,state)
        if(isVerbose):
            print("Currently trying rule: " + str(rule))
            print("The state reached from that rule is:\n" + str(newState))
        stateList.insert(0, newState)
        newStateList = stateList
        backCalls+=1
        path=backTrack(newStateList, isVerbose)
        if path!= 'Failed-1' and path!= 'Failed-2' and path!= 'Failed-3' and path!= 'Failed-4' and path!='Failed-5':
            return path + str(rule)
        else:
            fails+=1
    return 'Failed-5'
#--------------------------------------------------------------------------------
#  MAIN PROGRAM
#--------------------------------------------------------------------------------

if __name__ == '__main__':

	#============================================================================
	# Read input from command line:
	#   python3 <this program>.py  NUM_ROWS NUM_COLS filename
	# where NUM_ROWS and NUM_COLS give the size of the grid to be filled,
	# and filename is a file of words to place in the grid, one word per line.
	#============================================================================
	# Sample:
	#   python3 <this program>.py  12 12 wordfile1.txt
	# where wordfile1.txt contains these words on separate lines:
	#   ADMISSIBLE AGENT BACKTRACK CANNIBAL   DEADEND  GLOBAL   GRAPHSEARCH
	#   HEURISTIC  LISP  LOCAL     MISSIONARY OPTIMUM  RATIONAL SEARCH  SYMMETRY
	#============================================================================

    NUM_ROWS = int(get_arg(1))
    NUM_COLS = int(get_arg(2))

    filename = get_arg(3)	
    with open(filename, 'r') as infile:
	    theWords = [line.strip() for line in infile]
    verbose = str(get_arg(4))
	#============================================================================
	# Demonstration code for the Grid class:
	# Shows grid initialization, printing, and assignment to grid cells.
    #============================================================================#
    grid = Grid(NUM_ROWS,NUM_COLS)
    #print(grid)
    #grid[2][3] = "A"
    #grid[3][2] = "B"
    #grid[4][1] = "C"
    #print(grid)
    initialState= State(grid, theWords )
    state = initialState
    random.seed() # use clock to randomize RNG
    initialStateList=[state]
    if verbose!='' and verbose.lower()=="verbose":
        isVerbose=True
    else:
        isVerbose=False
    results=backTrack(initialStateList, isVerbose)
    if results == 'Failed-5':
        print("Backtrack did not complete successfully")
    else:
        theResults=results.split('.')
        theResults.reverse()
        lastResult=theResults[len(theResults)-1]
        lastResult=lastResult[4:]
        theResults[len(theResults)-1]=lastResult
        for result in theResults:
            print(result)
        print("Number of Fails: " + str(fails) + "\nNumber of BackCalls: " + str(backCalls))
    