class Automata:
    """class to represent an Automata"""

    def __init__(self, language = set(['0', '1'])):
        self.states = set()
        self.startstate = None
        self.finalstates = []
        self.transitions = dict()
        self.language = language
        self.table=list()
    @staticmethod
    def epsilon():
        return "e"

    def setstartstate(self, state):
        self.startstate = state
        self.states.add(state)

    def addfinalstates(self, state):
        if isinstance(state, int):
            state = [state]
        for s in state:
            if s not in self.finalstates:
                self.finalstates.append(s)

    def addtransition(self, fromstate, tostate, inp):
        if isinstance(inp, str):
            inp = set([inp])
        self.states.add(fromstate)
        self.states.add(tostate)
        if fromstate in self.transitions:
            if tostate in self.transitions[fromstate]:
                self.transitions[fromstate][tostate] = self.transitions[fromstate][tostate].union(inp)
            else:
                self.transitions[fromstate][tostate] = inp
        else:
            self.transitions[fromstate] = {tostate : inp}

    def addtransition_dict(self, transitions):
        for fromstate, tostates in transitions.items():
            for state in tostates:
                self.addtransition(fromstate, state, tostates[state])

    def gettransitions(self, state, key):
        if isinstance(state, int):
            state = [state]
        trstates = set()
        for st in state:
            if st in self.transitions:
                for tns in self.transitions[st]:
                    if key in self.transitions[st][tns]:
                        trstates.add(tns)
        return trstates

    def getEClose(self, findstate):
        allstates = set()
        states = set([findstate])
        while len(states)!= 0:
            state = states.pop()
            allstates.add(state)
            if state in self.transitions:
                for tns in self.transitions[state]:
                    if Automata.epsilon() in self.transitions[state][tns] and tns not in allstates:
                        states.add(tns)
        return allstates

    def newBuildFromNumber(self, startnum):
        translations = {}
        for i in list(self.states):
            translations[i] = startnum
            startnum += 1
        rebuild = Automata(self.language)
        rebuild.setstartstate(translations[self.startstate])
        rebuild.addfinalstates(translations[self.finalstates[0]])
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                rebuild.addtransition(translations[fromstate], translations[state], tostates[state])
        return [rebuild, startnum]

class BuildAutomata:
    """class for building e-nfa basic structures"""

    @staticmethod
    def basicstruct(inp):
        state1 = 1
        state2 = 2
        basic = Automata()
        basic.setstartstate(state1)
        basic.addfinalstates(state2)
        basic.addtransition(1, 2, inp)
        return basic

    @staticmethod
    def plusstruct(a, b):
        [a, m1] = a.newBuildFromNumber(2)
        [b, m2] = b.newBuildFromNumber(m1)
        state1 = 1
        state2 = m2
        plus = Automata()
        plus.setstartstate(state1)
        plus.addfinalstates(state2)
        plus.addtransition(plus.startstate, a.startstate, Automata.epsilon())
        plus.addtransition(plus.startstate, b.startstate, Automata.epsilon())
        plus.addtransition(a.finalstates[0], plus.finalstates[0], Automata.epsilon())
        plus.addtransition(b.finalstates[0], plus.finalstates[0], Automata.epsilon())
        plus.addtransition_dict(a.transitions)
        plus.addtransition_dict(b.transitions)
        return plus

    @staticmethod
    def dotstruct(a, b):
        [a, m1] = a.newBuildFromNumber(1)
        [b, m2] = b.newBuildFromNumber(m1)
        state1 = 1
        state2 = m2-1
        dot = Automata()
        dot.setstartstate(state1)
        dot.addfinalstates(state2)
        dot.addtransition(a.finalstates[0], b.startstate, Automata.epsilon())
        dot.addtransition_dict(a.transitions)
        dot.addtransition_dict(b.transitions)
        return dot

    @staticmethod
    def starstruct(a):
        [a, m1] = a.newBuildFromNumber(2)
        state1 = 1
        state2 = m1
        star = Automata()
        star.setstartstate(state1)
        star.addfinalstates(state2)
        star.addtransition(star.startstate, a.startstate, Automata.epsilon())
        star.addtransition(star.startstate, star.finalstates[0], Automata.epsilon())
        star.addtransition(a.finalstates[0], star.finalstates[0], Automata.epsilon())
        star.addtransition(a.finalstates[0], a.startstate, Automata.epsilon())
        star.addtransition_dict(a.transitions)
        return star

