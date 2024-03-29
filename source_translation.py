import subprocess
import os
import glob
import speech_recognition
import tkinter
import time
import googletrans
from pydub import AudioSegment
from pydub.silence import split_on_silence
from tkinter import Label
from tkinter import messagebox
from tkinter.ttk import Progressbar
from googletrans import Translator
from gtts import gTTS

def updateDisplayLabel(displayString,sleepTime):
	try:
		label.config(font=("Courier",20))
		print (displayString)
		displayLabel.set(displayString)
		root.update()
		root.update_idletasks()
		time.sleep(sleepTime)
	except:
		tkinter.messagebox.showerror("Error","Error while updating status!")	

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

def textToOtherLanguage():
	try:
		button.pack_forget()
		cancel.pack_forget()
		progress.pack()
		cancel.pack()
		root.update()
		progress['value'] = 10
		updateDisplayLabel("Audio Development Initiated",2)
		try:
			os.mkdir('translated_audio')
		except(FileExistsError):
			pass
		updateDisplayLabel("Reading the translated text file....",1.5)
		translatedText = open("translatedText.txt","r")
		progress['value'] = 12
		updateDisplayLabel("translated_audio directory created and\n home directory changed to translated_audio directory",1.5)
		os.chdir('translated_audio')
		progress['value'] = 15
		updateDisplayLabel("Reading translated text from translatedText.txt",1)
		audioMerge = AudioSegment.silent(500)
		data = translatedText.readlines()
		size = len(data)
		progressValue = 15
		increment = int(size/35)
		increment = int(increment)
		i = 1
		for line in data:
			updateDisplayLabel("Developing audio for line " + str(i) + "\n--- "+ time.ctime(),0)
			audio = gTTS(text=line, lang="ta", slow=False) 
			filename = "translated_" + str(i) + ".mp3"
			audio.save(filename) 
			updateDisplayLabel("Translated audio saved as " + filename + "\n--- " + time.ctime(),1.5)
			i = i + 1
			progressValue = progressValue + increment
			progress['value'] = progressValue
			root.update_idletasks()
		translatedText.close()
		path = os.getcwd()
		progress['value'] = 50
		updateDisplayLabel("Audio chunks developed succesfully --- " + time.ctime(),1.5)
		updateDisplayLabel("Audio translated and stored in location\n" + path + "/translated_audio",1.5)
		updateDisplayLabel("Audio Files Merging Initiated",1.5)
		size = i - 1
		progressValue = 50
		increment = size/50
		increment = int(increment)
		i = 1
		for filename in glob.glob(os.path.join(path,"*.mp3")):
			updateDisplayLabel("Merging Audio File translated_" +str(i) + ".mp3 \n--- " + time.ctime(),1)
			audio = AudioSegment.from_mp3(filename)
			audioMerge = audioMerge + audio
			i = i + 1    
			progressValue = progressValue + increment
			progress['value'] = progressValue
			root.update_idletasks()
		updateDisplayLabel("Audio files merged and stored at location \n" + os.getcwd() + " --- " + time.ctime(),1)    
		os.chdir('..')
		path = os.getcwd()
		audioMerge.export(path+"/translatedAudio.mp3", format='mp3')
		progress['value'] = 100
		updateDisplayLabel("Audio translated and stored in location " + path, 1.5)
		tkinter.messagebox.showinfo("Audio Development Success","Audio successfully developed from the text")
		root.destroy()
	except:
		try:
			root.destroy()
		except:
			pass	
		tkinter.messagebox.showerror("Error","Unexpected error while developing audio. Please try again!")

