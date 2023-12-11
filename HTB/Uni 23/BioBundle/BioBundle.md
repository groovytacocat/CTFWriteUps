# Reverse Enginnering - BioBundle

>We've obtained a sample of zombie DNA. Can you extract and decrypt their genetic code - we believe we can use it to create a cure...
>
>Helpful file: [biobundle](./biobundle)

Checking this with file and strings doesn't reveal anything noteworthy just that it's a binary although there are numerous strings in biobundle containing interspersed with other characters.

Decompile time!

```C
int __fastcall main(int argc, const char **argv, const char **envp)
{
  char s[128]; // [rsp+0h] [rbp-90h] BYREF
  unsigned int (__fastcall *v5)(char *); // [rsp+80h] [rbp-10h]
  void *handle; // [rsp+88h] [rbp-8h]

  handle = get_handle();
  v5 = (unsigned int (__fastcall *)(char *))dlsym(handle, "_");
  if ( !v5 )
    return -1;
  fgets(s, 127, stdin);
  s[strcspn(s, "\n")] = 0;
  if ( v5(s) )
    puts("[*] Untangled the bundle");
  else
    puts("[x] Critical Failure");
  return 0;
}
```
Looking at main we see that the program will read a 128 character string from input and then supply that string a parameter for the v5 function. (Thankfully I was working with the competition team leader for the cybersecurity club who helped explain how some of these functions worked/some basics of assembly)

Now to see what the v5 function will do:

```C
void *get_handle()
{
  char buf; // [rsp+Fh] [rbp-1021h] BYREF
  char s[8]; // [rsp+10h] [rbp-1020h] BYREF
  __int64 v3; // [rsp+18h] [rbp-1018h]
  char v4[4080]; // [rsp+20h] [rbp-1010h] BYREF
  void *v5; // [rsp+1018h] [rbp-18h]
  int fd; // [rsp+1024h] [rbp-Ch]
  unsigned __int64 i; // [rsp+1028h] [rbp-8h]

  fd = memfd_create(&unk_2004, 0LL);
  if ( fd == -1 )
    exit(-1);
  for ( i = 0LL; i <= 0x3E07; ++i )
  {
    buf = _[i] ^ 0x37;
    write(fd, &buf, 1uLL);
  }
  *(_QWORD *)s = 0LL;
  v3 = 0LL;
  memset(v4, 0, sizeof(v4));
  sprintf(s, "/proc/self/fd/%d", (unsigned int)fd);
  v5 = dlopen(s, 1);
  if ( !v5 )
    exit(-1);
  return v5;
}
```
Here I see that get_handle()'s for loop starts at 0 and goes to 15789 and XORs the elements in that array with 55 then writes those values out.

Referring back to the strings output with all the 7s and other characters I used `xxd` to get a hexdump of biobundle and located the start/end of the large 7/character block. With these values and the above function, this challenge is solveable!

I copy/pasted the xxd output into a [text file](./DNA.txt) then I wrote the below Python to get the flag!

```Python
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
```

I took the "DNA" and used string manipulation to get the hex values that represented the zombie DNA pieces (I excluded all '37's as there were a large amount of them that won't be useful as 0x37 = 55 in decimal.

Once the relevant values were extracted, they were converted to ints and XOR'd with 55, if the values were ASCII printable (between 33 and 126) and added to a collection of converted values. Once this was completed, just iterate through the converted values and printing their corresponding character which lead to:
>ELF>P@H7@8@.>>.>>888$$Ptd$$QtdRtd.>>GNUNk)M-vywU,F"|__gmon_start___ITM_deregisterTMCloneTable_ITM_registerTMCloneTable__cxa_finalizestrcmplibc.so.6GLIBC_2.2.5\uif>>@@????@HH/HtH5/%/@%/h%/fH=/H/H9tHv/HtH=/H5/H)HH?HHHtHE/HtfD=a/u/UH=&/HtH=B/]h9/]{UHHPH}HHTB{st4tH1c_l1b5_HEHUHbut_c00l3r}HEHUHEHEHEHEHUHEHHHH;$@@hzRx$FJw?;*3$"D\}|ACw\>>o`0r@xoooo>6@GCC:(Debian10.2.1-6)10.2.1202101108`0x@P(>>>?@@(@P!7(@C>jv>@>(@@0|?Y"crtstuff.cderegister_tm_clones__do_global_dtors_auxcompleted.0__do_global_dtors_aux_fini_array_entryframe_dummy__frame_dummy_init_array_entryflag.c__FRAME_END___fini__dso_handle_DYNAMIC__GNU_EH_FRAME_HDR__TMC_END___GLOBAL_OFFSET_TABLE__init_ITM_deregisterTMCloneTablestrcmp@GLIBC_2.2.5__gmon_start___ITM_registerTMCloneTable__cxa_finalize@GLIBC_2.2.5.symtab.strtab.shstrtab.note.gnu.build-id.gnu.hash.dynsym.dynstr.gnu.version.gnu.version_r.rela.dyn.rela.plt.init.plt.got.text.fini.eh_frame_hdr.eh_frame.init_array.fini_array.dynamic.got.plt.data.bss.comment88$.o``$8@00rHoUodnBxxxs~@@PP1$((|>.>.>.?/@0@0(@(00(0'P0+4t\6pttsR

Reading through that output you can see the text: HTB{st4tH1c_l1b5_HEHUHbut_c00l3r} (after a few rounds of testing I'm not sure how to remove them while also printing the entire flag, but flag obtained nonetheless)

Flag:
>HTB{st4t1c_l1b5_but_c00l3r}







