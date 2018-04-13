import os
import re
import numpy as np

def get_mp3_urls():

    with open('feed.txt') as myinput:
        contents=myinput.read()
    mymatch=re.findall(r'http(.+?)mp3',contents)
    allmymatches=['https' + mymatch[x] + 'mp3' for x in range(len(mymatch))]

    myfile=open('urls.txt','wr')
    myfile.writelines(["%s \n"%allmymatches[x] for x in range(len(allmymatches))])
    myfile.close()

    return 0
