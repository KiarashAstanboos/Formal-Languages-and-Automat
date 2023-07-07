from lb import *

inp1 = "(ab+c)*"
inp2="(b*a)*b*"

print("Regular Expression: ", inp1)
nfaObj1 = NFAfromRegex(inp1)
nfa1 = nfaObj1.getNFA()
dfaObj1 = DFAfromNFA(nfa1)
dfa1=dfaObj1.minimise()
dfa1 = dfaObj1.getDFA()



print ("Regular Expression: ", inp2)
nfaObj2 = NFAfromRegex(inp2)
nfa2 = nfaObj2.getNFA()
dfaObj2 = DFAfromNFA(nfa2)
dfa2=dfaObj2.minimise()
dfa2 = dfaObj2.getDFA()



if dfa2.states==dfa2.states :
    if dfa2.language==dfa2.language:
        if dfa1.table==dfa2.table: print("languages are equal")
        else :print("languages are not equal")
    else: print("languages are not equal")
else :print("languages are not equal")



