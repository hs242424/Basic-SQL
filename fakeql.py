import re
from tkinter import HIDDEN

def SELECT(statement):
    x = re.findall("FROM [^ ]+", statement)[0].strip('FROM ').strip("'").strip('"')
    
    if len(x) == 0:
        raise ValueError("You must enter a file path")
    try:
        file = open(x)
    except:
        raise FileNotFoundError(f"Could not find \"{x}\"")

    
    

def APPEND(statement):
    print(statement)

def search():
    print("Yes")

def __search():
    pass
