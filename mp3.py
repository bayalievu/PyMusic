from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.id3 import TIT2, TALB, TPE1, TPE2, COMM, USLT, TCOM, TCON, TDRC
from mutagen.easyid3 import EasyID3
import mutagen.id3
#audio = MP3("Aiar_-_Karlygachym.mp3")
#print audio.info.length, audio.info.bitrate

#from mutagen.easyid3 import EasyID3
#audio = EasyID3("Aiar_-_Karlygachym.mp3")
#audio["title"] = u"An example"
#audio.save()

#audio = MP3("Aiar_-_Karlygachym.mp3")
#audio.tags = ID3()
#audio.tags.add(TIT2(encoding=3, text=["Karlygashym"]))
#audio.save()

#print EasyID3.valid_keys.keys()
'''
mp3file = MP3("Aiar_-_Karlygachym.mp3", ID3=EasyID3)

try:
    mp3file.add_tags(ID3=EasyID3)
except mutagen.id3.error:
    print("has tags")

mp3file['title'] = 'Karlygach'
mp3file['artist'] = "Aiar"
mp3file.save()

print(mp3file.pprint())
'''

from glob import glob
for filename in glob('/home/ulan/PyMusic/*.mp3'):
    mp3info = EasyID3(filename)
    print mp3info.items()
