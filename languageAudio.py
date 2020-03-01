from gtts import gTTS
import os

def textToOtherLanguage():
    
    try:
	    os.mkdir('translated_audio')
    except(FileExistsError):
	    pass
	
    print("translated_audio directory created and home directory changed to translated_audio directory .....")
    os.chdir('translated_audio')\

    print("Reading translated text from translatedText.txt")
    translatedText = open("translatedText.txt","r")

    data = translatedText.readlines()
    i = 0
    for line in data:
        audio = gTTS(text=line, lang="ta", slow=False) 
        filename = "translated_" + str(i) + ".mp3"
        audio.save(filename) 
        i = i + 1
    print("Audio translated and stored in location /home/siva/Translator/translated_audio")    
    os.chdir('..')
textToOtherLanguage()