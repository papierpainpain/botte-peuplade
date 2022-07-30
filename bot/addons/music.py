import youtube_dl
ytdl = youtube_dl.YoutubeDL()


class Music:
    def __init__(self, link):
        music = ytdl.extract_info(link, download=False)
        music_format = music["formats"][0]
        self.title = music['title']
        self.url = music["webpage_url"]
        self.stream_url = music_format["url"]
