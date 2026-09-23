import wikipediaapi,requests,bs4,datetime,nepali_datetime
import json
from gtts import gTTS
from bs4 import BeautifulSoup as bs
from time import sleep
from pytube import YouTube
import giphy_client
from ddgs import DDGS
from pathlib import Path
from tempfile import TemporaryDirectory
import yt_dlp
import os

wiki = wikipediaapi.Wikipedia(
    user_agent="HeronBot/1.0 (dareludum@gmail.com)",
    language="en"
)

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

