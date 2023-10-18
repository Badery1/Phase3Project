

# from pydub import AudioSegment
# from pydub.playback import play
# import time

# def play_audio(audio_file):
#     audio = AudioSegment.from_mp3(audio_file)
#     play(audio)
#     time.sleep(len(audio) / 1000)

# if __name__ == '__main__':
#     audio_file = 'game-music.mp3'
#     play_audio(audio_file)

# from pydub import AudioSegment
# from pydub.playback import play
# import threading

# audio_file = 'game-music.mp3'

# def play_sound(audio_file):
#     audio = AudioSegment.from_mp3(audio_file)
#     while True:
#         play(audio)
#         time.sleep(len(audio) / 1000)

# audio_thread = threading.Thread(target=play_sound, args=(audio_file,))
# audio_thread.daemon = True
# audio_thread.start()

# import subprocess
# import threading

# audio_file = 'game-music.mp3'

# def play_sound(audio_file):
#     # Use subprocess to play audio in the background
#     subprocess.Popen(['mpg123', '-q', audio_file])

# audio_thread = threading.Thread(target=play_sound, args=(audio_file,))
# audio_thread.daemon = True
# audio_thread.start()