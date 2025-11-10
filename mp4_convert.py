from pydub import AudioSegment
vid = AudioSegment.from_file("Catswing.mp4", format="mp4")
vid.export("Catswing.mp3", format="mp3")