def translateText():
	try:
		button.pack_forget()
		cancel.pack_forget()
		progress.pack()
		cancel.pack()
		root.update()
		path = os.getcwd()
		progress['value'] = 10
		updateDisplayLabel("Translation Initiated",1.5)
		translator = Translator()
		translatedTextFile = open("translatedText.txt","+w")
		progress['value'] = 20
		updateDisplayLabel("Reading Recognized Text from file",1.5)
		recognized = open("recognized.txt","r")
		data = recognized.readlines()
		size = len(data)
		progressValue = 20
		increment = 70/size
		increment = int(increment)
		i = 1
		for line in data:
			updateDisplayLabel("Translating line " + str(i) +" --- "+ time.ctime(),1.5)
			translatedData = translator.translate(line.strip(), src = 'en', dest = 'ta')
			data = translatedData.text
			if len(data) != 0:  
				translatedTextFile.write(data+"\n")
				updateDisplayLabel("Line translated --- " + time.ctime(),1.5)
			progressValue = progressValue + increment
			progress['value'] = progressValue
			i = i + 1
		progress['value'] = 90
		updateDisplayLabel("Translation Completed",1.5)
		progress['value'] = 95
		updateDisplayLabel("Translated text file is stored at location\n" + path + "/translatedText.txt",1.5)
		tkinter.messagebox.showinfo("Translation Success","Text translated successfully")
		progress['value'] = 100
		updateDisplayLabel("Initiating Audio Conversion",1)
		root.destroy()
	except:
		try:
			root.destroy()
		except:
			pass
		tkinter.messagebox.showerror("Error","Unexpected error occured. Please try again!")		

def silence_based_conversion():	
	try:
		retryFile = False
		unrecognizedFile = False
		button.pack_forget()
		cancel.pack_forget()
		progress.pack()
		cancel.pack()
		root.update()
		path = os.getcwd()
		progress['value'] = 10 
		updateDisplayLabel("Source Location " + path + "/audio.wav", 1.5 )
		
		clearFiles()
		audio = AudioSegment.from_wav(path + "/audio.wav")
		recognized = open("recognized.txt","w+")
		unrecognized = open("unrecognized.txt","w+")
		retry = open("retry.txt","w+")
		progress['value'] = 20
		updateDisplayLabel("Splitting the Audio into chunks \n This may take a while...",1.5)
		chunks = split_on_silence(audio, min_silence_len = 750, silence_thresh = -30)
		updateDisplayLabel("Audio chunks successfully splitted", 1.5)
		size = len(chunks)
		progressValue = 20
		increment = 80/size
		increment = int(increment)
		try:
			os.mkdir('audio_chunks')
		except(FileExistsError):
			pass
		
		updateDisplayLabel("audio_chunks directory created and\n home directory changed to audio_chunks",1)
		os.chdir('audio_chunks')
		i = 0
		for chunk in chunks:
			root.update()
			chunk_silent = AudioSegment.silent(duration = 100)	
			audio_chunk = chunk_silent + chunk + chunk_silent
			updateDisplayLabel("Saving chunk{0}.wav --- ".format(i) + time.ctime(),0.75)
			audio_chunk.export("./chunk{0}.wav".format(i), bitrate = '192k', format = "wav")
			filename = 'chunk' + str(i)+ '.wav'
			updateDisplayLabel("Processing chunk " + str(i)+" --- "+ time.ctime(),0.75)
			file = filename
			r = speech_recognition.Recognizer()

			with speech_recognition.AudioFile(file) as source:
				r.adjust_for_ambient_noise(source)
				audio_listened = r.listen(source)

			try:
				rec = r.recognize_google(audio_listened)
				recognized.write( rec + ".\n" )
			
			except speech_recognition.UnknownValueError:
				unrecognizedFile = True
				print("Could not understand audio")
				print("Storing audio chunk as unconvertible chunk")
				audio_chunk = audio_chunk._spawn(audio_chunk.raw_data, overrides={"frame_rate": int(audio_chunk.frame_rate * 0.90)})
				with speech_recognition.AudioFile(file) as source:
					r.adjust_for_ambient_noise(source)
					audio_listened = r.listen(source)
				try:
					rec = r.recognize_google_cloud(audio_listened)
					recognized.write( rec + ".\n")
				except:
					unrecognized.write(filename + "\n")
					pass

			except speech_recognition.RequestError:
				retryFile = True
				print("Connectivity Failure!")
				print("Loading audio chunk in failed chunks for retrying")
				with speech_recognition.AudioFile(file) as source:
					r.adjust_for_ambient_noise(source)
					audio_listened = r.listen(source)
				try:
					rec = r.recognize_google_cloud(audio_listened)
					recognized.write( rec + ".\n")
				except:
					retry.write(filename + "\n")
					pass
			progressValue = progressValue + increment
			progress['value'] = progressValue
			root.update_idletasks()
			i = i + 1
		recognized.close()
		unrecognized.close()
		retry.close()
		updateDisplayLabel("Total number of chunks processed : " + str(i),1)
		updateDisplayLabel("Recognized text from audio file is stored at location\n" + path + "/recognized.txt",1.5)
		updateDisplayLabel("Unrecognized audio chunks is stored at location\n " + path + "/unrecognized.txt",1.5)
		updateDisplayLabel("Retry required audio chunks is stored at location\n " + path + "/retry.txt",1.5)
		progress['value'] = 100
		root.update_idletasks()
		tkinter.messagebox.showinfo("Audio Conversion Success", "Successfully converted Audio to Text")
		os.chdir('..')
		print("Returned to home directory.....")
		if unrecognizedFile == True:
			response = tkinter.messagebox.askyesno("Try Unrecognized Files","Do you want to retry to recognize unrecognized files?")
			if response == True:
				tkinter.messagebox.showinfo("Unrecognized FIle Information","Unrecognized file has been retried already! If results arent sattisfactory, Sorry!")
		if retryFile == True:
			response = tkinter.messagebox.askyesno("Retry Files","Do you want to recognize connectivity failed files?")
			if response == True:
				tkinter.messagebox.showinfo("Unrecognized FIle Information","Connectivity failed file has been retried already! If results arent sattisfactory, Sorry!")
		updateDisplayLabel("Initiating Language Translation....",1.5)
		root.destroy()
	except:
		try:
			root.destroy()
		except:
			pass	
		tkinter.messagebox.showerror("Error","Unexpected error while processing audio. Please try again!")
