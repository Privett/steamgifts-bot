import json

def read(filename):
    with open(filename, 'r', encoding = 'utf-8') as file:
        return json.load(file)

def write(data, filename):
    data = json.dumps(data)
    data = json.loads(str(data))
    with open(filename, 'w', encoding = 'utf-8') as file:
        json.dump(data, file, indent = 2)