from itertools import count
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
            filePath = x[listPos]
            break
        else:
            columns.append(x[listPos])
            listPos += 1
    print(columns)
    data = toList(filePath)
    returnColumns(columns, data)
    


def toList(file):
    file = open(file=file)
    temp = []
    for line in file:
        temp.append([i.strip('"') for i in re.findall('[^",]+|".+"', line.strip("\n"))])
    return temp
    
def returnColumns(columns, data):
    if columns == "All":
        for i in data[1::]:
            print(i)


def APPEND(statement):
    print(statement)


