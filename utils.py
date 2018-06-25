
import ftplib
import random
import pickle


def get_mp3_urls(moments, more=0):

#connect to the ftp server and lists the tracks names in the database
    ftp = ftplib.FTP("91.18a4.0.39",21)
    ftp.login("f307123", "8AsREl8I6T7X")
    # ftp = ftplib.FTP(pickle.load(open('config.pkl', 'rb'))['a'])
    # ftp.login(pickle.load(open('config.pkl', 'rb'))['b'], pickle.load(open('config.pkl', 'rb'))['c'])

    if more == 0:
        urls=ftp.nlst('webspace/httpdocs/eysoundtrack.com/resources/audio/' + moments)
        randomfile=random.choice(urls)
        randomurl='https://www.eysoundtrack.com/resources/audio/' + moments + '/' + randomfile.split('/')[-1]

    if more == 1:
        urls=ftp.nlst('webspace/httpdocs/eysoundtrack.com/resources/audio/' + moments + 'more' )
        randomfile=random.choice(urls)
        randomurl='https://www.eysoundtrack.com/resources/audio/' + moments + 'more'  + '/' + randomfile.split('/')[-1]

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

def make_ftp_folders():
    ftp = ftplib.FTP("91.184.0.39")
    ftp.login("f307123", "8AsREl8I6T7X")

    available_moments = {'adventures': '',
                         'afternoon': '',
                         'answering': '',
                         'applause': '',
                         'audience': '',
                         'autumn': '',
                         'awkward': '',
                         'bathroom': '',
                         'birthday': '',
                         'boring': '',
                         'brainstorm': '',
                         'brandnew': '',
                         'cleaning': 'enjoy your cleaning',
                         'coffee': '',
                         'colleagues': '',
                         'conference ': '',
                         'critical': '',
                         'crowd': '',
                         'crowded': '',
                         'cute': '',
                         'day': '',
                         'de-stressing': '',
                         'deadline': '',
                         'desk': '',
                         'door': '',
                         'dramatic': 'enjoy the drama..',
                         'driving ': '',
                         'earbuds': '',
                         'email': '',
                         'ending ': '',
                         'entry': 'ladies and gentlemen, prepare for this entrance',
                         'entrance': 'ladies and gentlemen, prepare for this entrance',
                         'epic': '',
                         'evening': '',
                         'extraspecial': '',
                         'fail': '',
                         'fancy': '',
                         'funny': '',
                         'garden': '',
                         'great': '',
                         'happy': '',
                         'headphones': '',
                         'hilarious': '',
                         'holliday': '',
                         'ideas': '',
                         'important': '',
                         'inbox': '',
                         'job': '',
                         'kitchen': '',
                         'lame': '',
                         'leaving ': '',
                         'lines': '',
                         'lunch': '',
                         'lunchbox': '',
                         'meeting': '',
                         'morning': '',
                         'nap': 'good night',
                         'new': '',
                         'noisy': '',
                         'notes': '',
                         'office': '',
                         'package': '',
                         'payday': '',
                         'phone': '',
                         'phonecall': '',
                         'plants': '',
                         'postit ': '',
                         'presentation': '',
                         'printer': '',
                         'promotion': 'you rule!',
                         'relaxing': '',
                         'reviewing': '',
                         'ruling': '',
                         'run': '',
                         'sad': '',
                         'sandwich': '',
                         'school': '',
                         'server': '',
                         'slide': '',
                         'spring': '',
                         'stapling': '',
                         'starting': '',
                         'stupid': '',
                         'summer': '',
                         'tape': '',
                         'tasks': '',
                         'tea': '',
                         'thinking': '',
                         'timesheets': '',
                         'toilet': '',
                         'typing': '',
                         'week': '',
                         'window': '',
                         'winter': '',
                         'work': '',
                         'writing': '',
                         'you': ''}


    for moments in available_moments.keys():
        try:
            ftp.mkd('webspace/httpdocs/eysoundtrack.com/resources/audio/' + moments)
        except Exception as e:
            print(e)
            continue

