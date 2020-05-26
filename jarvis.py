from basic import *
import os,sys,ctypes
import datetime as dt
from funcs import *
# from cal import *
# from goggle_auth import *





if __name__ == "__main__":
    
    wishMe()
    print('Say help to get the list of commands')
    while True:
        query = takeCommand().lower()

        if 'help' in query:
            listcommands()

        elif 'wikipedia' in query:
            wikip(query)
        elif 'open youtube' in query:
            yt()
        
        elif 'lock pc' in query and 'how' not in query:
            lckpc()

        elif 'capture' in query or 'screenshot' in query:
            takePicture()
        elif 'who am i' in query:
            whoami()
        elif 'open google' in query:
            ggl()

        elif 'open stackoverflow' in query or 'stack overflow' in query:
           sovfl() 
        elif 'send message' in query or 'whatsapp' in query:
            l=[]
            op='yes'
            # speak('say the name of the receiver')
            while True:
                if 'yes' in op:
                    speak('say the name of the receiver')
                    m=takeCommand()
                    if m != 'None' or m != 'NONE':
                        l.append(m)
                    else:
                        continue
                    speak('Want to add more person?, Say yes to add or say send to send msg')
                    op=takeCommand()
                elif 'send' in op or 'sent' in op:
                    break
                else:
                    pass
                
            speak("What should I say?")
            msg = takeCommand()
            whatsapp(l,msg)
            speak('Message Send Successfully')

        elif 'play music' in query:
            playmusic()

        elif 'the time' in query:
            ttm()

        elif 'open code' in query:
            code()

        elif 'send mail' in query:
            try:
                speak("What should I say?")
                content = takeCommand()    
                to=takeCommand()
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry  unable to send this email")

        elif 'exit' in query or 'stop' in query or 'bye' in query or 'buy' in query:
            speak('Exiting , Have a nice day sir')
            sys.exit()

        elif 'desktop' in query:
            chage_desk()

        elif 'news' in query or 'headline' in query:
            news()

        elif 'reminder'in query or 'event' in query:
            import cal
            if cal.crcal():
                speak('Event Created Successfully')
                speak('You will be notified 1 day before via mail, and ten minutes before the event via popup')
            else:
                speak('There was a problem while creating an event')
        
        elif 'send' in query and 'mail' in query:
            sender='me'
            to=input('Enter the email address of the sender : ')
            sub=input('Enter the subject : ')
            msg_txt=input('Enter the message : ')
            msg=CreateMessage('me',to, sub, msg_txt) #error can be here plz debug
            SendMessage(serviceml, 'me', msg)

        elif 'receive' in query or 'received' in query and 'mail' in query:
            receive_mail()






# TODO: 
#import Selenium
#whatsapp
#gmail send,receive
#youtube
# Voice recorder
# create a file locations.txt to have the location of music folder
# default download folder 
# During First run take the location of these music folder,download folder from the pop up window from the user           
#Create an exe
# put hindi voices and commands 
# ask for language at start
# push the drive link to mohit.ml,github