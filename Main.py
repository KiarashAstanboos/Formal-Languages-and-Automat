from lb import *
import sys


# inp1 = input("please enter input 1")
# inp2=  input("please enter input 2")
inp1 = "a*b*c*"
inp2="((b*)+(b+ab)*a)b*"

print("Regular Expression: ", inp1)
nfaObj1 = NFAfromRegex(inp1)
nfa1 = nfaObj1.getNFA()
dfaObj1 = DFAfromNFA(nfa1)
dfa1 = dfaObj1.getDFA()



print ("Regular Expression: ", inp2)
nfaObj2 = NFAfromRegex(inp2)
nfa2 = nfaObj2.getNFA()
dfaObj2 = DFAfromNFA(nfa2)
dfa2 = dfaObj2.getDFA()
print( 'hello')


# if minDFA2.states==minDFA1.states :
#     if minDFA1.finalstates==minDFA2.finalstates:
#         if minDFA1.transitions==minDFA2.transitions: print("languages are equal")
#         else :print("languages are not equal")
#     else: print("languages are not equal")
# else :print("languages are not equal")