try:
	clearFiles()
	root = tkinter.Tk()
	root.title("Audio Handling")
	root.geometry("1600x720")
	displayLabel = tkinter.StringVar()
	label = tkinter.Label(root, textvariable = displayLabel)
	label.config(font=("Courier",20))
	label.pack()
	spaceHolder = tkinter.Label(root)
	spaceHolder.config(height = 10, width = 20)
	spaceHolder.pack()
	progress = tkinter.ttk.Progressbar(root, orient = tkinter.HORIZONTAL, length = 800, mode = "determinate")
	button = tkinter.Button(root,text  = "Proceed", command = lambda: silence_based_conversion())
	button.pack()
	cancel = tkinter.Button(root,text = "Cancel", command = lambda: root.destroy())
	cancel.pack()
	root.update()
	root.mainloop()

	root = tkinter.Tk()
	root.title("Text Translation")
	root.geometry("1600x720")
	displayLabel = tkinter.StringVar()
	label = tkinter.Label(root, textvariable = displayLabel)
	label.config(font=("Courier",20))
	label.pack()
	spaceHolder = tkinter.Label(root)
	spaceHolder.config(height = 10, width = 20)
	spaceHolder.pack()
	progress = tkinter.ttk.Progressbar(root, orient = tkinter.HORIZONTAL, length = 800, mode = "determinate")
	button = tkinter.Button(root,text = "Translate Text", command = lambda: translateText())
	button.pack()
	cancel = tkinter.Button(root,text = "Cancel", command = lambda: root.destroy())
	cancel.pack()
	root.update()
	root.mainloop()

	root = tkinter.Tk()
	root.title("Audio Development")
	root.geometry("1600x720")
	displayLabel = tkinter.StringVar()
	label = tkinter.Label(root, textvariable = displayLabel)
	label.config(font=("Courier",20))
	label.pack()
	spaceHolder = tkinter.Label(root)
	spaceHolder.config(height = 10, width = 20)
	spaceHolder.pack()
	progress = tkinter.ttk.Progressbar(root, orient = tkinter.HORIZONTAL, length = 800, mode = "determinate")
	button = tkinter.Button(root,text = "Develop Audio from Text", command = lambda: textToOtherLanguage())
	button.pack()
	cancel = tkinter.Button(root,text = "Cancel", command = lambda: root.destroy())
	cancel.pack()
	root.update()
	root.mainloop()
except:
	try:
		root.destroy()
	except:
		pass
	tkinter.messagebox.showerror("Error","Unexpected error while translating audio. Please try again!")