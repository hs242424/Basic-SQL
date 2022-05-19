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
the format of condition statements is column, operator such as =, <, >, !=, and then a value and second condition

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
    
    if inputString[listPos].lower() == "where":                                                     # If the user has ented conditions it begins evaluating them
        data2 = data[1:]                                                                            # Removes the column names from the data
        listPos += 1
        while True:                                                                                 # Repeastes until all condition have been evaluated
            try:                                                                                    # The try except is used to inform the user if they have entered incorrect data
                # This next block of code finds the conditions and then evalutes them
                brokenCondition = [inputString[i] for i in range(listPos, listPos+3)]
                data2 = compare(data2, nameToColumn(data, brokenCondition[0]), brokenCondition[2], brokenCondition[1])
                listPos += 4
                if listPos > len(inputString):
                    break
            except:
                raise AttributeError("Your comparisons are incorrect")
            
        return returnData(data2, columnNums)                                                        # Return the final data

        

'''
This function takes a list of lists and a lists of column numbers and returns only the columns specified in the list of column numbers
'''
def returnData(data, columns):
    temp = []
    for i in data:
        try:                                                                                        # The try is used so that if the column does exist an error is not raised
            temp.append([i[j] for j in columns] + [i[-1]])                                          # This part iterates through each column in a specif line and returns the column if it is in the list of columns
        except:
            pass
    return temp

'''
This function converts a csv to a list of lists
file is the filepath
columnNums specifies if the number of the column should be appened to the list items
'''
def toList(file,columnNums=True):
    file = open(file=file)                                                                          # Opens the file in read mode
    temp = []
    counter = 0                                                                                     # The counter is used to keep track of the column number
    for line in file:
        # Only appends column number if the code specifies a column number should be addded
        if columnNums:
            x = [i.strip(',').strip('"').strip('\n') for i in re.findall('[^",]*[,\n]|".*"[,\n]', line)] + [str(counter)] # This splits the line and so that the values are sperate
        else:
            x = [i.strip(',').strip('"').strip('\n') for i in re.findall('[^",]*[,\n]|".*"[,\n]', line)]
        temp.append(x)
        counter += 1
    file.close()
    return temp

'''
Takes the column name and coverts it too a column number based on the name of the column in data
'''
def nameToColumn(data, name):
    for i in data[0]:                                                                               # Iterates through the header of data
        if i.lower() == name.lower():
            return data[0].index(i)                                                                 # Returns the number of the column
    raise AttributeError(f"{name} is not a valid column")                                           # Raises and error if the user enters an invalid column


'''
Take a
List of data
number of a column
the comparator that should be used
what that column should be compared to
and it returns the data with only the values that pass the test
'''
def compare(data, columnNum, val, comparitor):
    temp = []
    '''
    The program itself is simple, it just checks what the comparator is and then compares the data with that comparator
    If the comparator is = or != the data is lowered and if it is < or > the program attemps to convert the data to ints
    it returns and error if the users data can be converted to an int
    I only documented only the first evaluation because the rest are the same except for the try except which is used if the < or > is used and the values can't be converted to a string
    '''
    if comparitor == "=":                                                                           # Evaluates the comparitor
        for i in data:
            if i[columnNum].lower() == val.lower():                                                 # Evaluates the value
                temp.append(i)                                                                      # Appends to the output list if the comparitor is true
        return temp                                                                                 # Returns only the data that fit the conditions
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
        raise AttributeError(f"{comparitor} is not a valid comparitor\n use either =, !=, <, or >")


'''
Append adds information to the end of a file
Input format:
filename, column1value, column2, value and so on

If the value for a column contains spaces you must surround it in double quotes

'''
def APPEND(statement):
    inputString = re.findall('[^," ]+|".+"', statement)                                             # Splits the statement into parts
    inputString = [i.strip('"') for i in inputString]
    file = open(inputString[0], 'a')                                                                # Opens the file in append mode
    temp = ""                                                                                       # Creates a temp variable to store the string to be appened to the csv
    '''
    This next block of code converts the data into csv format
    '''
    for i in inputString[1:]:                                                                       # Iterats through the user input excluding the filepath
        if " " in i:                                                                                # If the user inout contains a space it adds double quotes around the input before it adds it to temp
            temp += ',"'+i+'"'                                                                      # A comma is always added before the string is added
        else:                                                                                       # The else statement deals with values that don't include spaces
            temp += ","+i
    temp = temp[1:] +'\n'                                                                           # Remove the first comma and adds a new line with the escape character
    file.write(temp)                                                                                # Appends the line to the end of the file and closes the file
    file.close()


'''
Input format:
Line filepath
Deletes a line from a CSV file
'''
def DELETE(statement):
    inputString = re.findall('[^," ]+|".+"', statement)                                             # Splits the statement into parts
    inputString = [i.strip('"') for i in inputString]
    data = toList(inputString[1], columnNums=False)                                                 # Converts data to a list
    line = int(inputString[0])                                                                      # Parses line from input string
    data.pop(line)                                                                                  # Removes the line from the data list
    temp2 = ""                                                                                      # Creates a temp variable for converting the list to CSV format(I know I should have made this its own function but I just copy and pasted it)
    'Converts the data to a csv format by iterating through the string, creating each line and then appending to a final string to be written to the CSV'
    for i in data:                                                                                  # Iterates through the data
        temp = ""                                                                                   # Temp variable stores each line for each iteration
        for j in i:                                                                                 # Iterates through each item in the line
            if " " in j:                                                                            # Uses quotes if the item has a space in it
                temp += ',"'+j+'"'
            else:
                temp += ","+j
        temp = temp[1:] +'\n'                                                                       # Removes the first comma and adds a new line character before appending
        temp2+=temp                                                                                 # Adds the temp string to the final output string
    file = open(inputString[1], 'w')                                                                # Writes the string in correct format to the csv
    file.write(temp2)
    file.close()                                                                                    # Closes the file after writing

'''
Input format:
line, column, filepath, value
'''
def UPDATE(statement):
    inputString = re.findall('[^," ]+|".+"', statement)                                             # Splits the statement into parts
    inputString = [i.strip('"') for i in inputString]
    data = toList(inputString[2], columnNums=False)                                                 # Converts the CSV to list
    line = int(inputString[0])                                                                      # Parses line from string
    column = nameToColumn(data, inputString[1])                                                     # finds the number of the column for the column the user specified
    data[line][column] = inputString[3]                                                             # Changes the data in the place the user specified to the value the user wanted
    """
    Same List to CSV convertion as in the DELETE functions
    Again, I relize in hindsight that I should have made this a function
    """
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