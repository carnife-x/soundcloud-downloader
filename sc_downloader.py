import requests
from requests.structures import CaseInsensitiveDict
from bs4 import BeautifulSoup
from urllib.parse import quote
import re,os
from coverart import combine_art

url = "https://sclouddownloader.net/download-sound-track"
music_url=quote(input("enter the song url:"))
# music_url="https%3A//soundcloud.com/greglaswell/dodged-a-bullet"

#defining headers for the request
headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/x-www-form-urlencoded"
headers["Referer"] = "https://sclouddownloader.net/"
headers["Cookie"] = "csrftoken=t9YD8iES7G9pJQF1SIIPgczhbsZaVcOx;"
data = "csrfmiddlewaretoken=t9YD8iES7G9pJQF1SIIPgczhbsZaVcOx&sound-url="+music_url

#initiating a requests session
s = requests.session()
resp = s.post(url, headers=headers, data=data)
print(resp.status_code)

#parsing urls from the response
soup = BeautifulSoup(resp.text, 'html.parser')
links=[]
for link in soup.find_all('a'):
    links.append(link.get('href'))

#Get song title from response
song_title=soup.find_all('i')[1]
song_title=re.compile(r'<[^>]+>').sub('', str(song_title))[:-4]

#download song from the parsed url
song=s.get(links[5])
open(song_title, 'wb').write(song.content)
print(song_title)

#get song image
image=soup.find('img').get('src')
cover_title=str(image).split("/")[-1]
cover=song=s.get(image)
open(cover_title, 'wb').write(cover.content)
print(cover_title)

#combine albumart and song
combine_art(song_title,cover_title)
os.remove(cover_title)