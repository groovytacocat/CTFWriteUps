# Reverse Engineering - Windows of Opportunity

>You've located a zombie hideout and are trying to peek inside. Suddenly, a window opens a crack and a zombie peers out - they want a password...

As with One Step Closer an additional file was given that would be "helpful" to solving the challenge, this case [windows](./windows)

Running the file command shows that windows is a 64-bit not-stripped ELF.

Attempting to run windows gives you the prompt:

>A voice comes from the window... 'Password?'

Giving inputs that aren't the flag will return "The window slams shut...". Checking it with strings and binwalk don't show anything interesting either. Time to dump this in a decompiler!

Tossing this into IDA and looking at main shows:

```C
int __fastcall main(int argc, const char **argv, const char **envp)
{
  char s[43]; // [rsp+0h] [rbp-30h] BYREF
  char v5; // [rsp+2Bh] [rbp-5h]
  unsigned int i; // [rsp+2Ch] [rbp-4h]

  puts("A voice comes from the window... 'Password?'");
  fgets(s, 42, stdin);
  for ( i = 0; i <= 0x24; ++i )
  {
    v5 = s[i] + s[i + 1];
    if ( v5 != arr[i] )
    {
      puts("The window slams shut...");
      return -1;
    }
  }
  puts("The window opens to allow you passage...");
  return 0;
}
```

Here we see that the program takes the input and sums 2 of the characters at a time and compares them to an array of stored values. Digging around further in IDA I found the array containing the values to be checked against, I took these values converted them from hex to decimal then loaded the values into a [text file](./nums.txt).

The logic for this is that each value in the decompiler array is equal to the sum of 2 characters in the flag, however the for loop in main increments by 1 and not 2 so arr[0] = flag[0] + flag[1] and arr[1] = flag[1] + flag[2]. Meaning each letter is the value in the decompiler array minus the previous letter in the string. 

Using H as the first letter since all the flags are of the form HTB{the flag} which corresponds to 72 as an integer, I wrote a [small python program](./solve.py) to read those numbers in and obtain the flag: 

```python
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
```

Running the above gives you:
>HTB{4_d00r_cl0s35_bu7_4_w1nd0w_0p3n5!}
