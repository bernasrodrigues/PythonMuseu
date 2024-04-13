import os
import threading

import pygame

# Get the current directory of soundPlayer.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate up one directory to BaseFolder
base_folder = os.path.dirname(current_dir)              # Parent Folder (PythonMuseu)

# Enter the GUI/sounds directory
# sound_file_path = os.path.join(base_folder, 'GUI', 'sounds', 'song.mp3')




class SoundPlayer:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)

                cls._instance._sound_threads = []
                pygame.mixer.init()  # Initialize the mixer
                print("Created Sound Player\n------------")
            return cls._instance

    @classmethod
    def Instance(cls):
        return cls()


    def GetPathToFile(self, fileName):
        sound_file_path = os.path.join(base_folder, 'GUI', 'sounds', fileName)
        return sound_file_path

    def play_sound(self, sound):
        thread = threading.Thread(target=self._play_sound, args=(self.GetPathToFile(sound),))
        self._sound_threads.append(thread)
        thread.start()

    def _play_sound(self, sound):
        #print(f"Playing sound: {sound}")
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(1000)  # Wait until the music is finished playing
        self._sound_threads.remove(threading.current_thread())
