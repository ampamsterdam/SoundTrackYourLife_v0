import os
import re

def get_mp3_url():


    with open('feed.txt') as myinput:
        contents=myinput.read()
    mymatch=re.findall(r'http(.+?)mp3',contents)
    allmymatches=['https' + mymatch[x] + 'mp3' for x in range(len(mymatch))]
print(allmymatches)

