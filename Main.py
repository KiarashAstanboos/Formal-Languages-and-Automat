from lb import *
import sys


# inp1 = input("please enter input 1")
# inp2=  input("please enter input 2")
inp1 = "(a*+b*)*(ab)(a+b)*"
inp2="(a+b)*(ba)(ab)*"
print ("Regular Expression: ", inp1)
nfaObj1 = NFAfromRegex(inp1)
nfa1 = nfaObj1.getNFA()
dfaObj1 = DFAfromNFA(nfa1)
dfa1 = dfaObj1.getDFA()
minDFA1 = dfaObj1.getMinimisedDFA()
print(minDFA1.states)
print(minDFA1.finalstates)
print(minDFA1.transitions)

print ("Regular Expression: ", inp2)
nfaObj2 = NFAfromRegex(inp2)
nfa2 = nfaObj2.getNFA()
dfaObj2 = DFAfromNFA(nfa2)
dfa2 = dfaObj2.getDFA()
minDFA2= dfaObj2.getMinimisedDFA()
print(minDFA2.states)
print(minDFA2.finalstates)
print(minDFA2.transitions)
if minDFA2.states==minDFA1.states :
    if minDFA1.finalstates==minDFA1.finalstates:
        if minDFA1.transitions==minDFA1.transitions: print("languages are equal")
        else :print("languages are not equal")
    else:
        print("languages are not equal")
else :print("languages are not equal")



