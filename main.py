

#opens text file and returns string as 2d array, each index is a new line in the txt file
def readFile(filename):
    f = open(filename)
    data = f.readlines()
    f.close()
    return data

#returns true if character is letter, false otherwise
def isLetter(ch):
    i=0
    letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
              'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
              'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    while i < len(letter):
        if ch == letter[i]:
            return True
        i+=1
    return False

#if next input has pre defined word, return that word. otherwise return 0
def isWord(file, i, j):
    k = 0
    temp = j
    words = ["and", "bool", "do", "else", "end", "false", "fi", "if", "int", "not", "od", "or", "print", "program",
             "then", "true", "while"]
    while k < len(words):
        j = temp
        l = 0
        while l < len(words[k]):
            if file[i][j] == words[k][l]:
                if l == len(words[k])-1:
                    if isDigit(file[i][j+1]) or isLetter(file[i][j+1]) or file[i][j+1] == "_":
                        return 0
                    return words[k]
                l += 1
                j += 1
            else:
                break

        k += 1
    return 0

#returns symbol if there is a pre defined symbol, returns 0 otherwise
def isSymbol(file, i, j):
    k = 0
    temp = j
    symbols = ["=<", ">=", "!=", ":=", "<", ">", ":", ";", "+", "-", "*", "/", "(", ")"]
    if file[i][j] == "=" and file[i][j + 1] == "<":
        return "=<"

    elif file[i][j] == ">" and file[i][j + 1] == "=":
        return ">="

    elif file[i][j] == "!" and file[i][j+1] == "=":
        return "!="

    elif file[i][j] == ":" and file[i][j + 1] == "=":
        return ":="

    elif file[i][j] == "<" or file[i][j] == ">" or file[i][j] == ":" or file[i][j] == ";" or file[i][j] == "+" or file[i][j] == "-" or file[i][j] == "*" or file[i][j] == "/" or file[i][j] == "(" or file[i][j] == ")" or file[i][j] == "=":
        return file[i][j]

    else:
        return 0


#returns Identifier
def isID(file, i, j):
    ID = file[i][j]
    j += 1
    while isDigit(file[i][j]) or isLetter(file[i][j]) or file[i][j] == "_":
            ID += file[i][j]
            j+=1
    return ID


#returns true if character is digit, false otherwise
def isDigit(ch):
    i=0
    digit = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    while i < len(digit):
        if ch == digit[i]:
            return True
        i += 1
    return False

#returns num
def isNum(file, i, j):
    num = file[i][j]
    j += 1
    while isDigit(file[i][j]):
        num += file[i][j]
        j+=1
    return num

#returns 0 if there is not double slash and returns the rest of the line as comment if there is
def getComment(file, i, j):
    if file[i][j] == "/" and file[i][j + 1] == "/":
        comment = ""
        while j < len(file[i])-1:
            comment+=file[i][j]
            j+=1
        return comment
    return 0


#returns [token,kind,value]
def next(file, i, j):
    if isLetter(file[i][j]):
        if isWord(file, i, j) != 0:
            word = isWord(file, i, j)
            return [word, word, ""]

        else:
            ID = isID(file, i, j)
            return [ID, "ID", ID]

    elif isDigit(file[i][j]):
            num = isNum(file, i, j)
            return [num, "num", num]

    else:
        if getComment(file, i, j) != 0:
            comment = getComment(file, i, j)
            return [comment, "comment", ""]

        elif isSymbol(file, i, j) != 0:
            symbol = isSymbol(file, i, j)
            return [symbol, "", symbol]

        else:
            return 0
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#lexial analyzer functions



#syntax analyzer functions
#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

def body(list,current):
    #decloration testing
    temp = declarations(list, current)
    if temp[0] != 0:
        current = temp[1]

    #statements testing
    current = statements(list,current)
    return current


#state is always called as 0. only used while in recursion
#returns array with [passed or failed, increment]
def declarations(list,current,state=0):
    if not (list[current][2] == 'bool' or list[current][2] == 'int'):
        return [state, current]
    else:
        current += 1
        if list[current][3] != 'ID':
            return [state, current-1]
        else:
            current += 1
            if list[current][2] != ';':
                return [state, current-1]
            else:
                current += 1
                return declarations(list, current, 1)

