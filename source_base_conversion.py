import subprocess
import os
import time
import tkinter
from tkinter import filedialog
from tkinter.ttk import Progressbar
from tkinter import Frame
from tkinter import messagebox

def updateDisplayLabel(displayString,sleepTime):
	displayLabel.set(displayString)
	root.update()
	time.sleep(sleepTime)

def audioToText():
    print("Resource file fetched and Audio extracted successfully....")
    print("Extracted Audio is stored at /home/siva/Translator as audio.wav file....")
    print("Executing Audio to Text Conversion.....")
    root.withdraw()
    command = "python3 source_translation.py"
    subprocess.call(command, shell=True)
    tkinter.messagebox.showinfo("Successfull Completion","The Translation is Successfull!")
    print("Process Completed....")
    root.destroy()

root = tkinter.Tk()
root.withdraw()

current_directory = os.getcwd()
locationPath = filedialog.askopenfilename(initialdir=current_directory,title='Language Carrier',filetypes=(('text files','*.txt'),('video files','*.mp4'),('audio files','*.mp3'),('wav file','*.wav'),('all files','*.*'))) 
print (locationPath)
root.update()
root.title("Audio Extraction")
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
    print(fileFormat)
    if(fileFormat == '.mp4' or fileFormat == '.mp3' or fileFormat =='.wav'):
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
        print("Handle for direct text file here")
        exception = True
    else:
        tkinter.messagebox.showerror("Error","Unsupported File format!")
        exception = True
else:
    tkinter.messagebox.showerror("Error","File Not Found!\nCheck if file has execution premissions")

if exception == True:
    tkinter.messagebox.showwarning("Failure Warning","Translation Failed! Please Retry")
    print("Unsuccessful Conversion. Please Try Again!!!")