import re
import os
import shutil
from Resources.delete import deleteUpdater

with open('Resources/splitlist.txt') as sl:
    fstring = sl.readlines()
pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
lst = []
for line in fstring:
    lst.append(pattern.search(line)[0])

count = str(len(lst))
print("Er zitten " + count + " IP's in deze lijst")
aantalscripts = input("Hoeveel scripts wil je tegelijkertijd openen? ")

countint = int(count)
aantalscriptsint = int(aantalscripts)

n = countint // aantalscriptsint

final = [lst[i * n:(i + 1) * n] for i in range((len(lst) + n - 1) // n)]

finalstr = '\n'.join(map(str, final))
print(finalstr)
finalfile = open("Resources/Logging/output.txt", "a")
finalfile.write(finalstr)
finalfile.close()

if os.path.exists('Updater 0'):
    answer = None
    while answer not in ("y", "n"):
        answer = input("PAS OP! Updaters bestaan al. Deze verwijderen en doorgaan ? [y/n] ")
        if answer == "y":
             deleteUpdater()
             continue
        elif answer == "n":
             print("Abort")
             quit()
        else:
            print("Kies alleen y of n")

i = 0
for lst in final:
    finalstr = '\n'.join(map(str, final[i]))
    strcount = str(i)
    i = i + 1
    filename = "ip.txt"
    directoryname = "Updater " + strcount
    os.mkdir(directoryname)
    f = open(filename, "x")
    f.write(finalstr)
    f.close()
    shutil.move(filename, directoryname)
    shutil.copy2("Resources/ipsdone.txt", directoryname)
    shutil.copy2("Resources/start.py", directoryname)
print("Updaters zijn aangemaakt. Gebruik Updater 0 tm "+ strcount + " om te updaten.")

