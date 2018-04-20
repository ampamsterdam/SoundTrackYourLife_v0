import os
import re
import numpy as np
from ftplib import FTP_TLS

def get_mp3_urls():

    ftp=FTP_TLS()
    ftp.set_debuglevel(2)
    ftp.connect('91.184.0.39', 21)
    ftp.sendcmd('USER f307123')
    ftp.sendcmd('PASS 8AsREl8I6T7X')
    urls=ftp.nlst('webspace/httpdocs/eysoundtrack.com/resources/audio')

    ftp.close()

    myfile=open('urls.txt','wr')
    myfile.writelines(["%s \n"%allmymatches[x] for x in range(len(allmymatches))])
    myfile.close()

    # with open('feed.txt') as myinput:
    #     contents=myinput.read()
    # mymatch=re.findall(r'http(.+?)mp3',contents)
    # allmymatches=['https' + mymatch[x] + 'mp3' for x in range(len(mymatch))]
    #
    # myfile=open('urls.txt','wr')
    # myfile.writelines(["%s \n"%allmymatches[x] for x in range(len(allmymatches))])
    # myfile.close()

    return 0
