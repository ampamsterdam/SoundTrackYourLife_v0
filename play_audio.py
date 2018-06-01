import logging
import os
from utils import *
import time

from flask import Flask, json, render_template
from flask_ask import Ask, request, session, question, statement, context, audio, current_stream, convert_errors

app = Flask(__name__)
ask = Ask(app, "/")
logger = logging.getLogger()
logging.getLogger('flask_ask').setLevel(logging.INFO)

@ask.launch
def launch():
    if session['application']['applicationId'] == 'amzn1.ask.skill.d236f4f0-8062-42bf-b5cd-61b62e3e5bc8':
        #Called when the app is launched directly e.g. via "Alexa, open My Soundtrack"
        card_title = 'Welcome to The Soundtracker!'
        text = 'Welcome, I can play the perfect soundtrack for every moment of your life. Ask me to play a song for a moment or an activity. Or just say that moment or activity.'
        prompt = 'I didnt get it?what do you want to hear?'
        return question(text).reprompt(prompt).simple_card(card_title, text)
    else:
        return statement('Sorry, your request to the Alexa service comes from an unidentified source.')

@ask.intent('PlayIntent')
def demo(moments):
    """
    Handles intent requests based on slot value
    """
    if session['application']['applicationId'] == 'amzn1.ask.skill.d236f4f0-8062-42bf-b5cd-61b62e3e5bc8':

        #This flag is set to zero when the slot (<moment> variable) matches our database.
        #If the slot is not in our momentsANDmoods database, the flag stays zero and the user is reprompted.
        flag=0

        print (moments)

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

        built_ins=['exit','quit','enough','shut up','shut down']
        #
        # if moments in built_ins:
        #     return statement('quitting').simple_card('quit', 'byebye')

        #if something goes wrong when starting playback, the session is ended (see <except> below)
        try:
            if moments in available_moments.keys():
                 speech = available_moments[moments]
                 stream_url = get_mp3_urls(moments)
                 card_title = 'Artist:'
                 text = 'Song:'
                 flag=1

        except ftplib.error_temp:
            speech = 'mmmh ' + moments + ' is a great moment but I dont have a perfect soundtrack for that. Try a different one.'
            prompt = 'Are you there?'
            card_title = 'Ops..I have no songs for your request.'
            text = 'Could not find a song for your request in The Soundtracker database. But your input will be used to improve the database, so try again in a few days!'
            flag=1
            return question(speech).reprompt(prompt).simple_card(card_title, text)

        except IndexError:
            speech = 'mmmh ' + moments + ' is a great moment but I dont have a perfect soundtrack for that. Try a different one.'
            prompt = 'Are you there?'
            card_title = 'Ops..I have no songs for your request.'
            text = 'Could not find a song for your request in The Soundtracker database. But your input will be used to improve the database, so try again in a few days!'
            flag=1
            return question(speech).reprompt(prompt).simple_card(card_title, text)

        except Exception as e:
            speech = 'Sorry I m having some technical difficulties. Please start over.'
            print(e)
            prompt = 'Are you there?'
            card_title = 'Ops..I have no songs for your request.'
            text = 'Could not find a song for your request in The Soundtracker database. But your input will be used to improve the database, so try again in a few days!'
            flag=1
            return statement(speech).simple_card(card_title, text)

        #<moment> is not a match in our database
        if flag == 0:
            if moments not in built_ins:
                try:
                    speech = 'Sorry I dont have the ' + moments + ' moment in my database. Try a different one!Just say the moment and I will take care of it.'
                except:
                    speech = 'Sorry I dont have that moment in my database, try a different one now.'
                prompt = 'Are you there?'
                card_title = 'Input error'
                text = 'Invalid input value'
                flag=1
                return question(speech).reprompt(prompt).simple_card(card_title, text)
            else:
                print('no available moments in the database.')
                cancel()

        #define time of playback start for PlayMoreIntent
        global t
        t=time.time()
        global globalmoment
        globalmoment=moments
        session.attributes['time']=t

        return audio(speech).play(stream_url, shouldEndSession=True, offset=0).simple_card(card_title, text)

    else:
        return statement('Sorry, your request to the Alexa service comes from an unidentified source.')

