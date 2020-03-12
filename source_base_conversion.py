import subprocess
import os
import wave
import glob
import time
import re
import tkinter
import googletrans
from tkinter import filedialog
from tkinter import messagebox
from tkinter import StringVar
from tkinter import Label
from googletrans import Translator
from gtts import gTTS
from pydub import AudioSegment

def clearFiles():
	open("recognized.txt","w").close()
	open("retry.txt","w").close()
	open("unrecognized.txt","w").close()
	open("translatedText.txt","w").close()

def updateDisplayLabel(displayString,sleepTime):
	displayLabel.set(displayString)
	root.update()
	time.sleep(sleepTime)

def textToOtherLanguage(root):
    root.title("Audio Development")
    root.update()
    root.deiconify()
    updateDisplayLabel("Audio Development Initiated",1.5)
    try:
        os.mkdir('translated_audio')
    except(FileExistsError):
        pass
    updateDisplayLabel("Reading the translated text file....",2)
    translatedText = open("translatedText.txt","r")
    print("translated_audio directory created and home directory changed to translated_audio directory .....")
    os.chdir('translated_audio')
    print("Reading translated text from translatedText.txt")
    audioMerge = AudioSegment.silent(1000)
    data = translatedText.readlines()
    i = 1
    for line in data:
        updateDisplayLabel("Develping audio for line " + str(i) + "---"+ time.ctime(),0)
        print("Develping audio for line " + str(i) + "---"+ time.ctime())
        audio = gTTS(text=line, lang="ta", slow=False)
        filename = "translated_" + str(i) + ".mp3"
        audio.save(filename)
        updateDisplayLabel("Translated audio saved as " + filename + "---" + time.ctime(),3)
        i = i + 1
    translatedText.close()
    updateDisplayLabel("Audio chunks developed succesfully ---" + time.ctime(),2)
    updateDisplayLabel("Audio translated and stored in location\n /home/siva/Translator/translated_audio",3)
    path = os.getcwd()
    updateDisplayLabel("Audio Files Merging Initiated",2)
    i = 1
    for filename in glob.glob(os.path.join(path,"*.mp3")):
        updateDisplayLabel("Merging Audio File translated_" +str(i) + ".mp3 ---" + time.ctime(),2)
        print("Merging Audio File translated_" +str(i) + ".mp3 ---" + time.ctime())
        audio = AudioSegment.from_mp3(filename)
        audioMerge = audioMerge + audio
        i = i + 1    
    updateDisplayLabel("Audio files merged and stored at location \n" + os.getcwd() + "---" + time.ctime(),2)    
    os.chdir('..')
    path = os.getcwd()
    audioMerge.export(path+"/translatedAudio.mp3", format='mp3')
    print("Audio translated and stored in location " + path )
    tkinter.messagebox.showinfo("Audio Development Success","Audio successfully developed from the text")

def translateText(root):
    current_directory = os.getcwd()
    root.title("Text File Translation")
    root.update()
    root.deiconify()
    updateDisplayLabel("Translation Initiated...",2)
    translator = Translator()
    languages = googletrans.LANGUAGES
    translatedTextFile = open("translatedText.txt","+w")
    updateDisplayLabel("Reading Source text from file",2)
    print("Reading Recognized Text from file....")
    path = current_directory + "/recognized.txt"
    recognized = open(path,"r")
    data = recognized.readlines()
    if data[len(data)-1] == '\n':
        data.pop()
    i = 1
    for line in data:
        print("Translating line " + str(i) + "---" + time.ctime())
        detect = translator.detect(line)
        sourceLanguage = detect.lang
        sourceLanguage = languages.__getitem__(sourceLanguage)
        updateDisplayLabel("Source Language is "+sourceLanguage,1)
        updateDisplayLabel("Translating line " + str(i) +"---"+ time.ctime(),1.5)
        translatedData = translator.translate(line.strip(), src=detect.lang,dest='ta')
        data = translatedData.text
        translatedTextFile.write(data+"\n")
        updateDisplayLabel("Line translated ---" + time.ctime(),1.5)
        i = i + 1
    recognized.close()    
    translatedTextFile.close()
    updateDisplayLabel("Translation Completed",1.5)
    print("Done Translating....")
    createAudio = tkinter.messagebox.askyesno("Audio Developement","Do you want to develop audio for this translation?", icon = "info")
    if createAudio == True:
        updateDisplayLabel("Initiating Audio Development",1.5)
        textToOtherLanguage(root)
    root.update()
    root.title("Text File Translation")
    root.update()
    root.deiconify()
    updateDisplayLabel("Translated text file is stored at location\n /home/siva/Translator/translatedText.txt",2)
    tkinter.messagebox.showinfo("Translation Success","Text translated successfully")
    print("Translated text file is stored at location /home/siva/Translator/translatedText.txt ")
    root.destroy()

