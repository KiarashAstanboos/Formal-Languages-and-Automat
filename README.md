# Formal-Languages-and-Automat
Equality of two regular expressions
getting two regular expressions as an input and determine if they are equal or not.
steps:
Regular expression ->NFA
NFA->DFA
Minimize DFA (using table filling algorithm)
Example:

input:
𝑏∗(𝑎𝑏𝑏∗)∗(𝑎 + e)
and
(𝑏 + 𝑎𝑏)∗(𝑎 + e)
output:
Yes

input:
(𝑎 + 𝑏)∗
and
(𝑎∗𝑏∗)
output:
No

e stands for epsilon and it cannot be a part of the alphabet of the language.