def statements(list,current,state=0):
    #test for assignment, conditonal, iterative, or print statement
    if list[current][3]=="ID":
        current = assignmentStatement(list, current)
        state+=1
    elif list[current][2]=="if":
        current = conditionalStatement(list, current)
        state += 1
    elif list[current][2]=="while":
        current = iterativeStatement(list, current)
        state += 1
    elif list[current][2]=="print":
        current = printStatement(list, current)
        state += 1
    if state == 0:
        print("error at: " + str(list[current]))
        quit()
    elif (state != 0) and (list[current][2] == ';'):
        current+=1
        current = statements(list,current,state)
    return current

#returns increment
def assignmentStatement(list,current):
    current += 1
    if not (list[current][2] == ":="):
        print("error at: " + str(list[current]))
        quit()
    else:
        current += 1
        return expression(list, current)


# returns array [pass 1 or fail 0, increment]
def conditionalStatement(list, current):

    if not (list[current][2] == 'if'):
        print("error at: " + str(list[current]))
        quit()
    current+=1
    current = expression(list,current)
    if not (list[current][2] == 'then'):
        print("error at: " + str(list[current]))
        quit()
    current += 1
    current = body(list,current)
    if (list[current][2] == 'else'):
        current += 1
        current = body(list,current)
    if not (list[current][2] == 'fi'):
        print("error at: " + str(list[current]))
        quit()
    return (current+1)



#returns array [pass 1 or fail 0, increment]
def iterativeStatement(list, current):
    current += 1
    current = expression(list,current)
    if list[current][2] != "do":
        print("error at: " + str(list[current]))
        quit()
    current += 1
    current = body(list,current)
    if list[current][2] != "od":
        print("error at: " + str(list[current]))
        quit()
    return (current + 1)



# returns array [pass 1 or fail 0, increment]
def printStatement(list, current):
    current += 1
    return expression(list,current)

# returns increment
def expression(list,current):
    current = term(list, current)
    while (list[current][2] == '+') or (list[current][2] == '-') or (list[current][2] == 'or'):
        current+=1
        current = term(list, current)
    while (list[current][2] == '<') or (list[current][2] == '>') or (list[current][2] == '=<') or (list[current][2] == '=') or (list[current][2] == '!=') or (list[current][2] == '>='):
        current += 1
        current = expression(list,current)
    return current

#returns increment
def term(list,current):
    if (list[current][2] == '-' or list[current][2] == 'not'):
        current += 1
    if not (list[current][2] == 'true' or list[current][2] == 'false' or list[current][3] == 'num' or list[current][3] == 'ID' or list[current][2] == '('):
        print("error at: " + str(list[current]))
        quit()
    else:
        #check if we need to go into expression()
        if (list[current][2] == '('):
            current += 1
            current = expression(list,current)
            if not (list[current][2] == ')'):
                print("error at: " + str(list[current]))
                quit()
            else:
                current +=1
                return current
        else:
            current += 1
            if not (list[current][2] == '*' or list[current][2] == '/' or list[current][2] == 'and'):
                return current
            else:
                current += 1
                return term(list,current)



#Lexical analyzer
#____________________________________________________________________________________________________________________________________________________________
tokenArray = []
file = readFile("hiding.txt")
linenumber = len(file)-1
file[linenumber] += " "
i=0
j=0
tc=0
while i < len(file):
    while j < len(file[i]):
        if file[i][j].isspace():
            j+=1
        else:
            temp = next(file, i, j)
            if temp == 0:
                print(str(file[i][j]) + " on line:" + str(i) + " position:" + str(j) + " is not a valid character")
                quit()
                #[line number, character number, token, kind, value]
            tokenArray.append([i,j,temp[0],temp[1],temp[2]])
            j += len(temp[0])
            tc += 1
            if temp[0] == "end":
                break
    i += 1
    j = 0
    if temp == 0:
        break

abcd = 0

#syntax analyzer
#_____________________________________________________________________________________________________________________________________________________________

#remove all comments from tokenArray
current = 0
i = 0
while i<len(tokenArray):
    if tokenArray[i][3] == "comment":
        tokenArray.pop(i)
    i+=1
print(*tokenArray, sep='\n')

# check list for "program" followed by an ID followed by ":"
if tokenArray[current][2] == "program":
    current += 1
    if tokenArray[current][3] == "ID":
        current += 1
        if tokenArray[current][2] == ":":
            current += 1
        else:
            print("error at: " + str(tokenArray[current]))
            quit()
    else:
        print("error at: " + str(tokenArray[current]))
        quit()
else:
    print("error at: " + str(tokenArray[current]))
    quit()

current = body(tokenArray,current)

if tokenArray[current][2] != "end":
    print("error at: " + str(tokenArray[current]))
    quit()
print("passed")

















