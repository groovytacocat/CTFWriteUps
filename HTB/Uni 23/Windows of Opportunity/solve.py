f = open('nums.txt')

nums = []
for line in f:
    nums.append(int(line))
f.close()

ans = [72]

def mysolve(value):
    letter = value - ans[-1]
    ans.append(letter)
for val in nums:
    mysolve(val)
for x in ans:
    print(chr(x), end = '')

print()
