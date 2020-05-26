import pyttsx3 
import speech_recognition as sr 
import datetime as dt
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

NAME='Mohit'

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def whoami():
    speak('You are my master sir ')
    speak('Your name is {}'.format(NAME))

def wishMe():
    hour = int(dt.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<17:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("Hello I am Jarvis, How may I help you")       

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")

    except Exception:
        # print(e)    
        print("Say that again please...")  
        speak("Say that again please...")  
        query='None'
    return query