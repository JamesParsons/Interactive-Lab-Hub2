
import pyttsx3

engine = pyttsx3.init()




# RATE
rate = engine.getProperty('rate')
engine.setProperty('rate', 80)   # slower is lower number

# VOICE
voices = engine.getPRoperty('voices')
#engine.setProperty('voice', voices[0].id) #male
engine.setProperty('voice', voices[1].id) #female




engine.say("Hello say ler.  it is ok if people call you james")
engine.runAndWait()