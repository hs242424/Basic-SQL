import fakeql as fql

# SELECT('Column FROM "path to csv" WHERE (column number or "name")')

x = fql.SELECT('* FROM data.csv where survived = 0 and sex = male')

for i in x:
    print(i)
