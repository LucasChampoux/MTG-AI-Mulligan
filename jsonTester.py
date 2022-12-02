import json
import difflib

jsonFile = open("NamesOnly.json", "r")
newJson = jsonFile.read().replace(",", "").replace("  ", "").splitlines()
jsonFile.close()

print(difflib.get_close_matches("=", newJson))