@ask.intent('PlayIntentMore')
def demo2(moments,mytime=0):

    offset=t2-t
    print(offset)
    a=audio('').stop()
    a=audio('').clear_queue(stop=True)
    stream_url = get_mp3_urls(globalmoment, more=1) #
    return audio('') .play(stream_url, shouldEndSession=True, offset=offset)

def get_time():
    return t

@ask.intent('AMAZON.PauseIntent')
def pause():
    global t2
    t2=time.time()
    audio('stopping').clear_queue(stop=True)
    card_title = 'pausing'
    text = 'ok, what do you want?'
    prompt = 'I didnt get it?what do you want?'
    return question(text).reprompt(prompt).simple_card(card_title,text)

@ask.intent('AMAZON.ResumeIntent')
def resume():
    return audio('Resuming.').resume()


@ask.intent('AMAZON.NextIntent')
def nexttrack():
    return audio('i m sorry, this function is not available for The Soundtracker.').resume()

@ask.intent('AMAZON.PreviousIntent')
def previous():
    return audio('i m sorry, this function is not available for The Soundtracker.').resume()

@ask.intent('AMAZON.LoopOnIntent')
def loopon():
    return audio('i m sorry, this function is not available for The Soundtracker.').resume()

@ask.intent('AMAZON.LoopOffIntent')
def loopoff():
    return audio('i m sorry, this function is not available for The Soundtracker.').resume()

@ask.intent('AMAZON.ShuffleOnIntent')
def shuffleoff():
    return audio('i m sorry, this function is not available for The Soundtracker.').resume()

@ask.intent('AMAZON.ShuffleOffIntent')
def shuffleon():
    return audio('i m sorry, this function is not available for The Soundtracker.').resume()

@ask.intent('AMAZON.RepeatIntent')
def repeat():
    return audio('i m sorry, this function is not available for The Soundtracker.').resume()

@ask.intent('AMAZON.StartOverIntent ')
def repeat():
    return audio('i m sorry, this function is not available for The Soundtracker.').resume()

@ask.intent('AMAZON.StopIntent')
def stop():
    speech='goodbye'
    card_title='Stopping.'
    text='Goodbye'
    return audio(speech).stop()

@ask.intent('AMAZON.CancelIntent')
def cancel():
    speech='goodbye'
    card_title='Canceling.'
    text='Goodbye'
    return audio(speech).stop()

@ask.intent('AMAZON.Unhandled')
def cancel():
    speech='Sorry, I dont know that.'
    card_title='Unhandled intent.'
    text='This intent is not implemented.'
    return audio(speech).stop()

@ask.intent('AMAZON.HelpIntent')
def help():
    card_title= 'How to use The Soundtracker.'
    text = 'Every moment deserves its own soundtrack. With my soundtrack you can add sound to your everyday life. I will help you with how to use this skill .' \
           'You simply need to tell me:  Alexa, open my soundtrack for.. and tell me what kind of moment you need it for .' \
           'My entry, this happy moment . or .  my boring meeting... you can try it out now. '
    #prompt = 'Hello?WHy dont you try to say open my soundtrack for this ... and then the moment or mood you are in?'
    return statement(text).simple_card(card_title,text)

# optional callbacks
@ask.on_playback_started()
def started(offset, token):
    _infodump('STARTED Audio Stream at {} ms'.format(offset))
    _infodump('Stream holds the token {}'.format(token))
    _infodump('STARTED Audio stream from {}'.format(current_stream.url))
    return

@ask.on_playback_stopped()
def stopped(offset, token):
    _infodump('STOPPED Audio Stream at {} ms'.format(offset))
    _infodump('Stream holds the token {}'.format(token))
    _infodump('Stream stopped playing from {}'.format(current_stream.url))

@ask.on_playback_nearly_finished()
def nearly_finished():
    _infodump('Stream nearly finished from {}'.format(current_stream.url))

@ask.on_playback_finished()
def stream_finished(token):
    _infodump('Playback has finished for stream with token {}'.format(token))


@ask.session_ended
def session_ended():
    print('SESSION ENDED')
    return "{}", 200

def _infodump(obj, indent=2):
    msg = json.dumps(obj, indent=indent)
    logger.info(msg)

if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)