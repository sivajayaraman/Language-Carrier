import subprocess
import os
import shutil
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
from tkinter.ttk import Progressbar
from googletrans import Translator
from gtts import gTTS
from pydub import AudioSegment

def clearFiles():
	try:
		open("recognized.txt","w").close()
		open("retry.txt","w").close()
		open("unrecognized.txt","w").close()
		open("translatedText.txt","w").close()
	except(FileNotFoundError):
		tkinter.messagebox.showerror("Error","Clearing Files Error. Try after creating required files.")
	except:
		tkinter.messagebox.showerror("Error","Files not cleared properly. Do it mannualy or retry")

def updateDisplayLabel(displayString,sleepTime):
    try:
        print(displayString)
        label.config(font=("Courier",20))
        displayLabel.set(displayString)
        root.update()
        root.update_idletasks()
        time.sleep(sleepTime)
    except:
    	tkinter.messagebox.showerror("Error","Error while updating status!")

def textToOtherLanguage(root):
    try:
        root.title("Audio Development")
        root.update()
        root.deiconify()
        progress['value'] = 10
        updateDisplayLabel("Audio Development Initiated",1)
        try:
            os.mkdir('translated_audio')
        except(FileExistsError):
            pass
        updateDisplayLabel("Reading the translated text file....",1.5)
        translatedText = open("translatedText.txt","r")
        os.chdir('translated_audio')
        audioMerge = AudioSegment.silent(1000)
        data = translatedText.readlines()
        size = len(data)
        increment = 40/size
        increment = int(increment)
        progressValue = 10
        i = 1
        for line in data:
            updateDisplayLabel("Develping audio for line " + str(i) + " --- "+ time.ctime(),0)
            audio = gTTS(text=line, lang="ta", slow=False)
            filename = "translated_" + str(i) + ".mp3"
            audio.save(filename)
            updateDisplayLabel("Translated audio saved as " + filename + " --- " + time.ctime(),1.5)
            i = i + 1
            progressValue = progressValue + increment
            progress['value'] = progressValue
            root.update_idletasks()
        translatedText.close()
        path = os.getcwd()
        updateDisplayLabel("Audio chunks developed succesfully --- " + time.ctime(),2)
        updateDisplayLabel("Audio translated and stored in location\n "  + path ,2)
        progress['value'] = 50
        updateDisplayLabel("Audio Files Merging Initiated",2)
        size = i - 1
        increment = 50/size
        increment = int(increment)
        progressValue = 50
        i = 1
        for filename in glob.glob(os.path.join(path,"*.mp3")):
            updateDisplayLabel("Merging Audio File translated_" +str(i) + ".mp3 --- " + time.ctime(),2)
            audio = AudioSegment.from_mp3(filename)
            audioMerge = audioMerge + audio
            i = i + 1
            progressValue = progressValue + increment
            progress['value'] = progressValue    
            root.update_idletasks()
        updateDisplayLabel("Audio files merged and stored at location \n" + os.getcwd() + " --- " + time.ctime(),2)    
        os.chdir('..')
        path = os.getcwd()
        audioMerge.export(path+"/translatedAudio.mp3", format='mp3')
        progress['value'] = 100
        root.update_idletasks()
        tkinter.messagebox.showinfo("Audio Development Success","Audio successfully developed from the text")
    except:
        tkinter.messagebox.showerror("Error","Unexpected error while developing audio. Please try again!")    

def translateText(root):
    try:
        current_directory = os.getcwd()
        root.title("Text File Translation")
        root.update()
        root.deiconify()
        progress['value'] = 10
        updateDisplayLabel("Translation Initiated...",2)
        translator = Translator()
        translatedTextFile = open("translatedText.txt","+w")
        updateDisplayLabel("Reading Source text from file",2)
        path = current_directory + "/recognized.txt"
        recognized = open(path,"r")
        data = recognized.readlines()
        if data[len(data)-1] == '\n':
            data.pop()
        size = len(data)
        increment = 70/size
        increment = int(increment)
        progressValue = 10
        i = 1
        for line in data:
            updateDisplayLabel("Translating line " + str(i) + " --- " + time.ctime(), 1)
            translatedData = translator.translate(line.strip(), src = 'en', dest = 'ta')
            data = translatedData.text
            translatedTextFile.write(data+"\n")
            updateDisplayLabel("Line translated --- " + time.ctime(),1)
            i = i + 1
            progressValue = progressValue + increment
            progress['value'] = progressValue
            root.update_idletasks()
        recognized.close()    
        translatedTextFile.close()
        progress['value'] = 80
        updateDisplayLabel("Translation Completed",1.5)
        createAudio = tkinter.messagebox.askyesno("Audio Developement","Do you want to develop audio for this translation?", icon = "info")
        if createAudio == True:
            updateDisplayLabel("Initiating Audio Development",1)
            textToOtherLanguage(root)
        root.update()
        root.title("Text File Translation")
        root.update()
        root.deiconify()
        progress['value'] = 100
        updateDisplayLabel("Translated text file is stored at location\n" + current_directory + "/translatedText.txt",2)
        tkinter.messagebox.showinfo("Translation Success","Text translated successfully")
        root.destroy()
    except:
        try:
            root.destroy()
        except:
            pass    
        tkinter.messagebox.showerror("Error","Unexpected error while translating text. Please try again!")    

