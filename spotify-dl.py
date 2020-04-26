from bs4 import BeautifulSoup as soupy
from os import system, rename
from urllib.request import urlopen as uReq


def convertName(title):
    title = list(title)
    for i in range(len(title)-1):
        if title[i] == ' ':
            title[i] = '%20'
        elif title[i] == r'(' or title[i]== r')' or title[i]=='-':
            del title[i]
    title = ''.join(title)
    
    duckurl = 'https://duckduckgo.com/html?q=' + title + '%20audio%20youtube'
    duckData = uReq(duckurl).read()
    duckSoup = soupy(duckData ,'html.parser')

    youtubeLink = str(duckSoup.findAll('a', {'class':'result__url'}, limit=1))
    startIndex = youtubeLink.find(r'www.youtube.com/watch?v=')
    youtubeLinkCut = youtubeLink[startIndex:-24]
    system(r"youtube-dl -f 'bestaudio[ext=m4a]' " + youtubeLinkCut)


def grabSP(url):
    spotifyPage = uReq(url).read()
    spotifySoup = soupy(spotifyPage, 'html.parser')

	#-~-~-~-~-~-~-~-~-~-~-Playlist name. can be used somewhere
    #playlistName = str(spotifySoup.head.title)
    #playlistName = playlistName[7:19] 
    
    trackDetailsRaw = spotifySoup.findAll('div',{'class':'tracklist-col name'})
    for track in trackDetailsRaw:
        turnCount = 0
        trackDetails = track.findAll('span', {'dir':'auto'})
        
        for detail in trackDetails:
            detail = str(detail)
            turnCount += 1
            if turnCount ==1:
                songDetail = detail[36:-7]
            elif turnCount ==2:
                artistDetail = detail[17:-7]
                global trackFinalName
                trackFinalName = songDetail + '-' + artistDetail
                convertName(trackFinalName)
            else:
                pass

print('\r')
print('Enter playlist link: ')
Link = input('$ ')

grabSP(Link)
system('pwd')
print('Done!')
