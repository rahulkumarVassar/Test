
import csv
l=[]
with open("test.csv", 'r') as cfile:
    reader = csv.DictReader(cfile)
    for row in reader:
        l.append(dict(row))
        print(dict(row))

print("\n")
print(l,"\n")
print(l[2])
print(l[2]['Name'])

cfile.close()




