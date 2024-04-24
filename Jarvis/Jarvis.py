
from datetime import datetime
from winreg import QueryInfoKey
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
activationWord = 'computer'

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))


def speak(text, rate = 120):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()


def parseCommand():
    listener = sr.Recognizer()
    print('Listening for a command')
    
    with sr.Microphone() as source:
        listener.pause_threshold = 1
        input_speech = listener.listen(source)

    try:
        print('Recognizing speech...')
        query = listener.recognize_google(input_speech, language='en_us')
        print(f'The input speech was: {query}')
    except Exception as exception:
        print('I did not quite catch that')
        speak('I did not quite catch that')
        print(exception)
        return 'None'
    
    return query

def search_wikipedia(query = ''):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print('No wikipedia result')
        return 'No result received'
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary

if __name__ == '__main__':
    speak('All systems normal.')
    
    while True:
        query = parseCommand().lower().split()
        
        if query[0] == activationWord:
            query.pop(0)
            
            if query[0] == 'say':
                if 'hello' in query:
                    speak('Greetings, all.')
                else:
                    query.pop(0)
                    speech = ' '.join(query)
                    speak(speech)
                    
            if query[0] == 'go' and query[1] == 'to':
                speak('Opening...')
                query = ' '.join(query[2:])
                webbrowser.get('chrome').open_new(query)
                
            if query[0] == 'search':
                query = ' '.join(query[1:])
                speak('Querying the universal databank')
                speak(search_wikipedia(query))
                