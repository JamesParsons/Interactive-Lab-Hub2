
from gtts import gTTS
from playsound import playsound
import os

#Message = "Hello"
#speech = gTTS(text="Howdy")
#speech.save('testsound.mp3')
#playsound('testsound.mp3')

text = "Hello!"
tts = gTTS(text)
#tts.save("hi.mp3")

os.system("user_input.mp3")