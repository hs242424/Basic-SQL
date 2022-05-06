import fakeql as fql

# SELECT('Column FROM "path to csv" WHERE (column number or "name")')

x = fql.SELECT('Age, Survived FROM data.csv where [Survived = 1]')

for i in x:
    print(i)
