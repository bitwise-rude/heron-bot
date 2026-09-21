from fbchat import Client
from fbchat.models import *
from functions import *
from threading import Thread
import random
import time
from PIL import Image
import json
import pickle
from dotenv import load_dotenv
import os

load_dotend()

meyan = "100078863451761"
on=True
prev = time.time()
def do():
    global prev
    while on:
        if(time.time()-prev) >60:
            print("WORKING")
            with open("school.text",'r',encoding="utf8") as file1:
                st = file1.read()
                print(st)
            stuff=get_pos()
            print(stuff)
            if(stuff!=st):
                print("OK NOT COME")
                for grps in GROUPS:
                    client.send(Message(text=stuff),grps,thread_type=ThreadType.GROUP)

            with open("school.text",'w',encoding="utf8") as file1:
                file1.write(stuff)
            prev = time.time()
            print("HERE")

on1=True
prev1 = time.time()

def do1():
    global prev
    while on1:
        if(time.time()-prev) >600:
            stuff=get_pos_ronb()
            client.send(Message(text=stuff),"5354113521302706",thread_type=ThreadType.GROUP)
            prev1= time.time()
            print("HERE")
            prev = time.time()

class Bot(Client):
    def onMessage(self, mid, author_id, message_object, thread_id, thread_type, ts, metadata, msg, **kwargs):


        # Do something with message_object here
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        if "hi heron" in message_object.text.lower():
                self.send(Message(text="Hi, wishing you very best"),thread_id,thread_type=thread_type)
        if "bye" in message_object.text.lower():
                self.send(Message(text="okay  see you later"),thread_id,thread_type=thread_type)
        if "heron" in  message_object.text.lower():
            if "thank" in message_object.text.lower():
                self.send(Message(text="You are welcome Sir"),thread_id,thread_type=thread_type)
            if "good job" in message_object.text.lower():
                self.send(Message(text="Thank you sir"),thread_id,thread_type=thread_type)
        if author_id != self.uid:
            if message_object.text[0:5]=="/post":
                self.send(Message(text=get_pos()),thread_id,thread_type=thread_type)

            if message_object.text[0:6]=="/heron":
                self.send(Message(text=send_gpt(message_object.text[7:])),thread_id,thread_type=thread_type)

            if message_object.text[0:5]=="/wiki":
                self.send(Message(text=get_s(message_object.text[6:])),thread_id,thread_type=thread_type)
            if message_object.text[0:3].lower()=="/jy":
                client.sendLocalFiles(file_paths="jy.png",

                thread_id=thread_id,
                thread_type=thread_type,
            )
            if message_object.text.lower() == 'heron':
                self.send(Message(text="Hey"))
            if message_object.text[0:5]=="/name":
                name((message_object.text[6:]),author_id,thread_id)
                self.send(Message(text="Added your name, thanks"),thread_id,thread_type=thread_type)
            if message_object.text[0:5]=="sourc":
                m="Heron's Code isn't open source yet"
                self.send(Message(text=m),thread_id,thread_type=thread_type)

            if message_object.text[0:5]=="/fact":
                self.send(Message(text=fact()),thread_id,thread_type=thread_type)

            if message_object.text[0:7]=="/advice":
                self.send(Message(text=advice()),thread_id,thread_type=thread_type)

            if message_object.text[0:5]=="/help":
                self.send(Message(text="Head out to our website heronbot.pythonanywhere.com to see all the features and news!!"),thread_id,thread_type=thread_type)




            if message_object.text[0:5]=="/show":
                if "ronb" in message_object.text.lower():
                    self.send(Message(text=get_pos_ronb()),thread_id,thread_type=thread_type)
                if not  "routine" in message_object.text.lower():
                        client.sendRemoteFiles(
            file_urls=get_im(message_object.text[6:]),

            thread_id=thread_id,
            thread_type=thread_type,
        )

                else:
                    if "today" in message_object.text.lower():
                        if not ("section d" in message_object.text.lower()):
                            self.send(Message(text=today_routine()),thread_id,thread_type=thread_type)
                        else:
                            self.send(Message(text=today_routine('d')),thread_id,thread_type=thread_type)
                    elif "tom" in message_object.text.lower():
                        if not ("section d" in message_object.text.lower()):
                            self.send(Message(text=tomm_routine()),thread_id,thread_type=thread_type)
                        else:
                            self.send(Message(text=tomm_routine('d')),thread_id,thread_type=thread_type)
                    else:
                        if not ("section d" in message_object.text.lower()):
                            client.sendLocalFiles(file_paths="routine.jpg",
                message=Message(text="Hopefully this works!:)"),
                thread_id=thread_id,
                thread_type=thread_type,
            )
                        else:
                            client.sendLocalFiles(file_paths="sec_D.jpg",
                message=Message(text="Good luck Section D!:)"),
                thread_id=thread_id,
                thread_type=thread_type,
            )
            if message_object.text[0:5].lower()=="/date":
                if "nepal" in message_object.text.lower():
                    self.send(Message(text=nep_date()),thread_id,thread_type=thread_type)
                else:
                    self.send(Message(text=date()),thread_id,thread_type=thread_type)
            t = message_object.text.lower()
            print(thread_id)


            if message_object.text[0:5].lower()=="/ronb":
                    self.send(Message(text=get_pos_ronb()),thread_id,thread_type=thread_type)
            if message_object.text[0:5].lower()=="/news":
                    self.send(Message(text=get_pos_ronb()),thread_id,thread_type=thread_type)
            if message_object.text[0:5].lower()=="/play":
                    download(message_object.text[5:])
                    print("downloaded")
                    self.sendLocalVoiceClips("audio.mp3",message="Here enjoy!!",thread_id=thread_id,thread_type=thread_type)
            if message_object.text[0:4].lower()=="/gif":
                self.sendRemoteFiles(giphy(message_object.text[4:]),thread_id=thread_id,thread_type=thread_type)

            if message_object.text[0:4].lower()=="/say":
                if "quote" in message_object.text.lower():
                    self.send(Message(text=rand_quote()),thread_id,thread_type=thread_type)
                if "date" in message_object.text.lower():
                    if "nepal" in message_object.text.lower():
                        self.send(Message(text=nep_date()),thread_id,thread_type=thread_type)
                    else:
                        self.send(Message(text=date()),thread_id,thread_type=thread_type)
                elif "joke" in message_object.text.lower():
                    if not "mama" in message_object.text.lower():
                        self.send(Message(text=joke()),thread_id,thread_type=thread_type)
                    else:
                        self.send(Message(text=yo_mama()),thread_id=thread_id,thread_type=thread_type)

                else:
                    if not "nepali" in message_object.text.lower():
                        conv_mp3(message_object.text[4:])
                        self.sendLocalVoiceClips("welcome.mp3",message=None,thread_id=thread_id,thread_type=thread_type)
                    else:
                        conv_mp3(message_object.text[4:].lower().replace("nepali","").replace("in",""),'ne')
                        self.sendLocalVoiceClips("welcome.mp3",message=None,thread_id=thread_id,thread_type=thread_type)


            if '/chill' in t or '/sad' in t or '/excited' in t or '/khoon' in t or'/laugh' in t or '/happy' in t or '/smile' in t:
                    client.sendLocalFiles(file_paths=f"emotions\\{message_object.text.lower()[1:]}.jpeg",
                thread_id=thread_id,
                thread_type=thread_type,
            )

GROUPS = [5354113521302706,5850146545005742,6354363004636599]
GROUPS_ORDER=['g','d','f']




username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
client = Bot(username,password)

#Thread(target=do1).start()
#Thread(target=do).start()
print("HI I AM HERE")
try:
    client.listen()
except:
    on=False
    on1=False
on=False
on1=False




 #huh i completed it ig today is 1-22-2022  1:59 AM and i feel shit
