import ftplib
import numpy as np
import glob
import os
#import random

ftp = ftplib.FTP('91.184.0.39')
ftp.login("f307123", "8AsREl8I6T7X")

homedir='/Users/Copo1/Google Drive (jacoposolari@ampamsterdam.com)/SoundtrackerDatabase/database/'
localdirs_roots=glob.glob(homedir+'*')
localdirs_roots=np.sort(localdirs_roots)
localdirs=[x.split('/')[-1] for x in localdirs_roots]
localdirs=np.sort(localdirs)

print(localdirs)

targetdir='webspace/httpdocs/eysoundtrack.com/resources/audio/'
remotedirs_roots=ftp.nlst(targetdir)
remotedirs_roots=np.sort(remotedirs_roots)
remotedirs=[x.split('/')[-1] for x in remotedirs_roots]
remotedirs=np.sort(remotedirs)
print(remotedirs)

for mydir in localdirs:

    if mydir in remotedirs:
        print(mydir + ' is online')
    else:
        print(mydir + ' is OFFLINE')
        try:
            ftp.mkd('webspace/httpdocs/eysoundtrack.com/resources/audio/' + mydir)
        except Exception as e:
            print(e)
            continue
    localdirs_roots=glob.glob(homedir+'*')
    localdirs_roots=np.sort(localdirs_roots)
    localdirs=[x.split('/')[-1] for x in localdirs_roots]
    localdirs=np.sort(localdirs)
    remotedirs_roots=ftp.nlst(targetdir)
    remotedirs_roots=np.sort(remotedirs_roots)
    remotedirs=[x.split('/')[-1] for x in remotedirs_roots]
    remotedirs=np.sort(remotedirs)






