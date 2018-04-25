import os
import re
import numpy as np
from ftplib import FTP_TLS
import ftplib
import random
import numpy as np

def get_mp3_urls(moments, more=0):

#connect to the ftp server and lists the tracks names in the database
    ftp = ftplib.FTP("91.184.0.39")
    ftp.login("f307123", "8AsREl8I6T7X")

    if more == 0:
        urls=ftp.nlst('webspace/httpdocs/eysoundtrack.com/resources/audio/' + moments)
        randomfile=random.choice(urls)
        randomurl='https://www.eysoundtrack.com/resources/audio/' + moments + '/' + randomfile.split('/')[-1]
        print(randomurl)
    if more == 1:
        urls=ftp.nlst('webspace/httpdocs/eysoundtrack.com/resources/audio/' + moments + 'more' )
        randomfile=random.choice(urls)
        randomurl='https://www.eysoundtrack.com/resources/audio/' + moments + 'more'  + '/' + randomfile.split('/')[-1]
        print(randomurl)
    ftp.quit()

#alternatively
    # ftp=FTP_TLS()
    # ftp.set_debuglevel(2)
    # ftp.connect('91.184.0.39', 21)
    # ftp.sendcmd('USER f307123')
    # ftp.sendcmd('PASS 8AsREl8I6T7X')
    # urls=ftp.nlst('webspace/httpdocs/eysoundtrack.com/resources/audio')
    # ftp.close()

#extracts and build the urls to use in the audio player directives
#save them in the url.txt file

    # with open('feed.txt') as myinput:
    #     contents=myinput.read()
    # mymatch=re.findall(r'http(.+?)mp3',contents)
    # allmymatches=['https' + mymatch[x] + 'mp3' for x in range(len(mymatch))]
    #
    #
    # basepath='https://eysoundtrack.com/resources/audio/'
    # myfile=open('urls.txt','wr')
    # myfile.writelines(["%s \n"%basepath + urls[x].split('/')[-1]  for x in range(len(urls))])
    # myfile.close()

    return randomurl
