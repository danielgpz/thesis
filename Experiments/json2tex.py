import json, json2latex, sys

json_files = sys.argv[1:-2]
name, tex_file = sys.argv[-2:]

def process(obj):
	if isinstance(obj, dict):
		return {key:process(val) for key, val in obj.items()}
	elif isinstance(obj, list):
		return [process(elem) for elem in obj]
	elif isinstance(obj, float):
		return round(obj, 2)
	return obj

data = {}

for i, json_file in enumerate(json_files, 1):
	with open(json_file, 'r') as js:
		data.update(process(json.load(js)))


with open(tex_file, 'w') as tex:
    json2latex.dump(name, data, tex)