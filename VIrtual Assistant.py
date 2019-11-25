from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from tkinter import *
import pyttsx3 as pp
import speech_recognition as s
import threading
import random
import re
import sys
from time import sleep
from urllib.request import *
from urllib.error import *
import requests
import json

def send_data_thingspeak(Code):
    fieldid='1'
    writekey='U6DEUI2SRWRL9WHW'
    code=str(Code)
    baseURL = 'http://api.thingspeak.com/update?api_key='+writekey+'&field'+fieldid+'='
    f = urlopen(baseURL+code)	
    print("Sending ",code," to thingspeak")
    retCode = int.from_bytes(f.read(), "big")
    f.close()
    if retCode!=48:
        print("Data sent to cloud succesfully.")
        return 1
    else:
        print("Data could not be sent to cloud.")
        return 0

def read_data_thingspeak(field):
    channelid='917359'
    fieldid=str(field)
    URL='https://api.thingspeak.com/channels/'+channelid+'/fields/'+fieldid+'.json?api_key='
    readkey='CU4W1P240POXKOQP'
    HEADER='&results=1'
    NEW_URL=URL+readkey+HEADER
    print("Contacting URL : ",NEW_URL)
    get_data=requests.get(NEW_URL).json()
    # print(get_data)
    # channel_id=get_data['channel']['id']
    fields=get_data['feeds']
    # print(fields)
    # t=[]
    for x in fields:
        return int(x['field'+fieldid])
# sleep(5)

def speak(word):
    engine.say(word)
    engine.runAndWait()

# takey query : it takes audio as input from user and convert it to string..

def takeQuery():
    sr = s.Recognizer()
    sr.pause_threshold = 1
    print("Your bot is listening, try to speak.")
    with s.Microphone() as m:
        try:
            audio = sr.listen(m)
            query = sr.recognize_google(audio, language='eng-in')
            print(query)
            textF.delete(0, END)
            textF.insert(0, query)
            ask_from_bot()
        except Exception as e:
            print(e)
            print("Could not recognize audio.")

# creating a function
def enter_function(event):
    btn.invoke()

def repeatL():
    while True:
        takeQuery()

