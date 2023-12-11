f = open('DNA.txt')

vals = []

for line in f:
    line = line[line.index(':')+1:].strip()
    line = line.replace('-', ' ')
    line = line.replace('  ', '-')
    line = line[:line.index('-')].split()
    for x in line:
        if not x == '37':
            vals.append(x)
f.close()

convertedVals = []

for i in range(0, len(vals)):
    x = int(vals[i], 16) ^ 55
    if x >= 33 and x < 127:
        convertedVals.append(x)

for i in convertedVals:
    print(chr(i), end='')
