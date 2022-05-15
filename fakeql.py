'''
Header:
Author: Harrison Servedio
Version: 1.0
Discription: A primitive recreation of SQL intended to be used with csv files
'''

import re


'''
Select is the primary function and is one of the two functions intended to be used by the user
The statement that is intended to be inputed into the functions is as follows

Note Well: in an argument in you statement has spaces surround it in double quotes

'column1, column2 FROM filepath WHERE column operator value'

Before the FROM you can put * for all of the columns of list the columns you want returned separated with a comma

replace file path with the path to your csv file. You may need to use two back slashes
remeber that if your filepath has a space in it you must surround it with quotes

the where is optional if you want conditional statements
the format of condition statements is column, operator such as =, <, >, !=, and then a value

If you want multiple conditions you can separate them with an and

It also returns a line number to easily edit the files
'''
def SELECT(statement):
    listPos = 0                                                                                     # A variable that increases as the program works through the words in the statement
    columns = []                                                                                    # Keeps track of the columns that the user wants returned
    
    inputString = re.findall('[^, ]+|".+"', statement)                                              # Splits the statement into parts
    inputString = [i.strip('"') for i in inputString]                                               # Strips the " from the statements
    
    '''
    This loop goes through the first part of the statement, serching for the columns that should be returned
    '''
    while True:
        if listPos == 0 and inputString[listPos] == 'FROM':                                         # Returns an error if the user does not specify columns
            raise ValueError("Must specify columns")
        elif inputString[listPos] == "*" and listPos == 0:                                          # Checks if the user enter * for columns
            columns = "All"
            listPos += 1
        elif inputString[listPos] == "FROM":                                                        # Checks for the end of the list of columns
            listPos += 1
            filePath = inputString[listPos]                                                         # Locates the filename because it should be directly after the FROM
            listPos += 1
            break
        else:
            columns.append(inputString[listPos])                                                    # Adds the colum the user wants to the list of columns  
            listPos += 1
    
    data = toList(file=filePath)                                                                    # converts the data to list of lists
    '''
    If the user doesn't want all of the columns the program finds the list index of the columns they want
    '''
    if columns != "All": 
        columnNums = [nameToColumn(data, i) for i in columns]
    else:                                                                                           # If the user does want all of the columns the program create a list that has the index of every column
        columnNums = [i for i in range(len(data[0]))]
    
    if listPos >= len(inputString):                                                                 # checks if the user has conditions and if not returns the data from the requested columns
        return returnData(data[1:], columnNums)                                                     # Uses a function to find all data from the request columns
    
    if inputString[listPos].lower() == "where":
        data2 = data[1:]
        listPos += 1
        while True:
            try:
                brokenCondition = [inputString[i] for i in range(listPos, listPos+3)]
                data2 = compare(data2, nameToColumn(data, brokenCondition[0]), brokenCondition[2], brokenCondition[1])
                listPos += 4
                if listPos > len(inputString):
                    break
            except:
                raise AttributeError("Your comparisons are incorrect")
            
        return returnData(data2, columnNums)

        

    
def returnData(data, columns):
    temp = []
    for i in data:
        try:
            temp.append([i[j] for j in columns] + [i[-1]])
        except:
            pass
    return temp


def toList(file,columnNums=True):
    file = open(file=file)
    temp = []
    counter = 0
    for line in file:
        if columnNums:
            x = [i.strip(',').strip('"').strip('\n') for i in re.findall('[^",]*[,\n]|".*"[,\n]', line)] + [str(counter)]
        else:
            x = [i.strip(',').strip('"').strip('\n') for i in re.findall('[^",]*[,\n]|".*"[,\n]', line)]
        temp.append(x)
        counter += 1
    file.close()
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
        for i in data:
            try:
                if int(i[columnNum]) > int(val):
                    temp.append(i)
            except:
                raise AttributeError('Either your condition or a value in the data can be converted to an int')
        return temp
    elif comparitor == "<":
        for i in data:
            try:
                if int(i[columnNum]) < int(val):
                    temp.append(i)
            except:
                raise AttributeError('Either your condition or a value in the data can be converted to an int')
    elif comparitor == "!=":
        for i in data:
            if i[columnNum].lower() != val.lower():
                temp.append(i)
        return temp  
    else:
        raise AttributeError


'''
Append adds information to the end of a file
Input format:
filename, column1value, column2, value and so on

If the value for a column contains spaces you must surround it in double quotes

'''
def APPEND(statement):
    inputString = re.findall('[^," ]+|".+"', statement)                                              # Splits the statement into parts
    inputString = [i.strip('"') for i in inputString]
    file = open(inputString[0], 'a')
    temp = ""
    for i in inputString[1:]:
        if " " in i:
            temp += ',"'+i+'"'
        else:
            temp += ","+i
    temp = temp[1:] +'\n'
    file.write(temp)
    file.close()



def DELETE():
    pass

'''
Input format:
line, column, filepath, value
'''
def UPDATE(statement):
    inputString = re.findall('[^," ]+|".+"', statement)                                              # Splits the statement into parts
    inputString = [i.strip('"') for i in inputString]
    data = toList(inputString[2], columnNums=False)
    line = int(inputString[0])
    column = nameToColumn(data, inputString[1])
    data[line][column] = inputString[3]
    temp2 = ""
    for i in data:
        temp = ""
        for j in i:
            if " " in j:
                temp += ',"'+j+'"'
            else:
                temp += ","+j
        temp = temp[1:] +'\n'
        temp2+=temp
    file = open(inputString[2], 'w')
    file.write(temp2)
    file.close