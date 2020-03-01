from googletrans import Translator
from gtts import gTTS
import languageAudio

def translateText():

    translator = Translator()
    translatedTextFile = open("translatedText.txt","+w")
    print("Reading Recognized Text from file....")
    recognized = open("recognized.txt","r")
    data = recognized.readlines()
    for line in data: 
        translatedData = translator.translate(line.strip(), src='en',dest='ta')
        data = translatedData.text
        translatedTextFile.write(data+"\n")
    print("Done Translating....")
    print("Translated text file is stored at location /home/siva/Translator/translatedText.txt ")

translateText()
languageAudio.textToOtherLanguage()