import random
import time


class Hearing(object):

    def __init__(self, speech):
        self.mname = "[FAKEHEARING] "

    def recognize_speech_from_mic(self, recognizer, microphone):
        print(self.mname +"Recognizing speech")
        return "cool"


    def recognize_answer(self):
        print(self.mname + "A simulated vocal input is required.")
        response = raw_input("Please insert spoken answer manually: \n")
        return response


    def recognize_answer_yn(self):
        response = self.recognize_answer()
        if "yes" in response:
            return True
        elif "no" in response:
            return False
        


'''
if __name__ == "__main__":
	print("Say yes or no")
	res = Hearing().recognize_answer_yn()
	print("YES" if res else "NO")
    
'''