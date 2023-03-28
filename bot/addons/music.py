import yt_dlp
ydl = yt_dlp.YoutubeDL({ 'format': 'bestaudio/best' })

class Music:
    def __init__(self, link):
        music = ydl.extract_info(link, download=False)

        self.title = music['title']
        self.url = music['webpage_url']
        self.stream_url = music['url']
