import speech_recognition as sr

r = sr.Recognizer()

def recognize():
    with sr.Microphone() as source:
        audio = r.listen(source)
        voice = ''
        try:
            voice = r.recognize_google(audio, language='tr-TR')
        except sr.UnknownValueError:
            print('not recognized')
        except sr.RequestError:
            print('server error')
        return voice
print('Listening...')
print(recognize())