def audioToText():
    print("Resource file fetched and Audio extracted successfully....")
    print("Extracted Audio is stored at /home/siva/Translator as audio.wav file....")
    print("Executing Audio to Text Conversion.....")
    root.withdraw()
    command = "python3 source_translation.py"
    subprocess.call(command, shell=True)
    tkinter.messagebox.showinfo("Translation Successful","Translation has been Sucessfully completed!")
    print("Process Completed....")
    root.destroy()

clearFiles()
root = tkinter.Tk()
root.withdraw()

current_directory = os.getcwd()
locationPath = filedialog.askopenfilename(initialdir=current_directory,title='Language Carrier',filetypes=(('text files','*.txt'),('video files','*.mp4'),('audio files','*.mp3'),('wav file','*.wav'),('all files','*.*'))) 
print (locationPath)
root.update()
root.title("Language Carrier")
root.deiconify()
root.geometry("800x240")
displayLabel = tkinter.StringVar()
label = tkinter.Label(root, textvariable = displayLabel)
label.pack()
updateDisplayLabel("Seeking Location....",2)
exception = False
isFileExisting = os.path.isfile(locationPath)

if isFileExisting == True:
    updateDisplayLabel("File Fetched....",2)
    fileName,fileFormat = os.path.splitext(locationPath)
    if(fileFormat == '.mp4' or fileFormat == '.mp3' or fileFormat =='.wav'):
        root.title("Audio Translation")
        root.update()
        isFileExisting = os.path.isfile('audio.wav')
        if isFileExisting == True:
            os.remove('audio.wav')
        command = "ffmpeg -i "+ locationPath +" -ab 20k -ac 2 -ar 44100 -vn audio.wav"
        subprocess.call(command, shell=True)    
        updateDisplayLabel("Audio Extracted....",2)
        tkinter.messagebox.showinfo("Audio Extraction","Audio Extracted Successfully")
        button = tkinter.Button(root, text = "Proceed", command = audioToText)
        button.pack()
        tkinter.mainloop()
    elif(fileFormat == '.txt'):
        root.destroy()
        root = tkinter.Tk()
        root.geometry("800x240")
        root.title("Text Translation")
        displayLabel = tkinter.StringVar()
        label = tkinter.Label(root, textvariable = displayLabel)
        label.pack()
        textFile = open(locationPath,"r")
        print("File Fetched ---" + time.ctime())
        updateDisplayLabel("File Fetched",1.5)
        print("Reading File Contents ---" + time.ctime())
        updateDisplayLabel("Reading File Content...",1.5)
        data = textFile.readlines()
        fileSentence = ""
        i = 1
        for line in data:
            print("Read Line "+ str(i) + "---" + time.ctime())
            updateDisplayLabel("Read Line "+ str(i) + "---" + time.ctime(), 1)
            fileSentence = fileSentence + line
            i = i + 1    
        recognizedText = open("recognized.txt","+w")
        fileSentence = fileSentence.strip() + '. '
        sentences = re.split(r'[.?!][.?!\s]+', fileSentence)
        print("Updating recognized.txt ---" + time.ctime())
        updateDisplayLabel("Updating recognized.txt ---" + time.ctime(),1.5 )
        i = 0
        for line in sentences:
            print("Writing Line "+ str(i) + "---" +time.ctime())
            updateDisplayLabel("Writing Line "+ str(i) + "---" +time.ctime(),1)
            recognizedText.write(line+"\n")
            i = i + 1
        recognizedText.close()    
        print("Writing Text File Completed ---" + time.ctime())
        updateDisplayLabel("Writing Text File Completed ---" + time.ctime(), 0)
        tkinter.messagebox.showinfo("Text Conversion","Text file converted for translation Successfully!")
        print("Initiating Text Translation ---" + time.ctime() )
        updateDisplayLabel("Initiating Text Translation",1.5)
        translateText(root)
    else:
        tkinter.messagebox.showerror("Error","Unsupported File format!")
        exception = True
else:
    tkinter.messagebox.showerror("Error","File Not Found!\nCheck if file has execution premissions")

if exception == True:
    tkinter.messagebox.showwarning("Failure Warning","Translation Failed! Please Retry")
    print("Unsuccessful Conversion. Please Try Again!!!")

clearFiles()