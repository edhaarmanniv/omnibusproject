from io import BytesIO
from urllib3 import PoolManager

from pydub import AudioSegment
from pydub.playback import play

# recognizer = sr.Recognizer()

mp3_url = "https://pdst.fm/e/aphid.fireside.fm/d/1437767933/8658dd0c-baa7-4412-9466-918650a0013d/6ba07dd7-ebc5-4686-b1eb-f25bcd83821a.mp3"
http = PoolManager()

mp3 = http.urlopen("GET", mp3_url)

# print(mp3.data)
mp3_as = AudioSegment.from_mp3(BytesIO(mp3.data))
print(type(mp3_as))
print(mp3_as.channels)
print(mp3_as.frame_rate)
print(mp3_as.sample_width)
print(mp3_as.max)
print(len(mp3_as)/60000)

# play(mp3_as)

