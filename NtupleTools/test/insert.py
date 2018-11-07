import sys
inFile = sys.argv[1]
outFile = sys.argv[2]

processedLines = []

with open(inFile,'r') as i:
    lines = i.readlines()

st = """--site-requirements='OpSysAndVer == "sl6"' """

#st = """--site-requirements='OpSysAndVer == "sl6"' --memory-requirements=6000 --vsize-limit=6000 """

#st = """--memory-requirements=6000 --vsize-limit=6000 """

print st

for line in lines:
    index = line.find('--input-files-per-job=1')
    if index!=-1:
        output_line = line[:index] + st + line[index:]
        processedLines.append(output_line)
    else:
        processedLines.append(line)

with open(outFile,'w') as o:
    for line in processedLines:
        o.write(line)
