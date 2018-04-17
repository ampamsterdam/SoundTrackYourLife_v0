import logging
import os
from utils import *
import time

from flask import Flask, json, render_template
from flask_ask import Ask, request, session, question, statement, context, audio, current_stream

app = Flask(__name__)
ask = Ask(app, "/")
logger = logging.getLogger()
logging.getLogger('flask_ask').setLevel(logging.INFO)

@ask.launch
def launch():
    #get_mp3_urls()
    card_title = 'Audio Example'
    text = 'Welcome, what do you want to hear?'
    prompt = 'I didnt get it?what do you want to hear?'
    return question(text).reprompt(prompt).simple_card(card_title, text)

@ask.intent('PlayIntent')
def demo(moments):

    if moments == "morning":
        speech = 'enjoy your morning!'
        stream_url = 'https://www.eysoundtrack.com/resources/audio/morning.mp3'
    if moments == "entrance":
        speech = 'ladies and gentlemen..'
        stream_url = 'https://www.eysoundtrack.com/resources/audio/entrance.mp3'
    if moments == "boring":
        speech = 'lets get some energy!'
        stream_url = 'https://www.eysoundtrack.com/resources/audio/conversation.mp3'
    if moments == "cleaning":
        speech = 'enjoy your cleaning!'
        stream_url ='https://www.eysoundtrack.com/resources/audio/cleaning.mp3'
    if moments == "crowd":
        speech = 'here we go!'
        stream_url ='https://www.eysoundtrack.com/resources/audio/crowd.mp3'
    if moments == "epic":
        speech = 'this is epic..'
        stream_url ='https://www.eysoundtrack.com/resources/audio/epic.mp3'

    global t=time.time()
    return audio(speech).play(stream_url, offset=0)

@ask.intent('PlayIntentMore')
def demo2(moments,t):
    print(t)

@ask.intent('AMAZON.PauseIntent')
def pause():
    return audio('Paused the stream.').stop()

@ask.intent('AMAZON.ResumeIntent')
def resume():
    return audio('Resuming.').resume()

@ask.intent('AMAZON.StopIntent')
def stop():
    return audio('stopping').clear_queue(stop=True)

@ask.intent('AMAZON.CancelIntent')
def cancel():
    text='canceling'
    return statement(text)

# optional callbacks
@ask.on_playback_started()
def started(offset, token):
    _infodump('STARTED Audio Stream at {} ms'.format(offset))
    _infodump('Stream holds the token {}'.format(token))
    _infodump('STARTED Audio stream from {}'.format(current_stream.url))

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