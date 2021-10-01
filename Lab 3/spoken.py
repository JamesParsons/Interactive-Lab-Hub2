
from gtts import gTTS
#from playsound import playsound
import os

#Message = "Hello"
#speech = gTTS(text="Howdy")
#speech.save('testsound.mp3')
#playsound('testsound.mp3')

text = "Hello!"
tts = gTTS(text, lang='en')
tts.save("hi.mp3")

os.system("mpg321 hi.mp3")