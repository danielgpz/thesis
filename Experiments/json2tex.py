import json, sys

json_files = sys.argv[1:-2]
name, tex_file = sys.argv[-2:]

data = {}

for i, json_file in enumerate(json_files, 1):
	with open(json_file, 'r') as js:
		for image, info in json.load(js).items():
			if image in data:
				data[image].update(info["iterations"])
			else:
				data[image] = info["iterations"]

headers = ["1", "2", "3", "TELEA", "NS"]
rows = []

for image, iters in data.items():
	vals = [iters[h]["psnr"] for h in headers]
	maxval = max(vals)
	minval = min(vals)
	rowstr = " & ".join([('\\textcolor{#3}{%.2f}' if val == maxval else ('\\textcolor{#4}{%.2f}' if val == minval else '%.2f'))%round(val, 2) for val in vals])
	rows.append('\\texttt{\\detokenize{%s}} & %s\\\\' % (image, rowstr))

rowsstr = '\n'.join(rows)

tex_code = '''\\makeatletter\\newcommand\\%s[4]{
\\begin{table}[H]\\centering\\begin{tabular}{p{4cm}ccccc}\\hline
Imagen & Iteraci\\\'on 1 & Iteraci\\\'on 2 & Iteraci\\\'on 3 & \\textbf{TELEA} & \\textbf{NS} \\\\\\hline
%s\\hline
\\end{tabular}\\caption{#1}\\label{#2}\\end{table}
}\\makeatother'''

with open(tex_file, 'w') as tex:
    tex.write(tex_code % (name, rowsstr))