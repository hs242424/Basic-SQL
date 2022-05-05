import re

def SELECT(statement):
    listPos = 0
    columns = []
    x = re.findall('[^, ]+|".+"', statement)
    x = [i.strip('"') for i in x]
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
    data = toList(file=filePath)
    columnNums = [nameToColumn(data, i) for i in columns]
    print(columnNums)

def toList(file):
    file = open(file=file)
    temp = []
    for line in file:
        temp.append([i.strip('"') for i in re.findall('[^",]+|".+"', line.strip("\n"))])
    return temp


def nameToColumn(data, name):
    for i in data[0]:
        if i.lower() == name.lower():
            return data[0].index(i)
    raise AttributeError(f"{name} is not a valid column")



def APPEND(statement):
    print(statement)
