import wikipediaapi,requests,bs4,datetime,nepali_datetime
import json
from gtts import gTTS
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.chrome.options import Options
from time import sleep
from pytube import YouTube
import os
import giphy_client
from dotenv import load_dotenv
from ddgs import DDGS
from pathlib import Path
from tempfile import TemporaryDirectory
import yt_dlp


load_dotenv()
chrome_options = Options()
chrome_options.add_argument("--headless")

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

rou={0:"COMP MS\nPHY RP\nCHE GD\nPHY DN\nMATHS KP\nPHY RP\nNEP PC",6:"COMP MS\nMATHS DM\nTEST\nPHY DN\nMATHS KP\nENG GA\nNEP PC",1:"COMP MS\nPHY DR\nCHE JY\nMATHS DM\nMATHS KP\nENG GA\nNEP PC",2:"CHEM JY\nCOMP MS\nPRACTICAL\nPRACTICAL\nPHY DR\nENG GA\nMATHS ND",3:"COMP MS\nCHE KS\nMATHS ND\nCHE JY\nPHY RP\nPRACTICAL\nPRACTICAL",4:"COMP MS\nCHE GD\nCHE KS\nPHY RP\nTEST\nENG GA\nMATHS ND",5:"आज छुट्टि हे मादरचोद"}
rou2={0:"CHEM JY\nMATHS DM\nPHY RP\nCHEM KS\nBOT AN\nPRACITCALS",6:"BOT AN\nPHY DR\nMATHS DM\nCHEM KS\nMATHS DM\nENG AS\nTEST",1:"MATHS DM\nBOT AN \nCHE SP\nPHY RP\nPHY DN\nENG GA\nTEST",2:"NEP BHU\nPRACTICAL\nCHE SP\nMATHS KP\nZOO UB\nPHY DN",3:"NEP BHU\nZOO UB\nCHE JY\nPHY DN\nMATHS KP\nENG AS\nPHY DR",4:"NEP BHU\nMATHS KP\nZOOL UB\nPRACTICAL\nPHY RP\nCHE JY\n",5:"आज छुट्टि हे मादरचोद"}

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

def today_routine(d='k'):
    if d=='k':
        return rou[datetime.datetime.today().weekday()]
    else:
        return rou2[datetime.datetime.today().weekday()]

def tomm_routine(d='k'):
    if d=='k':
        if datetime.datetime.today().weekday() ==6:
            return rou[0]
        return rou[datetime.datetime.today().weekday()+1]
    else:
        if datetime.datetime.today().weekday() ==6:
            return rou2[0]
        return rou2[datetime.datetime.today().weekday()+1]

def get_pos():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.facebook.com/KEBHS")
    sleep(5)
    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")


    s = bs(html,'html.parser')
    thing = (s.find(True, {"class":["x126k92a"]}).text)
    driver.quit()
    return thing

def get_pos_ronb():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.facebook.com/officialroutineofnepalbanda")
    sleep(5)
    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")


    s = bs(html,'html.parser')
    thing = (s.find(True, {"class":["x126k92a"]}).text)
    driver.quit()
    return thing

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

def name(n,num,g):
    with open('names.txt','a') as file1:
        print(f'{n}..{num}..{g}\n\n',file=file1)

def initialize_gpt():
    global api
    api = ChatGPT(auth_type='google',email="dareludum@gmail.com",password="manoharisdon")


def send_gpt(msg):
    return (api.send_message(msg)['message'].replace('ChatGPT',"Heron").replace("OpenAI","Section G"))


