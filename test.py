from fbchat_muqit import Client, Message, EventType
from functions import *
from threading import Thread
import random
import time
from PIL import Image
import json
import pickle
import os


client = Client(cookies_file_path="./cookies.json")
@client.event
async def on_message(message:Message):
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

            if message_object.text[0:6]=="/heron":
                text="cannot use chatgpt atm"

            if message_object.text[0:5]=="/wiki":
                text=get_s(message_object.text[6:]) 
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

            if message_object.text.strip().lower()=="/ronb":
                    if message_object.text.strip().lower():
                        text=get_pos_ronb()
                    else:
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
                    else:
                        conv_mp3(message_object.text[4:].lower().replace("nepali","").replace("in",""),'ne')
                        await client.send_files_from_path(
                                thread_id =  message.thread_id,
                                file_paths=["welcome.mp3"])

            if '/chill' in t or '/sad' in t or '/excited' in t or '/khoon' in t or'/laugh' in t or '/happy' in t or '/smile' in t:
                await client.send_files_from_path(
                                thread_id =  message.thread_id,
                                file_paths=[f"emotions/{message_object.text.lower()[1:]}.jpeg"])
           

        if text:
            await client.send_message(
                text=text,
                thread_id=message.thread_id,
                reply_to_message=message.id
                )

client.run()


 #huh i completed it ig today is 1-22-2022  1:59 AM and i feel shit
 #revived at 2026 september