def ask_from_bot():
    answers=['Yes I have turned on the light','Ok I\'ll do it for you!','Sure, on it.','Got you, done!']
    errors=["Sorry, I couldn't serve your request.","Sorry, couldn't process your request."]
    q_wordList = ['know','say','tell','inform','status']
    query_str = textF.get()
    query = query_str.split()
    if 'livingroom' in query or ('living' in query and 'room' in query) or 'hall' in query:
        if any(word in query for word in q_wordList):
            if 'light' in query or 'lights' in query:
                if 'on' in query:
                    #read status and give message
                    stat = read_data_thingspeak(1)
                    if stat==1:
                        answer_from_bot='Yes, the living room light is on.'
                    else:
                        answer_from_bot='No, the living room light is off.'
                elif 'off' in query or 'out' in query:
                    #read status and give message
                    stat = read_data_thingspeak(1)
                    if stat==1:
                        answer_from_bot='No, the living room light is on.'
                    else:
                        answer_from_bot='Yes, the living room light is off.'
                else:
                    #error message
                    answer_from_bot=random.choice(errors)
            elif 'fan' in query:
                if 'on' in query:
                    #read status and give message
                    stat = read_data_thingspeak(4)
                    if stat==1:
                        answer_from_bot='Yes, the fan is on.'
                    else:
                        answer_from_bot='No, the fan is off.'
                elif 'off' in query:
                    #read status and give message
                    stat = read_data_thingspeak(4)
                    if stat==1:
                        answer_from_bot='No, the fan is on.'
                    else:
                        answer_from_bot='Yes, the fan is off.'
                else:
                    #error message
                    answer_from_bot=random.choice(errors)
        elif 'light' in query or 'lights' in query:
            if 'is' in query or 'are' in query:
                query_list = [[('is', 'light'), ('is', 'on')], [('are', 'lights'), ('are', 'on')],[('is', 'light'), ('is', 'off')], [('are', 'lights'), ('are', 'off')],[('is', 'light'), ('is', 'out')], [('are', 'lights'), ('are', 'out')]]
                c=0
                for q1,q2 in query_list:
                    c+=1
                    p1 = r".*{}.*{}".format(*q1)
                    p2 = r".*{}.*{}".format(*q2)
                    #read status and give message
                    if re.match(p1, query_str) and re.match(p2, query_str):
                        stat = read_data_thingspeak(1)
                        if c<=2:
                            if stat==1:
                                answer_from_bot='Yes, the living room light is on.'
                            else:
                                answer_from_bot='No, the living room light is off.'
                        else:
                            if stat==1:
                                answer_from_bot='No, the living room light is on.'
                            else:
                                answer_from_bot='Yes, the living room light is off.'
                        break
            elif 'on' in query:
                #send code and give message
                retCode = send_data_thingspeak(101)                
                if retCode==1:
                    answer_from_bot=random.choice(answers)
                else:
                    answer_from_bot="Could not read from cloud, try again in some time."
            elif 'off' in query or 'out' in query:
                #send code and give message
                retCode = send_data_thingspeak(106)                
                if retCode==1:
                    answer_from_bot=random.choice(answers)
                else:
                    answer_from_bot="Could not read from cloud, try again in some time."
            else:
                #error message
                answer_from_bot=random.choice(errors)
        elif 'fan' in query:
            if 'is' in query or 'are' in query:
                query_list = [[('is', 'fan'), ('is', 'on')],[('is', 'fan'), ('is', 'off')]]
                c=0
                for q1,q2 in query_list:
                    c+=1
                    p1 = r".*{}.*{}".format(*q1)
                    p2 = r".*{}.*{}".format(*q2)
                    #read status and give message
                    if re.match(p1, query_str) and re.match(p2, query_str):
                        stat = read_data_thingspeak(4)
                        if c<=1:
                            if stat==1:
                                answer_from_bot='Yes, the fan is on.'
                            else:
                                answer_from_bot='No, the fan is off.'
                        else:
                            if stat==1:
                                answer_from_bot='No, the fan is on.'
                            else:
                                answer_from_bot='Yes, the fan is off.'
                        break
            elif 'on' in query:
                #send code and give message
                retCode = send_data_thingspeak(104)                
                if retCode==1:
                    answer_from_bot=random.choice(answers)
                else:
                    answer_from_bot="Could not read from cloud, try again in some time."
            elif 'off' in query:
                #send code and give message
                retCode = send_data_thingspeak(109)                
                if retCode==1:
                    answer_from_bot=random.choice(answers)
                else:
                    answer_from_bot="Could not read from cloud, try again in some time."
            else:
                #error message
                answer_from_bot=random.choice(errors)
        else:
            #error message
            answer_from_bot=random.choice(errors)
        
    elif 'diningroom' in query or ('dining' in query and ('room' in query or 'hall' in query)) or 'kitchen' in query:
        if any(word in query for word in q_wordList):
            if 'light' in query or 'lights' in query:
                if 'on' in query:
                    #read status and give message
                    stat = read_data_thingspeak(2)
                    if stat==1:
                        answer_from_bot='Yes, the dining room light is on.'
                    else:
                        answer_from_bot='No, the dining room light is off.'
                elif 'off' in query or 'out' in query:
                    #read status and give message
                    stat = read_data_thingspeak(2)
                    if stat==1:
                        answer_from_bot='No, the dining room light is on.'
                    else:
                        answer_from_bot='Yes, the dining room light is off.'
                else:
                    #error message
                    answer_from_bot=random.choice(errors)
            elif 'fan' in query:
                if 'on' in query:
                    #read status and give message
                    stat = read_data_thingspeak(4)
                    if stat==1:
                        answer_from_bot='Yes, the fan is on.'
                    else:
                        answer_from_bot='No, the fan is off.'
                elif 'off' in query:
                    #read status and give message
                    stat = read_data_thingspeak(4)
                    if stat==1:
                        answer_from_bot='No, the fan is on.'
                    else:
                        answer_from_bot='Yes, the fan is off.'
                else:
                    #error message
                    answer_from_bot=random.choice(errors)
        elif 'light' in query or 'lights' in query:
            if 'is' in query or 'are' in query:
                query_list = [[('is', 'light'), ('is', 'on')], [('are', 'lights'), ('are', 'on')],[('is', 'light'), ('is', 'off')], [('are', 'lights'), ('are', 'off')],[('is', 'light'), ('is', 'out')], [('are', 'lights'), ('are', 'out')]]
                c=0
                for q1,q2 in query_list:
                    c+=1
                    p1 = r".*{}.*{}".format(*q1)
                    p2 = r".*{}.*{}".format(*q2)
                    #read status and give message
                    if re.match(p1, query_str) and re.match(p2, query_str):
                        stat = read_data_thingspeak(2)
                        if c<=2:
                            if stat==1:
                                answer_from_bot='Yes, the dining room light is on.'
                            else:
                                answer_from_bot='No, the dining room light is off.'
                        else:
                            if stat==1:
                                answer_from_bot='No, the dining room light is on.'
                            else:
                                answer_from_bot='Yes, the dining room light is off.'
                    break
            elif 'on' in query:
                #send code and give message
                retCode = send_data_thingspeak(102)                
                if retCode==1:
                    answer_from_bot=random.choice(answers)
                else:
                    answer_from_bot="Could not read from cloud, try again in some time."
            elif 'off' in query or 'out' in query:
                #send code and give message
                retCode = send_data_thingspeak(107)                
                if retCode==1:
                    answer_from_bot=random.choice(answers)
                else:
                    answer_from_bot="Could not read from cloud, try again in some time."
            else:
                #error message
                answer_from_bot=random.choice(errors)
        elif 'fan' in query:
            if 'is' in query or 'are' in query:
                query_list = [[('is', 'fan'), ('is', 'on')],[('is', 'fan'), ('is', 'off')]]
                c=0
                for q1,q2 in query_list:
                    c+=1
                    p1 = r".*{}.*{}".format(*q1)
                    p2 = r".*{}.*{}".format(*q2)
                    #read status and give message
                    if re.match(p1, query_str) and re.match(p2, query_str):
                        stat = read_data_thingspeak(4)
                        if c<=1:
                            if stat==1:
                                answer_from_bot='Yes, the fan is on.'
                            else:
                                answer_from_bot='No, the fan is off.'
                        else:
                            if stat==1:
                                answer_from_bot='No, the fan is on.'
                            else:
                                answer_from_bot='Yes, the fan is off.'
                    break
            elif 'on' in query:
                #send code and give message
                retCode = send_data_thingspeak(104)                
                if retCode==1:
                    answer_from_bot=random.choice(answers)
                else:
                    answer_from_bot="Could not read from cloud, try again in some time."
            elif 'off' in query:
                #send code and give message
                retCode = send_data_thingspeak(109)                
                if retCode==1:
                    answer_from_bot=random.choice(answers)
                else:
                    answer_from_bot="Could not read from cloud, try again in some time."
            else:
                #error message
                answer_from_bot=random.choice(errors)
        else:
            #error message
            answer_from_bot=random.choice(errors)
            
    elif 'bedroom' in query or 'room' in query:
        if any(word in query for word in q_wordList):
            if 'light' in query or 'lights' in query:
                if 'on' in query:
                    #read status and give message
                    stat = read_data_thingspeak(3)
                    if stat==1:
                        answer_from_bot='Yes, the bedroom light is on.'
                    else:
                        answer_from_bot='No, the bedroom light is off.'
                elif 'off' in query or 'out' in query:
                    #read status and give message
                    stat = read_data_thingspeak(3)
                    if stat==1:
                        answer_from_bot='No, the bedroom light is on.'
                    else:
                        answer_from_bot='Yes, the bedroom light is off.'
                else:
                    #error message
                    answer_from_bot=random.choice(errors)
            elif 'fan' in query:
                if 'on' in query:
                    #read status and give message
                    stat = read_data_thingspeak(4)
                    if stat==1:
                        answer_from_bot='Yes, the fan is on.'
                    else:
                        answer_from_bot='No, the fan is off.'
                elif 'off' in query:
                    #read status and give message
                    stat = read_data_thingspeak(4)
                    if stat==1:
                        answer_from_bot='No, the fan is on.'
                    else:
                        answer_from_bot='Yes, the fan is off.'
                else:
                    #error message
                    answer_from_bot=random.choice(errors)
        elif 'light' in query or 'lights' in query:
            if 'is' in query or 'are' in query:
                query_list = [[('is', 'light'), ('is', 'on')], [('are', 'lights'), ('are', 'on')],[('is', 'light'), ('is', 'off')], [('are', 'lights'), ('are', 'off')],[('is', 'light'), ('is', 'out')], [('are', 'lights'), ('are', 'out')]]
                c=0
                for q1,q2 in query_list:
                    c+=1
                    p1 = r".*{}.*{}".format(*q1)
                    p2 = r".*{}.*{}".format(*q2)
                    #read status and give message
                    if re.match(p1, query_str) and re.match(p2, query_str):
                        stat = read_data_thingspeak(3)
                        if c<=2:
                            if stat==1:
                                answer_from_bot='Yes, the bedroom light is on.'
                            else:
                                answer_from_bot='No, the bedroom light is off.'
                        else:
                            if stat==1:
                                answer_from_bot='No, the bedroom light is on.'
                            else:
                                answer_from_bot='Yes, the bedroom light is off.'
                    break
            elif 'on' in query:
                #send code and give message
                retCode = send_data_thingspeak(103)                
                if retCode==1:
                    answer_from_bot=random.choice(answers)
                else:
                    answer_from_bot="Could not read from cloud, try again in some time."
            elif 'off' in query or 'out' in query:
                #send code and give message
                retCode = send_data_thingspeak(108)                
                if retCode==1:
                    answer_from_bot=random.choice(answers)
                else:
                    answer_from_bot="Could not read from cloud, try again in some time."
            else:
                #error message
                answer_from_bot=random.choice(errors)
        elif 'fan' in query:
            if 'is' in query or 'are' in query:
                query_list = [[('is', 'fan'), ('is', 'on')],[('is', 'fan'), ('is', 'off')]]
                c=0
                for q1,q2 in query_list:
                    c+=1
                    p1 = r".*{}.*{}".format(*q1)
                    p2 = r".*{}.*{}".format(*q2)
                    #read status and give message
                    if re.match(p1, query_str) and re.match(p2, query_str):
                        stat = read_data_thingspeak(4)
                        if c<=1:
                            if stat==1:
                                answer_from_bot='Yes, the fan is on.'
                            else:
                                answer_from_bot='No, the fan is off.'
                        else:
                            if stat==1:
                                answer_from_bot='No, the fan is on.'
                            else:
                                answer_from_bot='Yes, the fan is off.'
                    break
            elif 'on' in query:
                #send code and give message
                retCode = send_data_thingspeak(104)                
                if retCode==1:
                    answer_from_bot=random.choice(answers)
                else:
                    answer_from_bot="Could not read from cloud, try again in some time."
            elif 'off' in query:
                #send code and give message
                retCode = send_data_thingspeak(109)                
                if retCode==1:
                    answer_from_bot=random.choice(answers)
                else:
                    answer_from_bot="Could not read from cloud, try again in some time."
            else:
                #error message
                answer_from_bot=random.choice(errors)
        else:
            #error message
            answer_from_bot=random.choice(errors)
            
    msgs.insert(END, "you : " + ' '.join(query))
    #print(type(answer_from_bot))
    msgs.insert(END, "bot : " + str(answer_from_bot))
    speak(answer_from_bot)
    textF.delete(0, END)
    msgs.yview(END)

engine = pp.init()
voices = engine.getProperty('voices')
print(voices)
engine.setProperty('voice', voices[1].id) 
main = Tk()
main.geometry("500x650")
main.title("My Chat bot")
#img = PhotoImage(file="bot1.png")
#photoL = Label(main, image=img)
#photoL.pack(pady=5)

frame = Frame(main)
sc = Scrollbar(frame)
msgs = Listbox(frame, width=80, height=20, yscrollcommand=sc.set)
#msgs1 = Listbox(frame, width=80, height=20, yscrollcommand=sc.set)
sc.pack(side=RIGHT, fill=Y)
msgs.pack(side=LEFT, fill=BOTH, pady=10)
#msgs1.pack(side=RIGHT, fill=BOTH, pady=10)
frame.pack()
# creating text field
textF = Entry(main, font=("Verdana", 20))
textF.pack(fill=X, pady=10)
btn = Button(main, text="Ask from bot", font=("Verdana", 20), command=ask_from_bot)
btn.pack()

# going to bind main window with enter key...
main.bind('<Return>', enter_function)
t = threading.Thread(target=repeatL)
t.start()
main.mainloop()
