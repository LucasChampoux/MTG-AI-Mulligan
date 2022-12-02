import json
import difflib

jsonFile = open("NamesOnly.json", "r")
newJson = jsonFile.read().replace(",", "").replace("  ", "").splitlines()

for j in newJson:
    print(j)

print(len(newJson))
jsonFile.close()

print(difflib.get_close_matches("[sanctum Weaver 18)", newJson))