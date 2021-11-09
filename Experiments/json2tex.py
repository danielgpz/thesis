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
sums = [0] * len(headers)
rowsstr = []

for image, iters in data.items():
    vals = [iters[h]["psnr"] for h in headers]
    sums = [s + val for s, val in zip(sums, vals)]
    maxval = max(vals)
    minval = min(vals)
    rowstr = " & ".join([('\\textcolor{#2}{%.2f}' if val == maxval else ('\\textcolor{#3}{%.2f}' if val == minval else '%.2f'))%val for val in vals])
    rowsstr.append('\\texttt{\\detokenize{%s}} & %s\\\\' % (image, rowstr))

n = len(rowsstr)
avgs = [(s/n) for s in sums]
diffs = [avgs[1] - avgs[0], avgs[2] - avgs[1], avgs[2] - avgs[0], avgs[2] - avgs[4], avgs[4] - avgs[0]]

tabstr = '\n'.join(rowsstr)
avgsstr = 'Promedio & %s\\\\' % " & ".join(['%.2f' % avg for avg in avgs])
diffsstr =  '%s\\\\' % " & ".join(['%.2f' % diff for diff in diffs])

tex_code = '''\\makeatletter
\\newcommand\\%s[3]{
\\begin{table}[H]\\centering\\begin{tabular}{p{4cm}ccccc}\\hline
Imagen & Iteraci\\\'on 1 & Iteraci\\\'on 2 & Iteraci\\\'on 3 & \\textbf{TELEA} & \\textbf{NS} \\\\\\hline
%s\\hline
%s\\hline
\\end{tabular}\\caption{#1}\\label{tab:%s}\\end{table}
}
\\newcommand\\%sdiffs[1]{
\\begin{table}[H]\\centering\\begin{tabular}{|c|c|c|c|c|}\\hline
Iters. 2 y 1 & Iters. 3 y 2 & Iters. 3 y 1 & Iter. 3 y \\textbf{NS} & \\textbf{NS} e Iter. 1 \\\\\\hline
%s\\hline
\\end{tabular}\\caption{#1}\\label{tab:%s_diffs}\\end{table}
}
\\makeatother'''

with open(tex_file, 'w') as tex:
    tex.write(tex_code % (name, tabstr, avgsstr, name, name, diffsstr, name))