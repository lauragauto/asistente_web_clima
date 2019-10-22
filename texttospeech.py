from gtts import gTTS


def tts(text, lang, name_file):
    file = gTTS(text=text, lang=lang)
    filename = name_file
    file.save(filename)
