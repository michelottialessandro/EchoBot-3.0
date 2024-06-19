
# import required modules
from pydub import AudioSegment
from pydub.playback import play
 
# for playing wav file
song = AudioSegment.from_wav("speech.wav")
print('playing sound using  pydub')
play(song)