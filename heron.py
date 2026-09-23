from fbchat_muqit import Client, Message, EventType
from threading import Thread

client = Client(cookies_file_path="./cookies.json")

@client.event
async def on_message(message:Message):
        if message.sender_id == client.uid:
            return
        if not message.text.lower().startswith("/heron"):
            return
        
        to_send = "Hello How are you"
        await client.send_message(
                text=to_send,
                thread_id=message.thread_id,
                reply_to_message=message.id
                )

client.run()


 #huh i completed it ig today is 1-22-2022  1:59 AM and i feel shit
 #revived at 2026 september

 # rechanging everything
