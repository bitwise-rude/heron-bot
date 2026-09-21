from fbchat_muqit import Client, Message, EventType
from functions import *
from threading import Thread
import random
import time
from PIL import Image
import json
import pickle
import os


meyan = "100078863451761"
on=True
prev = time.time()
client = Client(cookies_file_path="./cookies.json")

# def do():
#     global prev
#     while on:
#         if(time.time()-prev) >60:
#             print("WORKING")
#             with open("school.text",'r',encoding="utf8") as file1:
#                 st = file1.read()
#                 print(st)
#             stuff=get_pos()
#             print(stuff)
#             if(stuff!=st):
#                 print("OK NOT COME")
#                 for grps in GROUPS:
#                     client.send(Message(text=stuff),grps,thread_type=ThreadType.GROUP)
#
#             with open("school.text",'w',encoding="utf8") as file1:
#                 file1.write(stuff)
#             prev = time.time()
#             print("HERE")

on1=True
prev1 = time.time()

# def do1():
#     global prev
#     while on1:
#         if(time.time()-prev) >600:
#             stuff=get_pos_ronb()
#             client.send(Message(text=stuff),"5354113521302706",thread_type=ThreadType.GROUP)
#             prev1= time.time()
#             print("HERE")
#             prev = time.time()

def list_commands():
    return """
Heron Bot Commands

/wiki <topic>
Search Wikipedia.

/show <query>
Search and send an image.

/show routine today
Show today's routine.

/show routine tom
Show tomorrow's routine.

/date
Show current date and time.

/date nepal
Show Nepali date.

/advice
Get random advice.

/play <song>
Search YouTube and send the audio.

/gif <query>
Search and send a GIF.

/say <text>
Convert text to speech.

/say nepali <text>
Convert Nepali text to speech.

/say quote
Get a random quote.

/name <name>
Save your name.

/help
Show Heron help information.

/ronb
RONB feature (currently disabled).

/news
News feature (currently disabled).

/post
Post feature (currently disabled).

/heron <message>
ChatGPT feature (currently disabled).

Emotion commands:
/chill
/sad
/excited
/khoon
/laugh
/happy
/smile
""".strip()

