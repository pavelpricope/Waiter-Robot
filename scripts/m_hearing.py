import random
import time

import speech_recognition as sr


class Hearing(object):

    def __init__(self, speech):
        self.mname = "[HEARING] "
        self.PROMPT_LIMIT = 3
        self.UNDETECTED = "0UC"
        self.speech = speech
        self.speech.say("Hey, I don't know how to listen to you. Look at my screen!")
	    mics = sr.Microphone.list_microphone_names()
	    print(10*"\n")
	    print(self.mname + "These microphones were found on your system:")   
	    print(mics)
        self.MIC_INDEX = int(raw_input("An index number is required:"))

    def recognize_speech_from_mic(self, recognizer, microphone):
        print(self.mname +"Recognizing speech")
        """Transcribe speech from recorded from `microphone`.

        Returns a dictionary with three keys:
        "success": a boolean indicating whether or not the API request was
                   successful
        "error":   `None` if no error occured, otherwise a string containing
                   an error message if the API could not be reached or
                   speech was unrecognizable
        "transcription": `None` if speech could not be transcribed,
                   otherwise a string containing the transcribed text
        """
        # check that recognizer and microphone arguments are appropriate type
        if not isinstance(recognizer, sr.Recognizer):
            print(self.mname +"`recognizer` must be `Recognizer` instance")

        if not isinstance(microphone, sr.Microphone):
            print(self.mname +"`microphone` must be `Microphone` instance")

        # adjust the recognizer sensitivity to ambient noise and record audio
        # from the microphone
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            self.speech.prompt()
            audio = recognizer.listen(source, timeout = 8.0)

        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        # try recognizing the speech in the recording
        # if a RequestError or UnknownValueError exception is caught,
        #     update the response object accordingly
        try:
            response["transcription"] = recognizer.recognize_google(audio)
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"

        return response


    def recognize_answer(self):
        recognizer = sr.Recognizer()
        recognizer.dynamic_energy_threshold = False
        microphone = sr.Microphone(device_index=self.MIC_INDEX)
        
        response = self.recognize_speech_from_mic(recognizer, microphone)
        if response["transcription"]:
            return response["transcription"].lower()
        if not response["success"]:
            print(self.mname +"Response failed")
        return self.UNDETECTED


    def recognize_answer_yn(self):
        print(self.mname +"Asking YES or NO")
        answer = False
        for j in range(self.PROMPT_LIMIT):
            response = self.recognize_answer()
            if response == self.UNDETECTED:
                pass
            if "yes" in response:
                return True
            elif "no" in response:
                return False
            else:
                print("I got: " + str(response))
            self.speech.say("I didn't catch that. What did you say?")
            pass
        return False


'''
if __name__ == "__main__":
	sp = Speech()
	hr = Hearing(sp)
	sp.say("Say yes or no")
	res = hr.recognize_answer_yn()
	print("YES" if res else "NO")
	sp.say("Tell me something else")
	sp.beep()
	res = hr.recognize_answer()
	print("I heard you saying: \n"+res)
    
'''
