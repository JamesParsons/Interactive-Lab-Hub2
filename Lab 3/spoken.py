
from gtts import gTTS
from playsound import playsound

Message = "Hello"
speech = gTTS(text="Howdy")
speech.save('testsound.mp3')
playsound('testsound.mp3')


