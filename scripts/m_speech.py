#!/usr/bin/env python
from gtts import gTTS
import os
import subprocess

class Speech(object):
    def __init__(self):
        self.mname = "[SPEECH] "
        self.FNULL = open(os.devnull, 'w')


    def play(self,f):
        subprocess.call(["mpg321", f], stdout=self.FNULL, stderr = subprocess.STDOUT)

    def say(self, what):
        print(what)
        tts = gTTS(text=what, lang='en-uk')
        tts.save("speech.mp3")
        self.play("speech.mp3")

    def beep(self):
        print(self.mname + "Beeping")
        self.play("sound/ap-success.mp3")

    def prompt(self):
        print(self.mname + "Prompt")
        self.play("sound/hw-insert.mp3")