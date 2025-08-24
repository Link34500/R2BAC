import json

with open("./messages.json") as f:
    translation:dict = json.load(f)

def message(code):
    return translation.get(code,code)