def audioToText(root):
    try:
        root.update()
        root.title("Audio To Text Conversion")
        progress['value'] = 10
        path = os.getcwd()
        progress['value'] = 20
        updateDisplayLabel("Resource file fetched and Audio extracted successfully....",1)
        progress['value'] = 30
        updateDisplayLabel("Extracted Audio is stored at " + path + " as audio.wav file....",1)
        progress['value'] = 40
        updateDisplayLabel("Executing Audio to Text Conversion",1)
        root.withdraw()
        command = "python3 source_translation.py"
        subprocess.call(command, shell=True)
        progress['value'] = 100
        updateDisplayLabel("Process Completed",2)
        tkinter.messagebox.showinfo("Translation Successful","Translation has been Sucessfully completed!")
        root.destroy()
    except:
        tkinter.messagebox.showerror("Error","Unexpected error while Translating audio. Please try again!")    

try:
    current_directory = os.getcwd()
    clearFiles()
    root = tkinter.Tk()
    root.withdraw()

    locationPath = filedialog.askopenfilename(initialdir=current_directory,title='Language Carrier',filetypes=(('text files','*.txt'),('video files','*.mp4'),('audio files','*.mp3'),('wav file','*.wav'),('all files','*.*'))) 
    root.update()
    root.title("Language Carrier")
    root.deiconify()
    root.update()
    root.geometry("1600x720")
    displayLabel = tkinter.StringVar()
    label = tkinter.Label(root, textvariable = displayLabel)
    label.config(font=("Courier",20))
    label.pack()
    spaceHolder = tkinter.Label(root)
    spaceHolder.config(height = 10, width = 20)
    spaceHolder.pack()
    progress = tkinter.ttk.Progressbar(root, orient = tkinter.HORIZONTAL, length = 800, mode = "determinate")
    progress.pack(anchor = tkinter.CENTER)
    progress['value'] = 50
    updateDisplayLabel("Seeking Location....",2)
    exception = False
    isFileExisting = os.path.isfile(locationPath)

    if isFileExisting == True:
        progress['value'] = 100
        progress.update_idletasks()
        updateDisplayLabel("File Fetched....",1.5)
        fileName,fileFormat = os.path.splitext(locationPath)
        if(fileFormat == '.mp4' or fileFormat == '.mp3' or fileFormat =='.wav'):
            root.destroy()
            root = tkinter.Tk()
            root.title("Audio Translation")
            root.update()
            root.geometry("1600x720")
            displayLabel = tkinter.StringVar()
            label = tkinter.Label(root, textvariable = displayLabel)
            label.config(font=("Courier",20))
            label.pack()
            spaceHolder = tkinter.Label(root)
            spaceHolder.config(height = 10, width = 20)
            spaceHolder.pack()
            progress = tkinter.ttk.Progressbar(root, orient = tkinter.HORIZONTAL, length = 800, mode = "determinate")
            progress.pack(anchor = tkinter.CENTER)
            button = tkinter.Button(root, text = "Proceed", command = lambda: audioToText(root))
            button.pack()
            isFileExisting = os.path.isfile('audio.wav')
            if isFileExisting == True:
                os.remove('audio.wav')
            command = "ffmpeg -i "+ locationPath +" -ab 20k -ac 2 -ar 44100 -vn audio.wav"
            subprocess.call(command, shell=True)    
            progress['value'] = 100
            progress.update_idletasks()
            updateDisplayLabel("Audio Extracted....",2)
            tkinter.messagebox.showinfo("Audio Extraction","Audio Extracted Successfully")
            root.update()
            root.mainloop()
        elif(fileFormat == '.txt'):
            progress['value'] = 100
            root.update_idletasks()
            root.destroy()
            root = tkinter.Tk()
            root.geometry("1600x720")
            root.title("Text Translation")
            displayLabel = tkinter.StringVar()
            label = tkinter.Label(root, textvariable = displayLabel)
            label.pack()
            spaceHolder = tkinter.Label(root)
            spaceHolder.config(height = 10, width = 20)
            spaceHolder.pack()
            progress = tkinter.ttk.Progressbar(root, orient = tkinter.HORIZONTAL, length = 800, mode = "determinate")
            progress.pack()
            textFile = open(locationPath,"r")
            progress['value'] = 10
            updateDisplayLabel("File Fetched --- " + time.ctime(),1.5)
            progress['value'] = 20
            updateDisplayLabel("Reading File Content --- " + time.ctime(),1.5)
            data = textFile.readlines()
            size = len(data)
            progressValue = 20
            increment = 40/size
            increment = int(increment)
            fileSentence = ""
            i = 1
            for line in data:
                updateDisplayLabel("Read Line "+ str(i) + " --- " + time.ctime(), 1)
                fileSentence = fileSentence + line
                i = i + 1    
                progressValue = progressValue + increment
                progress['value'] = progressValue
                root.update_idletasks()
            recognizedText = open("recognized.txt","+w")
            fileSentence = fileSentence.strip() + '. '
            sentences = re.split(r'[.?!][.?!\s]+', fileSentence)
            progress['value'] = 60
            updateDisplayLabel("Updating recognized.txt --- " + time.ctime(),1.5 )
            size = len(sentences)
            progressValue = 60
            increment = 35/size
            increment = int(increment)
            i = 0
            for line in sentences:
                updateDisplayLabel("Writing Line "+ str(i) + " --- " +time.ctime(),1)
                recognizedText.write(line+"\n")
                i = i + 1
                progressValue = progressValue + increment
                progress['value'] = progressValue
                root.update_idletasks()
            recognizedText.close()    
            progress['value'] = 95
            updateDisplayLabel("Writing Text File Completed --- " + time.ctime(), 0)
            progress['value'] = 100
            root.update_idletasks()
            tkinter.messagebox.showinfo("Text Conversion","Text file converted for translation Successfully!")
            progress['value'] = 0
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

except:
    try:
        root.destroy()
    except:
        pass    
    tkinter.messagebox.showerror("Error","Unexpected error while preprocessing. Please try again!")