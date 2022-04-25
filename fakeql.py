import re

def SELECT(statement):
    x = re.findall("FROM [^ ]+", statement)[0].strip('FROM ').strip("'").strip('"')
    
    if len(x) == 0:
        raise ValueError("You must enter a file path")
    try:
        
    print(x)
    
    

def APPEND(statement):
    print(statement)