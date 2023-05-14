import sys
import pyttsx3
import webbrowser
import datetime
import wikipedia
import speech_recognition as sr
import requests
import wolframalpha
import requests
import pywhatkit
import pyjokes
from pywikihow import search_wikihow
from playsound import playsound
import os
import time
import json
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from PyQt5.QtCore import*
from PyQt5.QtGui import*
from MORTALUi import Ui_MORTALUi


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wish_Me():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%H:%M:%S")
    if hour >= 0 and hour < 12:
        speak(f"good morning  its {tt}")

    elif hour >= 12 and hour < 16:
        speak("good afternoon")

    elif hour >= 16 and hour < 20:
        speak("good evening")

    else:
        speak("good night")
    speak("i am MORTAL. how can i help you ?")


def mylocation():
    ip_add = requests.get('https://api.ipify.org').text

    url = 'https://get.geojs.io/v1/ip/geo/'+ip_add + '.json'
    geo_q = requests.get(url)
    geo_d = geo_q.json()
    state = geo_d['city']
    country = geo_d['country']
    speak(f"sir you are in {state,country}")
    print(state)


def latestnews():
    api_dict = {"buisness": "https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=f00eb7935f4f4ddba39d0672f2382bdd",
                "entertainment": "https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=f00eb7935f4f4ddba39d0672f2382bdd",
                "health": "https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=f00eb7935f4f4ddba39d0672f2382bdd",
                "science": " https://newsapi.org/v2/top-headlines?country=us&category=science&apiKey=f00eb7935f4f4ddba39d0672f2382bdd",
                "sports": "https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=f00eb7935f4f4ddba39d0672f2382bdd",
                "technology": "https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=f00eb7935f4f4ddba39d0672f2382bdd"

                }
    content = None
    url = None
    speak(
        "Which field news do you want, [business] , [health] , [technology], [sports] , [entertainment] , [science]")
    field = input("Type field news that you want: ")

    for key, value in api_dict.items():
        if key.lower() in field.lower():
            url = value
            print(url)
            print("url was found")
            break
        else:
            url = True
    if url is True:
        print("url not found")

    news = requests.get(url).text
    news = json.loads(news)
    speak("Here is the first news.")

    arts = news["articles"]
    for articles in arts:
        article = articles["title"]
        print(article)
        speak(article)
        news_url = articles["url"]
        print(f"for more info visit: {news_url}")

        a = input("[press 1 to cont] and [press 2 to stop]")
        if str(a) == "1":
            pass
        elif str(a) == "2":
            break


def WolfRamAlpha(query):
    apikey = "TXAG8R-WP44KPWXX9"
    requester = wolframalpha.Client(apikey)
    requested = requester.query(query)

    try:
        answer = next(requested.results).text
        return answer
    except:
        speak("The value is not answerable")


def Calc(query):

    Term = str(query)
    Term = Term.replace("MORTAL", "")
    Term = Term.replace("multiply", "*")
    Term = Term.replace("plus", "+")
    Term = Term.replace("minus", "-")
    Term = Term.replace("divide", "/")

    Final = str(Term)
    try:
        result = WolfRamAlpha(Final)
        print(f"{result}")
        speak(result)

    except:
        speak("The value is not answerable")
    speak("thats all")


class MainThread(QThread):
    def __init__(self):

        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    def takeCommand(self):

        r = sr.Recognizer()
        with sr.Microphone(device_index=1) as source:
            print("LISTENING .......")
            r.pause_threshold = 1

            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            print("RECOGNIZING......")
            query = r.recognize_google(audio, language='en-in')
            print(f" user said {query}\n")

        except Exception as e:
           # print(e)
            #print("say it agqain  .....")
            return "None"
        return query

    def TaskExecution(self):

        wish_Me()
        while True:
            self.query = self.takeCommand().lower()

            if 'wikipedia' in self.query:
                speak('seaarching wikipedia....')
                self.query = self.query.replace("wikipedia", "")
                results = wikipedia.summary(self.query, sentences=2)
                speak("according to wikipedia")
                print(results)
                speak(results)

            elif 'what is your name' in self.query:

                speak("i am mortal ")

            elif 'hello' in self.query:
                speak("hello sir or madam")

            elif 'how are you' in self.query:
                speak("i am fine sir or madam !what about you")

            elif 'good night' in self.query:
                speak("ok sir/madam thank you see you again soon ")

            elif 'you are awesome' in self.query:
                speak("thanks for the complememt")

            elif 'open youtube' in self.query:
                webbrowser.open("youtube.com")

            elif 'open google' in self.query:
                webbrowser.open("google.com")

            elif 'the time' in self.query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"sir the time is {strTime}")

            elif 'play' in self.query:

                speak('playing' + self. query)
                pywhatkit.playonyt(self.query)
                continue

            elif 'search web' in self.query:
                pywhatkit.search(self.query)
                speak("searching result in google")
                continue

            elif 'joke' in self.query:

                speak(pyjokes.get_joke())
                # print(pyjokes.get_joke())
                continue

            elif 'how to' in self.query:

                speak("getting dataa from internet")
                prob = self.query.replace("mortal", "")
                max_result = 1
                how_to_function = search_wikihow(prob, max_result)
                assert len(how_to_function) == 1
                how_to_function[0].print()
                speak(how_to_function[0].summary)

            elif 'alarm' in self.query:
                speak("enter the time  ")
                time = input("enter the time")
                while True:
                    Time_Ac = datetime.datetime.now()
                    now = Time_Ac.strftime("%H:%M:%S")
                    if now == time:
                        speak("time to wakeup sir")
                        playsound('Alarm.mp3')
                        speak("Alarm close")

                    elif now > time:
                        break

            elif 'open notepad' in self.query:
                path = "C:\\Windows\\system32\\notepad.exe"
                os.startfile(path)

            elif 'location' in self.query:

                mylocation()

            elif 'news' in self.query:
                latestnews()

            elif 'calculate' in self.query:
                Calc(self.query)

            elif 'exit me' in self.query:
                speak("ok sir madam see you soon")
                exit()

            elif 'outside temperature is' in self.query:

                var1 = "temperature in faridabad is"
                answer = WolfRamAlpha(var1)
                speak(f"{var1} is {answer}")
                print(answer)
            elif 'temperature in' in self.query:

                var2 = "temperature in"+self.query
                ans = WolfRamAlpha(var2)
                speak(f"{var2} is {ans}")
                print(ans)


startExecution = MainThread()


class Main_gui(QMainWindow):
    def __init__(self):
        super(Main_gui, self).__init__()
        uic.loadUi("MORTALUi.ui", self)  # Load the .ui file
        self.show()
        self.ui = Ui_MORTALUi()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString("hh:mm:ss")
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)


app = QApplication(sys.argv)
mort = Main_gui()
mort.show()
exit(app.exec_())
