import speech_recognition as sr 
import transformers
import os 
import re
import playsound 
import datetime 
import webbrowser
import wikipedia
import time
from gtts import gTTS  
from plyer import notification
import spacy
import tkinter as tk
from PIL import Image, ImageTk
from itertools import count, cycle

nlp = spacy.load('en_core_web_sm')
current_path = os.path.dirname(os.path.abspath(__file__)) + "\\"

sentences = [
    "I have a meeting with John next Monday at 2pm in New York.",
    "Remember to buy milk on your way home.",
    "I do not know what to do",
    "Hi, movie tonight at 9PM?",
    "You are looking phenomenal",
    "Call Mom tomorrow at 10am.",
    "Don't forget to submit the report by Friday."
]

reminders = []
final_reminders = []

for sentence in sentences:
    doc = nlp(sentence)

    for entity in doc.ents:
        if entity.label_ in ['DATE', 'TIME', 'GPE', 'EVENT']:
            reminders.append(sentence)
            break

def talk():
    input=sr.Recognizer()
    with sr.Microphone() as source:
        audio=input.listen(source)
        data=""
        try:
            data=input.recognize_google(audio)
            print("Your question is, " + data)
            
        except sr.UnknownValueError:
            print("Sorry I did not hear your question, Please repeat again.")
    
    return data

def check_reminder():
    check_file = os.path.isfile('./reminder.txt')
    if check_file == False:
        lists = open('reminder.txt','w')
        lists.close()
    
    lists = open('reminder.txt','r')
    lines = lists.readlines()
    today1 = datetime.datetime.today()
    today = today1.strftime("%d/%m/%Y")
    n = len(lines)
    i=0
    while i<n:
        if today == lines[i].rstrip():
            text = lines[i+1].rstrip()
            notification.notify(title = 'Reminder for today', message = text, app_name = 'J.U.D.E', timeout = 10)
        else:
            pass
        i = i+1
    
    lists.close()

def set_reminder(sentence):
    respond("\nDo you want to set a reminder for this sentence?")
    respond(sentence)
    
    response = talk().lower()
    if 'yes' in response.lower():
        respond("Reminder set!")
        final_reminders.append(sentence)

    else:
        respond("Reminder not set.")

def is_reminder_time():
    now = datetime.datetime.now().time()
    if (now.hour == 16) and (now.minute == 38):
        return True

    # return now.hour == 20

def check_time():
    if is_reminder_time():
        notification.notify(title = 'Reminder', message = 'Please go through the list of reminders!', app_name = 'J.U.D.E', timeout = 10)
        respond("Hi, here are some potential reminders I want you to go through.")
        
        for reminder in reminders:
            set_reminder(reminder)
            time.sleep(1) 

        respond("That's all for today. Goodbye!")
    else:
        pass

        
def respond(output):
    num=0
    print(output)
    num += 1
    response=gTTS(text=output, lang='en', tld="us")
    file = str(num)+".mp3"
    response.save(file)
    playsound.playsound(file, True)
    os.remove(file)

def command():
    # root.destroy()
    text=talk().lower()
    check_file = os.path.isfile('./name.txt')
    name = ''

    if check_file == False:
        respond("Before I answer that, may I know your name?")
        while(1):
            name=talk().lower()
            if str(name) != 0:
                break
        
        file=open("name.txt","w")
        file.write(name)
        file.close()
        respond("Hello " + name + ".How can I help you?")
        text()
    
    else:
        file=open("name.txt","r")
        name=file.read()
        file.close()

    if "stop" in str(text) or "exit" in str(text) or "bye" in str(text):
        respond("Thank you!")
        file = current_path + "off.wav"
        playsound.playsound(file, True)    
        exit()

    if 'wikipedia' in text:
        respond('Searching Wikipedia')
        text =text.replace("wikipedia", "")
        results = wikipedia.summary(text, sentences=3)
        respond("According to Wikipedia")
        print(results)
        respond(results)

    elif 'time' in text:
        strTime=datetime.datetime.now().strftime("%H:%M:%S")
        respond(f"the time is {strTime}")     

    elif 'search' in text:
        reg_ex = re.search('search (.+)', text)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.google.com/search?q=' + domain
            webbrowser.open(url)
        
    elif 'open google' in text:
        webbrowser.open("google.com")
        respond("Google is open")

    elif 'set reminder' in text:
        respond("What is the reminder?")
        sentence = talk()
        set_reminder(sentence)
        respond("Reminder has been added to the list!")
    
    elif 'reminder' in text:
        respond("Here are your reminders!")
        if(len(final_reminders) == 0):
            respond("You have no reminders set currently!")
        
        else:
            for reminder in final_reminders:
                respond(reminder)

    elif 'open website' in text:
        reg_ex = re.search('open website (.+)', text)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.' + domain + '.com'
            webbrowser.open(url)
            respond("The website is open!")
        else:
            pass
    
    elif 'www' in text:
        reg_ex = re.search('www (.*)', text)
        url = text
        webbrowser.open(url)
        respond("The website is open!")
        
    elif 'shutdown' in text:
        respond("Are you sure you want to shutdown your computer? (yes or no)")
        choice = talk().lower()
        if 'yes' in choice:
            os.system("shutdown /s /t 1")

        elif 'no' in choice:
            respond("Shutting Down!")
                
        else:
            respond("No definitive Answer found")
    
    elif 'restart' in text:
        respond("Are you sure you want to restart your computer? (yes or no)")
        choice = talk().lower()
        if 'yes' in choice:
            os.system("shutdown /r /t 1")

        elif 'no' in choice:
            respond("Restarting!")
                
        else:
            respond("No definitive Answer found")

    elif 'youtube' in text: 
        webbrowser.open("youtube.com")
        respond("Youtube is open")       

    elif 'notify' in text:
        check_reminder()
        with open('reminder.txt','a') as m:
            text = input("Enter the Body:")
            date = input("When do you want to be reminded:")
            m.write('\n')
            m.write(date)
            m.write('\n')
            m.write(text)
            notification.notify(title = 'Reminder', message = 'Reminder has been set!', app_name = 'J.U.D.E', timeout = 10)


    elif "don't make it bad" in text:
        file = current_path + "song.wav"
        playsound.playsound(file, True)    

    else:
        chat = nlp(transformers.Conversation(text), pad_token_id=50256)
        res = str(chat)
        res = res[res.find("bot >> ")+6:].strip()
        respond(res)

if __name__=='__main__':
    nlp = transformers.pipeline("conversational", model="microsoft/DialoGPT-medium")
    os.environ["TOKENIZERS_PARALLELISM"] = "true"

    check_reminder()

    while(1):
        print("\n----------------------------------")
        print("J.U.D.E is Ready")
        print("----------------------------------")

        check_time()
        text=talk().lower()
        
        if "jude" or "dude" in str(text):
            # root.mainloop()
            check_file = os.path.isfile('./initial.txt')
            if check_file == False:
                file=open("initial.txt","w")
                file.write('Configured')
                file.close()
                respond("Hello, I am Jude. From now on, whenever I recognize you, I will play the following sound")
                file = current_path + "wake.mp3"
                playsound.playsound(file, True)
                respond("With that being said, How can I help you today?")
                command()
            
            else:
                file = current_path + "wake.mp3"
                playsound.playsound(file, True)
                command()

        else:
            check_time()
            continue