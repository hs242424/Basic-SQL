import re

def SELECT(statement):
    listPos = 0
    columns = []
    x = re.findall("[^ ]+", statement)
    while True:
        if listPos == 0 and x[listPos] == 'FROM':
            raise ValueError("Must specify columns")
        elif x[listPos] == "*" and listPos == 0:
            columns = "All"
            listPos += 1
        elif x[listPos] == "FROM":
            listPos += 1
            break
        else:
            columns.append(x[listPos])
            listPos += 1
    print(columns)


    
    

def APPEND(statement):
    print(statement)

def search():
    print("Yes")

def __search():
    pass
