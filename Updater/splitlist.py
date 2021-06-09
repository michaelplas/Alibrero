import re
import os
import shutil
from shutil import copyfile

with open('splitlist.txt') as sl:
    fstring = sl.readlines()
pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
lst = []
for line in fstring:
    lst.append(pattern.search(line)[0])

count = str(len(lst))
print("Er zitten " + count + " IP's in deze lijst")
aantalscripts = input("Hoeveel scripts wil je tegelijkertijd openen?")

countint = int(count)
aantalscriptsint = int(aantalscripts) - 1

n = countint // aantalscriptsint

final = [lst[i * n:(i + 1) * n] for i in range((len(lst) + n - 1) // n)]

finalstr = '\n'.join(map(str, final))
print(finalstr)
finalfile = open("output.txt", "a")
finalfile.write(finalstr)
finalfile.close()

i = 0
for lst in final:
    finalstr = '\n'.join(map(str, final[i]))
    strcount = str(i)
    i = i + 1
    filename = "iplist.txt"
    directoryname = "Update" + strcount
    f = open(filename, "w")
    f.write(finalstr)
    f.close()
    shutil.copy(filename, directoryname)
