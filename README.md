# lex-syn-analyzer: Michael Long
lexical and syntax analyzer for a mini coding language
The grammar for the language is included in grammar.txt
'example' folder contains example code that will either fail or succeed

First part of the program contains functions used within the lexical analyzer, followed by functions
used within the syntax analyzer, lexical analyzer code, and syntax analyzer code.
To test diferent txt files, alter the readFile function underneath '#lexical analyzer'

after run, the program will produce all tokens in a 2d array with token, type, line number, and per line character number, after comments are removed.
This is followed by a 'passed' if it is syntaxically correct or an error message with the corresponding error listed
