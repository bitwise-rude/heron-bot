import wikipedia,requests,bs4,datetime,nepali_datetime
import json
from gtts import gTTS
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.chrome.options import Options
from time import sleep
from pytube import YouTube
import os
import giphy_client

chrome_options = Options()
chrome_options.add_argument("--headless")

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

rou={0:"COMP MS\nPHY RP\nCHE GD\nPHY DN\nMATHS KP\nPHY RP\nNEP PC",6:"COMP MS\nMATHS DM\nTEST\nPHY DN\nMATHS KP\nENG GA\nNEP PC",1:"COMP MS\nPHY DR\nCHE JY\nMATHS DM\nMATHS KP\nENG GA\nNEP PC",2:"CHEM JY\nCOMP MS\nPRACTICAL\nPRACTICAL\nPHY DR\nENG GA\nMATHS ND",3:"COMP MS\nCHE KS\nMATHS ND\nCHE JY\nPHY RP\nPRACTICAL\nPRACTICAL",4:"COMP MS\nCHE GD\nCHE KS\nPHY RP\nTEST\nENG GA\nMATHS ND",5:"आज छुट्टि हे मादरचोद"}
rou2={0:"CHEM JY\nMATHS DM\nPHY RP\nCHEM KS\nBOT AN\nPRACITCALS",6:"BOT AN\nPHY DR\nMATHS DM\nCHEM KS\nMATHS DM\nENG AS\nTEST",1:"MATHS DM\nBOT AN \nCHE SP\nPHY RP\nPHY DN\nENG GA\nTEST",2:"NEP BHU\nPRACTICAL\nCHE SP\nMATHS KP\nZOO UB\nPHY DN",3:"NEP BHU\nZOO UB\nCHE JY\nPHY DN\nMATHS KP\nENG AS\nPHY DR",4:"NEP BHU\nMATHS KP\nZOOL UB\nPRACTICAL\nPHY RP\nCHE JY\n",5:"आज छुट्टि हे मादरचोद"}

def get_s(tx):
    try:
        return wikipedia.summary(tx, sentences=2,auto_suggest=False)
    except:
        return wikipedia.summary(tx, sentences=2,auto_suggest=True)

def get_im(query):
            image_urls = []

            url = "https://bing-image-search1.p.rapidapi.com/images/search"

            querystring = {"q": query, "count": 1}

            headers = {
                'x-rapidapi-host': "bing-image-search1.p.rapidapi.com",
                'x-rapidapi-key': "801ba934d6mshf6d2ea2be5a6a40p188cbejsn09635ee54c45"
            }
            print("sending requests...")
            response = requests.request(
                "GET", url, headers=headers, params=querystring)
            print("got response..")
            data = json.loads(response.text)
            img_contents = (data["value"])
            for img_url in img_contents:
                image_urls.append(img_url["contentUrl"])
                print("appended..")
                print(image_urls)
                return image_urls[0]

def rand_quote():

    url = "https://zenquotes.io/"

    b = requests.get(url)
    s = bs4.BeautifulSoup(b.text,'html.parser')
    return (s.find('h1').text)




def joke():
    g = requests.get("https://icanhazdadjoke.com",headers={"Accept":"text/plain"})
    return g.text

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
    link = VideosSearch(s,limit=1).result()['result'][0]
    link = link['link']
    yt= YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download()
    base, ext = os.path.splitext(out_file)
    new_file = 'audio' + '.mp3'
    os.remove("audio.mp3")
    os.rename(out_file, new_file)

def giphy(q):
    key = "DtsfE5oaOQLOiOySqoGfMHeMX5SeS8As"
    ins = giphy_client.DefaultApi()
    res = ins.gifs_search_get(key,q,limit=1,rating='r')
    giff = res.data[0]
    url = f'https://media.giphy.com/media/{giff.id}/giphy.gif'
    return url

def fact():
    limit = 1
    api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
    response = requests.get(api_url, headers={'X-Api-Key': '+KBpcqK6SeJPNFn9DQ9YRQ==9EDHbVo5RVeK3jER'})
    if response.status_code == requests.codes.ok:
        a=json.loads(response.text)
        return (a[0]['fact'])
    else:
        print("Error: in the fact librar", response.status_code, response.text)

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