class NFAfromRegex:
    """class for building e-nfa from regular expressions"""

    def __init__(self, regex):
        self.star = '*'
        self.plus = '+'
        self.dot = '.'
        self.openingBracket = '('
        self.closingBracket = ')'
        self.operators = [self.plus, self.dot]
        self.regex = regex
        self.alphabet = [chr(i) for i in range(65,91)]
        self.alphabet.extend([chr(i) for i in range(97,123)])
        self.alphabet.extend([chr(i) for i in range(48,58)])
        self.buildNFA()

    def getNFA(self):
        return self.nfa


    def buildNFA(self):
        language = set()
        self.stack = []
        self.automata = []
        previous = "::e::"
        for char in self.regex:
            if char in self.alphabet:
                if char != 'e':language.add(char)
                if previous != self.dot and (previous in self.alphabet or previous in [self.closingBracket,self.star]):
                    self.addOperatorToStack(self.dot)
                self.automata.append(BuildAutomata.basicstruct(char))
            elif char  ==  self.openingBracket:
                if previous != self.dot and (previous in self.alphabet or previous in [self.closingBracket,self.star]):
                    self.addOperatorToStack(self.dot)
                self.stack.append(char)
            elif char  ==  self.closingBracket:
                if previous in self.operators:
                    raise BaseException("Error processing '%s' after '%s'" % (char, previous))
                while(1):
                    if len(self.stack) == 0:
                        raise BaseException("Error processing '%s'. Empty stack" % char)
                    o = self.stack.pop()
                    if o == self.openingBracket:
                        break
                    elif o in self.operators:
                        self.processOperator(o)
            elif char == self.star:
                if previous in self.operators or previous  == self.openingBracket or previous == self.star:
                    raise BaseException("Error processing '%s' after '%s'" % (char, previous))
                self.processOperator(char)
            elif char in self.operators:
                if previous in self.operators or previous  == self.openingBracket:
                    raise BaseException("Error processing '%s' after '%s'" % (char, previous))
                else:
                    self.addOperatorToStack(char)
            else:
                raise BaseException("Symbol '%s' is not allowed" % char)
            previous = char
        while len(self.stack) != 0:
            op = self.stack.pop()
            self.processOperator(op)
        if len(self.automata) > 1:
            print (self.automata)
            raise BaseException("Regex could not be parsed successfully")
        self.nfa = self.automata.pop()
        self.nfa.language = language

    def addOperatorToStack(self, char):
        while(1):
            if len(self.stack) == 0:
                break
            top = self.stack[len(self.stack)-1]
            if top == self.openingBracket:
                break
            if top == char or top == self.dot:
                op = self.stack.pop()
                self.processOperator(op)
            else:
                break
        self.stack.append(char)

    def processOperator(self, operator):
        if len(self.automata) == 0:
            raise BaseException("Error processing operator '%s'. Stack is empty" % operator)
        if operator == self.star:
            a = self.automata.pop()
            self.automata.append(BuildAutomata.starstruct(a))
        elif operator in self.operators:
            if len(self.automata) < 2:
                raise BaseException("Error processing operator '%s'. Inadequate operands" % operator)
            a = self.automata.pop()
            b = self.automata.pop()
            if operator == self.plus:
                self.automata.append(BuildAutomata.plusstruct(b,a))
            elif operator == self.dot:
                self.automata.append(BuildAutomata.dotstruct(b,a))
