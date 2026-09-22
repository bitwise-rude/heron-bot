from fbchat_muqit import Client, Message, EventType
from functions import gemini
from threading import Thread


client = Client(cookies_file_path="./cookies.json")
@client.event
async def on_message(message:Message):
        if message.sender_id == client.uid:
            return

        message_object = message
        if not message_object.text.lower().startswith("/heron"):
            return

        result = gemini(message_object.text[6:].strip())
        action_handlers = {
            "image": lambda: client.send_files_from_url(thread_id=message.thread_id, file_urls=[result["url"]]),
            "gif": lambda: client.send_files_from_url(thread_id=message.thread_id, file_urls=[result["url"]]),
            "audio": lambda: client.send_files_from_path(thread_id=message.thread_id, file_paths=[result["path"]]),
            "speech": lambda: client.send_files_from_path(thread_id=message.thread_id, file_paths=[result["path"]]),
            "emotion": lambda: client.send_files_from_path(thread_id=message.thread_id, file_paths=[result["path"]]),
        }
        handler = action_handlers.get(result["type"])
        if handler:
            await handler()
        else:
            await client.send_message(
                text=result["text"],
                thread_id=message.thread_id,
                reply_to_message=message.id
                )

client.run()


 #huh i completed it ig today is 1-22-2022  1:59 AM and i feel shit
 #revived at 2026 september
