from basic import *
import json
import requests as rq
import pyscreenshot as ImageGrab
from bs4 import BeautifulSoup as bs
# import datetime as dt
import wikipedia 
import webbrowser
import os,sys,ctypes
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pyautogui,random
# import smtplib


def takePicture():
    curdt=dt.datetime.now()
    curdt=curdt.strftime("%Y-%m-%d %H:%M:%S").replace(':','-')
    # print(curdt)

    im = ImageGrab.grab()  # X1,Y1,X2,Y2
    try:
        os.mkdir('img')
    except FileExistsError:
        os.chdir('img\\')
    im.save(curdt+'.png')
    speak('Photo Saved')

def sendEmail(to, content):
    # server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.ehlo()
    # server.starttls()
    # server.login('username@gmail.com', 'pass')
    # print(to)
    # server.sendmail('username@gmail.com', to, content)
    # server.close()
    pass



def listcommands():
    speak('Here are the list of commands for operation')
    print('Say Capture to take a scrrenshot')
    print('Say new or headline to listen to top 10 headlines')
    print('Say whoami to listen to some intresting facts')
    print('Say Open Google to open Google.com')
    print('Say Open Youtube to open Youtube.com')
    print('Say Send Email  to send mail')
    # print('Say Show Mail  to Receive mail')
    print('Say Read Newspaper  to Read the newspaper')
    print('Say Set Remainder or create event  to set a remainder/create event ')
    print('Say anyname of person/thing object along with wikipedia to get a short desciption\n example Rose Wikipedia')
    print('Say Lock PC to lock the pc')
    print('Say Exit,Stop or bye to Shutdown Jarvis Program')
    print('Say Open Code to open VSCODE')
    print('Say Open Stackoverflow to open StackOverflow')
    print('Say Play Music to Play Music')
    print('Say Picture or Selfie to click a selfie')
    print('Say Change Desktop to change desktop wallpaper')
    print('Say Battery to know the battery status')
    print('Say what is the weather to know the weather information')
    print("Say What's the time to Show the current time")
    # print("Say Open whatsapp, to send messages")
    # print("Extras:\n")
    # print('After opening youtube through jarvis, you can do the following command')
    # print('Download Vide: To download the currently opened Video Page of youtube')
    # print('Download playlist: To download the complete playlits but you have to nagivate to the playlist page manually')

def wikip(query):
    speak('Searching Wikipedia...')
    query = query.replace("wikipedia", "")
    results = wikipedia.summary(query, sentences=2)
    speak("According to Wikipedia")
    print(results)
    speak(results)


def yt():
    pass
            # webbrowser.open("youtube.com")
            # webbrowser.open_new_tab("youtube.com")
    

def ttm():
    # strTime = dt.datetime.now().strftime("%H:%M:%S")  
    strTime=dt.datetime.now().strftime("%I:%M%p on %B %d, %Y")  
    print(dt.datetime.today().strftime("%A"),strTime)
    # speak()
    speak(f"Today is {dt.datetime.today().strftime('%A')} {strTime}")

def ggl():
    speak('Opening Google, Sir')
    webbrowser.open_new_tab("google.com")

def sovfl():
    speak('Opening Stack Overflow sir')
    webbrowser.open_new_tab("stackoverflow.com")  

def playmusic():
    music_dir = 'D:\\Non Critical\\songs\\Favorite Songs2'
    songs = os.listdir(music_dir)
    print(songs)    
    os.startfile(os.path.join(music_dir, songs[0]))

def code():
    codePath = "C:\\Users\\Mohit\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
    try:
        os.startfile(codePath)
        speak("Opened VSCode Successfully")
        pass
    except Exception:
        speak('Operation failed Please check the following issues')
        print('VS Code not found! ')
        print('Either VScode Not installed or correct path of vs code is not provided/set')
    
def gcal():
    pass

def lckpc():
    speak('PC Locked Successfully')
    ctypes.windll.user32.LockWorkStation()

def whatsapp(l,msg):
    web = webdriver.Chrome("C:\\Users\\Mohit\\Desktop\\lco\\Learning-ML\\project\\Assitant\\binaries to pack\\chromedriver.exe")
    speak('Scan the qr code')
    web.get('http://web.whatsapp.com')
    time.sleep(10)
    pyautogui.hotkey('shift', 'win', 'down')
    elem = web.find_element_by_tag_name('Input')
    elem.click()
    for i in l:
        elem.send_keys(i)
        elem.send_keys(Keys.RETURN)
        elem1 = web.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]')
        elem1.send_keys(msg)
        elem1.send_keys(Keys.RETURN)
    web.close()

def chage_desk():
    SPI_SETDESKWALLPAPER = 20
    path="C:/Users/Mohit/Desktop/Images/"+str(random.randrange(0,10))+'.jpeg'
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER,0,path,0)

def news():
    url = ('https://newsapi.org/v2/top-headlines?''country=in&''apiKey=d030ed2958944d5b9eaaf85dddf96228')
    response = rq.get(url)
    text = response.text
    my_json = json.loads(text)
    speak('The Top 10 Headlines are')
    for i in range(0, 11):
        print(my_json['articles'][i]['title'])
        speak(my_json['articles'][i]['title'])