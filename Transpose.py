import csv
r=0 
c=0
k=0




List=[]
def read(file_name):
	global r,c
	with open(file_name,'r') as csvfile:
		File = csv.reader(csvfile)
		for row in File:
			List.append(row)
			#print(row)
			r=r+1
			c=len(row)
	print("%d,%d"%(r,c),"\n")
	for row in List:
		print("\t".join([str(elem) for elem in row]))
	print(List[3],"\n")

read("test1.csv")


List_Invert=[[0]*r for i in range(c)]
def invert(name):
	global k
	for row in name:
		for i in range(len(row)):
			List_Invert[i][k]=row[i]
		k=k+1

	for row in List_Invert:
		print("\t".join([str(elem) for elem in row]))

invert(List)

"""with open('test.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(List_Invert)"""