class DFAfromNFA:
    """class for building dfa from e-nfa and minimise it"""

    def __init__(self, nfa):
        self.buildDFA(nfa)


    def getDFA(self):
        return self.dfa

    def getMinimisedDFA(self):
        return self.minDFA

    def buildDFA(self, nfa):
        allstates = dict()
        eclose = dict()
        count = 1
        state1 = nfa.getEClose(nfa.startstate)
        eclose[nfa.startstate] = state1
        dfa = Automata(nfa.language)
        dfa.setstartstate(count)
        states = [[state1, count]]
        allstates[count] = state1
        count += 1
        while len(states) != 0:
            [state, fromindex] = states.pop()
            for char in dfa.language:
                trstates = nfa.gettransitions(state, char)
                for s in list(trstates)[:]:
                    if s not in eclose:
                        eclose[s] = nfa.getEClose(s)
                    trstates = trstates.union(eclose[s])
                if len(trstates) != 0:
                    if trstates not in allstates.values():
                        states.append([trstates, count])
                        allstates[count] = trstates
                        toindex = count
                        count += 1
                    else:
                        toindex = [k for k, v in allstates.items() if v == trstates][0]
                    dfa.addtransition(fromindex, toindex, char)
        for value, state in allstates.items():
            if nfa.finalstates[0] in state:
                dfa.addfinalstates(value)

        dfa.language = sorted(dfa.language)                  #dorost kardane transition table
        dfa.table.append(None)
        for i in range(1, len(dfa.states) + 1):
            temp_tran = list()
            for char in dfa.language:
               temp_tran.append(dfa.gettransitions(i, char))
            dfa.table.append(temp_tran)
        if len(dfa.states)== len(dfa.table):
            dfa.table.append([len(dfa.table)+1]*len(dfa.language)) # momkene state akhar nfa transition nadashte bashe  vase hamin be ezaye har alphabet mibarimesh be trap
        dfa.table.append([len(dfa.table)]*len(dfa.language)) #trap state

        for i in range(1, len(dfa.table) - 1):             # gozashtane transition az state ha be trap state va avaz kardan type az set be int
            for j in range(len(dfa.language)):
                if dfa.table[i][j] == set():
                    dfa.table[i][j] = len(dfa.table)-1
                elif not str(dfa.table[i][j]).isnumeric():
                    dfa.table[i][j] = next(iter(dfa.table[i][j]))

        flag=0                                            # momkene az trap estefade nashe . age estefade nashode bashe az table hazf mishe
        for i in dfa.table[1:len(dfa.table)-1]:
            for j in i:
                if j==len(dfa.table)-1 :
                    flag=1
                    break
        if flag==0 : dfa.table.pop()

        if len(dfa.table)-1 not in dfa.states: dfa.states.add(len(dfa.table)-1)  # ezafe kardane state trap be dfa.states
        self.dfa = dfa

    def to_Which_state(self, state, input):  # state va vurudi begire maqsad ro bede
        return self.dfa.table[state][input]

    def in_which_state(self, state, minimized):  # state ro begire va bege too che state dfa minimize shode qarar dare
        for i in minimized:
            if (state in i): return minimized.index(i)

    def minimise(self):
        unmarked=list()
        marked=list()

        # pairs
        for i in self.dfa.states:
            for j in self.dfa.states:
                if j>i  : unmarked.append((i,j))
        # joda kardane final az nonfinal
        t=0
        while t<(len(unmarked)):
            tuples=unmarked[t]
            a=tuples[0]
            b=tuples[1]
            if ((a in self.dfa.finalstates) & (b not in self.dfa.finalstates)) or  ((b in self.dfa.finalstates) & (a not in self.dfa.finalstates)):
                    marked.append(unmarked.pop(unmarked.index(tuples)))
            else :t+=1
        #peyda kardane marked
        flag = True
        while flag:
            flag = False
            t = 0
            while t < (len(unmarked)):
                tuples = unmarked[t]
                a = tuples[0]
                b = tuples[1]
                for alphabet in range(len(self.dfa.language)):
                    if ((self.dfa.table[a][alphabet],self.dfa.table[b][alphabet]) in marked) or \
                            ((self.dfa.table[b][alphabet],self.dfa.table[a][alphabet]) in marked):
                          marked.append(unmarked.pop(unmarked.index(tuples)))
                          flag = True
                          break
                else:
                    t += 1

        #merge kardane state haye yeksan
        flag = True
        while flag:
            flag=False
            t = 0
            while t < (len(unmarked)):
                 s=t+1
                 while s <len(unmarked):
                    if len(set(unmarked[t]) & set(unmarked[s])) >=1:
                        unmarked[t]=tuple(set(unmarked[t] + unmarked[s]))
                        unmarked.pop(s)
                        if s==len(unmarked): s=len(unmarked)-1
                        flag =True
                    s+=1
                 t+=1



        minimized_states=[]
        minimized_states = minimized_states + unmarked
        for i in self.dfa.states: # state haye dfa minimized shode
            flag = False
            for j in unmarked:
                if (i in j): flag=True
            if flag==False: minimized_states.append((i,))



########################################################


        minimized_table=[]
        transition = []

        for alpha in range(len(self.dfa.language)): # transition start state
            next_old = self.to_Which_state(1, alpha)
            next_new = self.in_which_state(next_old, minimized_states)
            transition.append(next_new)
        minimized_table.append(transition)
        start=self.in_which_state(1,minimized_states)


        for i in minimized_states: # transition table baqie state ha
            if minimized_states.index(i)!= start:
                transition=[]
                state=i[0]
                for alpha in range(len(self.dfa.language)):
                    next_old=self.to_Which_state(state,alpha)
                    next_new=self.in_which_state(next_old,minimized_states)
                    transition.append(next_new)
                minimized_table.append(transition)
        final_states=[]
        for i in self.dfa.finalstates:
            new_final=self.in_which_state(i,minimized_states)
            if new_final not in final_states: final_states.append(new_final)

        self.dfa.finalstates=final_states
        self.dfa.table=minimized_table
        states=[]
        for i in range(len(minimized_table)): states.append(i)
        self.dfa.states=states

        return


