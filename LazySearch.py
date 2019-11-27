# LazySearch for lazy people
# Deborah Venuti | 2019

#TODO:
# Get rid of ugly terminal notif

import applescript
import urllib
from bs4 import BeautifulSoup
from pync import Notifier

def main():
# Mac
# AppleScript to get currently playing artist and song from Spotify / iTunes (no auth req)
    scpt = applescript.AppleScript('''
        on run
            set spotifyApp to \"Spotify\"
            set itunesApp to \"iTunes\"
            set runningApp to \"\"
            set isRunning to false
            tell application \"System Events\"
                if (exists process spotifyApp) then
                    set isRunning to true
                    set runningApp to spotifyApp
                else if (exists process itunesApp) then
                    set isRunning to true
                    set runningApp to itunesApp
                end if
            end tell
            
            if isRunning is true then
                tell application runningApp
                    set artistName to artist of current track as string
                    set songName to name of current track as string 
                    set currentSong to artistName & \" - \" & songName
                end tell
            end if
        return currentSong
        end run
    ''')

    nowPlaying = scpt.run()

# Search for video of currently playing song
    # Telling urllib what the query text will be
    query = urllib.parse.quote(nowPlaying)

    # Get video URL for nowPlaying
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    video = soup.find(attrs={'class':'yt-uix-tile-link'})
    videoUrl = 'https://www.youtube.com' + video['href']

    Notifier.notify(title='LazySearch',
                    message='Successfully Shared: ' + nowPlaying,
                    open='' + videoUrl
                    )
                        
if __name__ == "__main__":
    main()
