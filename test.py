import fakeql as fql

# SELECT('Column FROM "path to csv" WHERE (column number or "name")')

'''
x = fql.SELECT('sex, survived FROM data.csv where survived > 0 and sex = male')

for i in x:
    print(i)

fql.APPEND('data.csv, fda, dsaf,dsf wef, "This is one bit of data"')
'''

fql.UPDATE('2, Survived, data.csv, "Hello There"')