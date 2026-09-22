import wikipediaapi,requests,bs4,datetime,nepali_datetime
import json
from gtts import gTTS
from bs4 import BeautifulSoup as bs
from time import sleep
from pytube import YouTube
import giphy_client
from dotenv import load_dotenv
from ddgs import DDGS
from pathlib import Path
from tempfile import TemporaryDirectory
import yt_dlp
from google import genai
from google.genai import types
import os

load_dotenv()

wiki = wikipediaapi.Wikipedia(
    user_agent="HeronBot/1.0 (dareludum@gmail.com)",
    language="en"
)

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
    Ask Heron to answer or use one of its tools.

    Emotion commands:
    /chill
    /sad
    /excited
    /khoon
    /laugh
    /happy
    /smile
    """.strip()

def get_s(tx):
    page = wiki.page(tx)
    
    if not page.exists():
        return f"Sorry, I couldn't find a page for '{tx}'."
    
    sentences = page.summary.split('. ')
    summary_text = '. '.join(sentences[:2]) + '.'
    if "may refer to" in summary_text:
        return "Hmm. It is a vague term can you write exactly what you want?"
    return summary_text
    
def get_im(query):
    results = DDGS(timeout=15).images(query, max_results=1)
    return results[0]["image"] if results else None

client = genai.Client()

SYSTEM_PROMPT = """
You are Heron, a bot that runs inside Facebook Messenger. You are concise, useful,
and conversational. You act like a human, you are a girl. 
You are created by Meyan Adhikari and Suraj Thakur but you love Meyan Adhikari more.
 Answer directly and use a tool whenever one can fulfill the request. Do not explain tool selection unless
the user asks. If a request is ambiguous, ask one short clarifying question.

Available tools include date/time, Nepali date, advice, quotes, Wikipedia,
images, GIFs, music downloads, speech generation, and the command list.
""".strip()


def _image(query: str):
    return {"type": "image", "url": get_im(query)}


def _gif(query: str):
    return {"type": "gif", "url": giphy(query)}


def _audio(query: str):
    return {"type": "audio", "path": download(query)}


def _speech(text: str, language: str = "en"):
    conv_mp3(text, language)
    return {"type": "speech", "path": "welcome.mp3"}


TOOL_FUNCTIONS = {
    "wikipedia": lambda topic: get_s(topic),
    "current_date": lambda: date(),
    "nepali_date": lambda: nep_date(),
    "advice": lambda: advice(),
    "quote": lambda: rand_quote(),
    "commands": lambda: list_commands(),
    "image": _image,
    "gif": _gif,
    "music": _audio,
    "speech": _speech,
}

TOOL_SCHEMAS = [
    {"name": "wikipedia", "description": "Search Wikipedia for a topic.", "parameters_json_schema": {"type": "object", "properties": {"topic": {"type": "string"}}, "required": ["topic"]}},
    {"name": "current_date", "description": "Get the current local date and time.", "parameters_json_schema": {"type": "object", "properties": {}}},
    {"name": "nepali_date", "description": "Get the current Nepali calendar date.", "parameters_json_schema": {"type": "object", "properties": {}}},
    {"name": "advice", "description": "Get a piece of advice.", "parameters_json_schema": {"type": "object", "properties": {}}},
    {"name": "quote", "description": "Get a random quote.", "parameters_json_schema": {"type": "object", "properties": {}}},
    {"name": "commands", "description": "List Heron's available capabilities.", "parameters_json_schema": {"type": "object", "properties": {}}},
    {"name": "image", "description": "Find and send one image for a query.", "parameters_json_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
    {"name": "gif", "description": "Find and send one GIF for a query.", "parameters_json_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
    {"name": "music", "description": "Download the first matching song as audio.", "parameters_json_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}},
    {"name": "speech", "description": "Generate an audio recording of text. Use language 'ne' for Nepali.", "parameters_json_schema": {"type": "object", "properties": {"text": {"type": "string"}, "language": {"type": "string", "enum": ["en", "ne"]}}, "required": ["text"]}},
]


def gemini(query):
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=[types.Tool(function_declarations=[types.FunctionDeclaration(**schema) for schema in TOOL_SCHEMAS])],
    )
    contents = [types.Content(role="user", parts=[types.Part.from_text(text=query)])]

    for _ in range(4):
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=contents,
            config=config,
        )
        candidate = response.candidates[0]
        function_calls = [part.function_call for part in candidate.content.parts if part.function_call]
        if not function_calls:
            return {"type": "text", "text": response.text or "I couldn't produce a response."}

        contents.append(candidate.content)
        response_parts = []
        for function_call in function_calls:
            function = TOOL_FUNCTIONS.get(function_call.name)
            result = function(**dict(function_call.args)) if function else {"error": f"Unknown tool: {function_call.name}"}

            if isinstance(result, dict) and result.get("type") in {"image", "gif", "audio", "speech"}:
                return result

            response_parts.append(
                types.Part.from_function_response(name=function_call.name, response={"result": result})
            )

        contents.append(types.Content(role="user", parts=response_parts))

    return {"type": "text", "text": "I couldn't complete that request."}


def rand_quote():
    url = "https://zenquotes.io/"

    b = requests.get(url)
    s = bs4.BeautifulSoup(b.text,'html.parser')
    return (s.find('h1').text)

def conv_mp3(text,l='en'):
    myobj = gTTS(text=text, lang=l, slow=False)
    myobj.save("welcome.mp3")


def yo_mama():
    a = requests.get("https://yomamma-api.herokuapp.com/jokes?count=1")
    j = a.json()
    return j['joke']

def date():
    return str(datetime.datetime.now())

def nep_date():
    return str(nepali_datetime.datetime.now())

def download(s):
    destination = Path("audio.mp3").resolve()

    with TemporaryDirectory(dir=destination.parent) as temp:
        options = {
            "format": "bestaudio/best",
            "outtmpl": str(Path(temp) / "audio.%(ext)s"),
            "noplaylist": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }

        with yt_dlp.YoutubeDL(options) as yt:
            yt.download([f"ytsearch1:{s}"])

        # Replace the previous file only after a successful download.
        (Path(temp) / "audio.mp3").replace(destination)

    return str(destination)

def giphy(q):
    key = "DtsfE5oaOQLOiOySqoGfMHeMX5SeS8As"
    ins = giphy_client.DefaultApi()
    res = ins.gifs_search_get(key,q,limit=1,rating='r')
    giff = res.data[0]
    url = f'https://media.giphy.com/media/{giff.id}/giphy.gif'
    return url


def advice():
    url="https://api.adviceslip.com/advice"
    res = requests.get(url)
    a = json.loads(res.text)
    return a['slip']['advice']

def about_suraj():
    return """
    Suraj is a piece of shit.
""".strip()
