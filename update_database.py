import ftplib
import numpy as np
import glob
import os
#import random

#connects to server
ftp = ftplib.FTP('91.184.0.39')
ftp.login("f307123", "8AsREl8I6T7X")

#get list of local directories in the google drive (or any local folder)
homedir='/Users/Copo1/GoogleDrive(jacoposolari@ampamsterdam.com)/SoundtrackerDatabase/database/'
localdirs_roots=glob.glob(homedir+'*')
localdirs_roots=np.sort(localdirs_roots)
localdirs=[x.split('/')[-1] for x in localdirs_roots]
localdirs=np.sort(localdirs)

#get list of remote directories in the eysoundtrack website
targetdir='webspace/httpdocs/eysoundtrack.com/resources/audio/'
remotedirs_roots=ftp.nlst(targetdir)
remotedirs_roots=np.sort(remotedirs_roots)
remotedirs=[x.split('/')[-1] for x in remotedirs_roots]
remotedirs=np.sort(remotedirs)

#check if the local and remote deirectories match
for mydir in localdirs:
    if mydir in remotedirs:
        ''
    #make missing folders
    else:
        try:
            ftp.mkd('webspace/httpdocs/eysoundtrack.com/resources/audio/' + mydir)
            #os.mkdir(homedir + mydir)
        except Exception as e:
            print(e)
            continue
#update the synced db folders
    localdirs_roots=glob.glob(homedir+'*')
    localdirs_roots=[localdirs_roots[x] for x in range(len(localdirs_roots)) if os.path.isdir(localdirs_roots[x])]
    localdirs_roots=np.sort(localdirs_roots)
    localdirs=[x.split('/')[-1] for x in localdirs_roots]
    localdirs=np.sort(localdirs)
    remotedirs_roots=ftp.nlst(targetdir)
    remotedirs_roots=np.sort(remotedirs_roots)
    remotedirs=[x.split('/')[-1] for x in remotedirs_roots]
    remotedirs=np.sort(remotedirs)


#for each local folder, check if there are the same files in the remote corresponding one

localfiles=[[] for x in range(len(localdirs_roots))]
remotefiles=[[] for x in range(len(localdirs_roots))]

for n in range(len(localdirs_roots)):


    try:
        #print(glob.glob(mydir + '/*'))
        files=glob.glob(localdirs_roots[n] + '/*mp3')
        for i in range(len(files)):
            localfiles[n].append(files[i].split('/')[-1])
    except:
        ''
    #print(glob.glob(mydir + '/*'))
    try:
        files=ftp.nlst(remotedirs_roots[n] + '/*mp3')

        for i in range(len(files)):
            remotefiles[n].append(files[i].split('/')[-1])

    except:
        ''

#if there is discrepancy between the local and the remote, upload all the locals
    if localfiles and remotefiles[n]!=localfiles[n]:
        for file in localfiles[n]:
            f=localdirs_roots[n] + '/' + file
            fh=open(f, 'r' )
            ftp.cwd('/' + remotedirs_roots[n] )
            #safety check that yuo are in the correct folder both locally and remotely
            if ftp.pwd().split('/')[-1] == localdirs_roots[n].split('/')[-1]:
                ftp.storbinary('STOR %s'%file , fh) #upload file
            fh.close()
######