@client.event
async def on_message(message:Message):
# def onMessage(self, mid, author_id, message_object, thread_id, thread_type, ts, metadata, msg, **kwargs):

        # Do something with message_object here
        # self.markAsDelivered(thread_id, message_object.uid)
        # self.markAsRead(thread_id)
        if message.sender_id == client.uid:
            return

        text = ""
        
        message_object = message
        if "hi heron" in message_object.text.lower():
                text="Hi, wishing you very best"
        if "bye" in message_object.text.lower():
                text="okay  see you later"
        if "heron" in  message_object.text.lower():
            if "thank" in message_object.text.lower():
                text="You are welcome Sir"
            if "good job" in message_object.text.lower():
                text="Thank you sir"
        if True: # i didn't wanna deindent
            if message_object.text[0:5]=="/post":
                text="Cannot post atm"
                # self.send(Message(text=get_pos()),thread_id,thread_type=thread_type)

            if message_object.text[0:6]=="/heron":
                text="cannot use chatgpt atm"
                # self.send(Message(text=send_gpt(message_object.text[7:])),thread_id,thread_type=thread_type)

            if message_object.text[0:5]=="/wiki":
                text=get_s(message_object.text[6:]) # TODO: kam garena

            if message_object.text.lower() == 'heron':
                text="Hey"
            if message_object.text[0:5]=="/name":
                name((message_object.text[6:]),message_object.sender_id,message_object.thread_id)
                text="Added your name, thanks"
            if message_object.text[0:5]=="sourc":
                m="Heron's Code isn't open source yet"
                text=m

            if message_object.text[0:7]=="/advice":
                text=advice()

            if message_object.text[0:5]=="/help":
                text="Head out to our website heronbot.pythonanywhere.com to see all the features and news!!"

            if message_object.text[0:5]=="/list":
                text=list_commands()

            if message_object.text[0:5]=="/show":
                if "ronb" in message_object.text.lower():
                    # self.send(Message(text=get_pos_ronb()),thread_id,thread_type=thread_type)
                    text="RONB NOT IMPLEMENTED"
                elif not  "routine" in message_object.text.lower():
                        await client.send_files_from_url(
                                thread_id =  message.thread_id,
                                file_urls=[get_im(message.text[6:])],
                                )

                else:
                    if "today" in message_object.text.lower():
                        if not ("section d" in message_object.text.lower()):
                           text=today_routine()
                        else:
                            text=today_routine('d')
                    elif "tom" in message_object.text.lower():
                        if not ("section d" in message_object.text.lower()):
                            text=tomm_routine()
                        else:
                            text=tomm_routine('d')
                    else:
                        await client.send_files_from_path(
                                thread_id =  message.thread_id,
                                file_paths=["routine.jpg"]
                                )

                        if not ("section d" in message_object.text.lower()):
                            await client.send_files_from_path(
                                thread_id =  message.thread_id,
                                file_paths=["routine.jpg"]
                                )
                            text="Hope this worsk"
                        else:
                            await client.send_files_from_path(
                                thread_id =  message.thread_id,
                                file_paths=["sec_D.jpg"]
                                )
                            text="Good luck Section D"
            if message_object.text[0:5].lower()=="/date":
                if "nepal" in message_object.text.lower():
                    text=nep_date()
                else:
                    text=date()
            t = message_object.text.lower()

            if message_object.text[0:5].lower()=="/ronb":
                    # self.send(Message(text=get_pos_ronb()),thread_id,thread_type=thread_type)
                    text="RONB NOT IMPLEMENTED NOW"
            if message_object.text[0:5].lower()=="/news":
                    # self.send(Message(text=get_pos_ronb()),thread_id,thread_type=thread_type)
                    text="RONB NOT IMPLEMENTED NOW"
            if message_object.text[0:5].lower()=="/play":
                    download(message_object.text[5:])
                    print("downloaded")
                    await client.send_files_from_path(
                                thread_id =  message.thread_id,
                                file_paths=["audio.mp3"])

            if message_object.text[0:4].lower()=="/gif":
                await client.send_files_from_url(
                                thread_id =  message.thread_id,
                                file_urls=[giphy(message_object.text[4:])])
                # self.sendRemoteFiles(giphy(message_object.text[4:]),thread_id=thread_id,thread_type=thread_type)

            if message_object.text[0:4].lower()=="/say":
                if "quote" in message_object.text.lower():
                    text=rand_quote()
                elif "date" in message_object.text.lower():
                    if "nepal" in message_object.text.lower():
                        text=nep_date()
                    else:
                        text=date()

                else:
                    if not "nepali" in message_object.text.lower():
                        conv_mp3(message_object.text[4:])
                        await client.send_files_from_path(
                                thread_id =  message.thread_id,
                                file_paths=["welcome.mp3"])
                        # self.sendLocalVoiceClips("welcome.mp3",message=None,thread_id=thread_id,thread_type=thread_type)
                    else:
                        conv_mp3(message_object.text[4:].lower().replace("nepali","").replace("in",""),'ne')
                        # self.sendLocalVoiceClips("welcome.mp3",message=None,thread_id=thread_id,thread_type=thread_type)
                        await client.send_files_from_path(
                                thread_id =  message.thread_id,
                                file_paths=["welcome.mp3"])

            if '/chill' in t or '/sad' in t or '/excited' in t or '/khoon' in t or'/laugh' in t or '/happy' in t or '/smile' in t:
                await client.send_files_from_path(
                                thread_id =  message.thread_id,
                                file_paths=[f"emotions/{message_object.text.lower()[1:]}.jpeg"])
            #         client.sendLocalFiles(file_paths=f"emotions\\{message_object.text.lower()[1:]}.jpeg",
            #     thread_id=thread_id,
            #     thread_type=thread_type,
            # )

        if text:
            await client.send_message(
                text=text,
                thread_id=message.thread_id,
                reply_to_message=message.id
                )


GROUPS = [5354113521302706,5850146545005742,6354363004636599]
GROUPS_ORDER=['g','d','f']


#Thread(target=do1).start()
#Thread(target=do).start()

print("HI I AM HERE")
try:
    client.run()
except:
    on=False
    on1=False
on=False
on1=False




 #huh i completed it ig today is 1-22-2022  1:59 AM and i feel shit
