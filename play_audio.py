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
    #Called when the app is launched directly e.g. via "Alexa, open My Soundtrack"
    card_title = 'Audio Example'
    text = 'Welcome, I can play the perfect soundtrack for every moment of your life. Ask me to play a song for a moment or an activity. Or just say that moment or activity.'
    prompt = 'I didnt get it?what do you want to hear?'
    return question(text).reprompt(prompt).simple_card(card_title, text)

@ask.intent('PlayIntent')
def demo(moments):
    """
    Handles intent requests based on slot value
    """
    #This flag is set to zero when the slot (<moment> variable) matches our database.
    #If the slot is not in our momentsANDmoods database, the flag stays zero and the user is reprompted.
    flag=0

    print (moments)

    available_moments={"dramatic" : "this is so...dramatic"}
    print(available_moments)

    #if something goes wrong when starting playback, the session is ended (see <except> below)
    try:

        if moments == "dramatic":
            speech = 'this is so...dramatic'
            stream_url = get_mp3_urls(moments)
            flag=1
        if moments == "morning":
            speech = 'enjoy your morning!'
            stream_url = get_mp3_urls(moments)
            flag=1
        if moments == "entrance":
            speech = 'ladies and gentlemen..'
            stream_url = get_mp3_urls(moments)
            flag=1
        if moments == "conversation":
            speech = 'lets get some energy!'
            stream_url = get_mp3_urls(moments)
            flag=1
        if moments == "cleaning":
            speech = 'enjoy your cleaning!'
            stream_url = get_mp3_urls(moments)
            flag=1
        if moments == "crowd":
            speech = 'here we go!'
            stream_url = get_mp3_urls(moments)
            flag=1
        if moments == "epic":
            speech = 'this is epic..'
            stream_url = get_mp3_urls(moments)
            flag=1
        if moments == "coffee":
            speech = 'enjoy your coffee..'
            stream_url = get_mp3_urls(moments)
            flag=1
        if moments == "happy":
           speech = 'yessss'
           stream_url = get_mp3_urls(moments)

    except Exception as e:
        speech = 'Sorry I didnt get it. please start over.'
        print(e)
        prompt = 'Are you there?'
        card_title = 'Slot error'
        text = 'invalid slot value'
        flag=1
        return statement(speech).simple_card(card_title, text)

    #<moment> is not a match in our database
    if flag == 0:
        speech = 'Sorry I dont have the ' + moments + ' mood or moment in my database. could you try again?just say the mood or moment and Ill take care of that'
        prompt = 'Are you there?'
        card_title = 'Slot error'
        text = 'invalid slot value'
        flag=1
        return question(speech).reprompt(prompt).simple_card(card_title, text)



    #define time of playback start for PlayMoreIntent
    global t
    t=time.time()
    global globalmoment
    globalmoment=moments
    session.attributes['time']=t

    return audio(speech).play(stream_url, shouldEndSession=True, offset=0)

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

@ask.intent('AMAZON.ResumeIntent')
def resume():
    return audio('Resuming.').resume()

@ask.intent('AMAZON.NextIntent')
def stop():
    return audio('this function is not available.').resume()

@ask.intent('AMAZON.PreviousIntent')
def stop():
    return audio('this function is not available.').resume()

@ask.intent('AMAZON.CancelIntent')
def cancel():
    text='canceling'
    return audio('goodbye').stop()

@ask.intent('AMAZON.HelpIntent')
def cancel():
    card_title= 'helpcard'
    text = 'My soundtrack gives you the perfect soundtrack for every moment. Try to say open my soundtrack for this ... and then the moment or mood you are in!'
    reprompt = 'Hello?WHy dont you try to say open my soundtrack for this ... and then the moment or mood you are in?'
    return question(text).reprompt(prompt).simple_card(card_title,text)

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