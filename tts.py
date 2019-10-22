import speech_recognition as sr
from gtts import gTTS
import os


class _TTS:
    engine = None
    rate = None
    r = None

    def __init__(self):
        self.r = sr.Recognizer()

    def start(self):
        audio_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'RecordedFile.wav')

        with sr.WavFile(audio_file) as source:  # use "RecordedFile.wav" as the audio source
            audio = self.r.record(source) # extract audio data from the file
        
        result = ""
        try:
            result = self.r.recognize_google(audio, language="es-PY")
            print(result)   # recognize speech using Google Speech Recognition
            mytext = result
            language = 'es'
            myobj = gTTS(text=mytext, lang=language, slow=False)
            myobj.save(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'response.mp3'))
        except LookupError:                                        # speech is unintelligible
            print("Disculpame, no entendi lo que dijiste. Podrías ser más claro?")
        return result
