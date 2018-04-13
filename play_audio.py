import logging
import os
from utils import *

from flask import Flask, json, render_template
from flask_ask import Ask, request, session, question, statement, context, audio, current_stream

app = Flask(__name__)
ask = Ask(app, "/")
logger = logging.getLogger()
logging.getLogger('flask_ask').setLevel(logging.INFO)

@ask.launch
def launch():
    get_mp3_urls()
    card_title = 'Audio Example'
    text = 'Welcome to an audio example. What do you want to hear?'
    prompt = 'I didnt get it?what do you want to hear?'
    return question(text).reprompt(prompt).simple_card(card_title, text)

@ask.intent('PlayIntent')
def demo(genre, moments):



    if moments=="entrance":
        speech='it works, you called the playintent with the my entrance slot!'
        stream_url = 'https://feeds.soundcloud.com/stream/427589469-user-734136599-thechno-1.mp3'
    if genre=="techno":
        speech = "here is your {} track".format(genre)
        stream_url = 'https://feeds.soundcloud.com/stream/427589469-user-734136599-thechno-1.mp3'
    if genre=="acoustic":
        speech = "here is your {} track".format(genre)
        stream_url = 'https://feeds.soundcloud.com/stream/426580746-user-734136599-overtune.mp3'
    if genre=="jazz":
        speech = "here is your {} track".format(genre)
        stream_url = 'https://feeds.soundcloud.com/stream/423921354-user-734136599-fremito.mp3'
    return audio(speech).play(stream_url, offset=0)

@ask.intent('AMAZON.PauseIntent')
def pause():
    return audio('Paused the stream.').stop()

@ask.intent('AMAZON.ResumeIntent')
def resume():
    return audio('Resuming.').resume()

@ask.intent('AMAZON.StopIntent')
def stop():
    return audio('stopping').clear_queue(stop=True)

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