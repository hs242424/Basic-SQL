import re

def SELECT(statement):
    listPos = 0
    columns = []
    
    inputString = re.findall('\[[^\]]*\]|[^, ]+|".+"', statement)
    inputString = [i.strip('"').strip("[").strip("]") for i in inputString]
    
    while True:
        if listPos == 0 and inputString[listPos] == 'FROM':
            raise ValueError("Must specify columns")
        elif inputString[listPos] == "*" and listPos == 0:
            columns = "All"
            listPos += 1
        elif inputString[listPos] == "FROM":
            listPos += 1
            filePath = inputString[listPos]
            listPos += 1
            break
        else:
            columns.append(inputString[listPos])
            listPos += 1
    
    data = toList(file=filePath)
    
    if columns != "All":
        columnNums = [nameToColumn(data, i) for i in columns]
    else:
        columnNums = [i for i in range(len(data[0]))]
    
    if inputString[listPos] == inputString[-1]:
        return returnData(data, columnNums)
    
    if inputString[listPos].lower() == "where":
        conditions = []
        listPos += 1
        while True:
            brokenCondition = re.findall('[^ <>!=]+|".+"| [=<>!]+ ', inputString[listPos])
            brokenCondition = [i.strip(" ") for i in brokenCondition]
            print(brokenCondition)
            break
        data2 = compare(data, nameToColumn(data, brokenCondition[0]), brokenCondition[2], brokenCondition[1])
        return returnData(data2, columnNums)

        

    
def returnData(data, columns):
    temp = []
    for i in data[1:]:
        temp.append([i[j] for j in columns])
    return temp


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

def compare(data, columnNum, val, comparitor):
    temp = []
    if comparitor == "=":
        for i in data:
            if i[columnNum].lower() == val.lower():
                temp.append(i)
        return temp       
    elif comparitor == ">":
        pass
    elif comparitor == "<":
        pass
    elif comparitor == "!=":
        pass
    else:
        raise AttributeError

def APPEND(statement):
    print(statement)
