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
		label.config(font=("Courier",30))
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
		print("Audio Development Initiated --- " + time.ctime() )
		updateDisplayLabel("Audio Development Initiated",2)
		try:
			os.mkdir('translated_audio')
		except(FileExistsError):
			pass
		progress['value'] = 20
		print("Reading the translated text file....")
		updateDisplayLabel("Reading the translated text file....",1.5)
		translatedText = open("translatedText.txt","r")
		progress['value'] = 25
		print("translated_audio directory created and home directory changed to translated_audio directory .....")
		updateDisplayLabel("translated_audio directory created and\n home directory changed to translated_audio directory",1.5)
		os.chdir('translated_audio')
		progress['value'] = 50
		print("Reading translated text from translatedText.txt")
		updateDisplayLabel("Reading translated text from translatedText.txt",1)
		audioMerge = AudioSegment.silent(500)
		data = translatedText.readlines()
		i = 1
		for line in data:
			updateDisplayLabel("Developing audio for line " + str(i) + "\n--- "+ time.ctime(),0)
			print("Devoloping audio for line " + str(i) + " --- " + time.ctime())
			audio = gTTS(text=line, lang="ta", slow=False) 
			filename = "translated_" + str(i) + ".mp3"
			audio.save(filename) 
			updateDisplayLabel("Translated audio saved as " + filename + "\n--- " + time.ctime(),1.5)
			i = i + 1
		translatedText.close()
		path = os.getcwd()
		progress['value'] = 60
		print("Audio chunks developed succesfully --- " + time.ctime())
		updateDisplayLabel("Audio chunks developed succesfully --- " + time.ctime(),1.5)
		print("Audio translated and stored in location\n" + path + "/translated_audio")
		updateDisplayLabel("Audio translated and stored in location\n" + path + "/translated_audio",1.5)
		print("Audio Files Merging Initiated")
		progress['value'] = 80
		updateDisplayLabel("Audio Files Merging Initiated",1.5)
		i = 1
		for filename in glob.glob(os.path.join(path,"*.mp3")):
			updateDisplayLabel("Merging Audio File translated_" +str(i) + ".mp3 \n--- " + time.ctime(),1)
			print("Merging Audio File translated_" +str(i) + ".mp3 --- " + time.ctime())
			audio = AudioSegment.from_mp3(filename)
			audioMerge = audioMerge + audio
			i = i + 1    
		print("Audio files merged and stored at location \n" + os.getcwd() + " --- " + time.ctime())
		updateDisplayLabel("Audio files merged and stored at location \n" + os.getcwd() + " --- " + time.ctime(),1)    
		os.chdir('..')
		path = os.getcwd()
		audioMerge.export(path+"/translatedAudio.mp3", format='mp3')
		progress['value'] = 100
		print("Audio translated and stored in location " + path )
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
		print("Reading Recognized Text from file....")
		recognized = open("recognized.txt","r")
		data = recognized.readlines()
		i = 1
		for line in data:
			updateDisplayLabel("Translating line " + str(i) +" --- "+ time.ctime(),1.5)
			print("Translating line " + str(i) +" ---  "+ time.ctime())
			translatedData = translator.translate(line.strip(), src = 'en', dest = 'ta')
			data = translatedData.text
			if len(data) != 0:  
				translatedTextFile.write(data+"\n")
				updateDisplayLabel("Line translated --- " + time.ctime(),1.5)
			print("Line translated ---" + time.ctime())
			i = i + 1
		progress['value'] = 50
		updateDisplayLabel("Translation Completed",1.5)
		print("Done Translating....")
		progress['value'] = 80
		updateDisplayLabel("Translated text file is stored at location\n" + path + "/translatedText.txt",1.5)
		tkinter.messagebox.showinfo("Translation Success","Text translated successfully")
		progress['value'] = 100
		updateDisplayLabel("Initiating Audio Conversion",1)
		print("Translated text file is stored at location" + path + "/translatedText.txt")
		root.destroy()
	except:
		try:
			root.destroy()
		except:
			pass
		tkinter.messagebox.showerror("Error","Unexpected error occured. Please try again!")		

def silence_based_conversion():	
	try:
		button.pack_forget()
		cancel.pack_forget()
		progress.pack()
		cancel.pack()
		root.update()
		path = os.getcwd()
		progress['value'] = 10 
		updateDisplayLabel("Source Location " + path + "/audio.wav", 1.5 )
		print("Souce Location : " + path + "/audio.wav" )
		
		clearFiles()
		audio = AudioSegment.from_wav(path + "/audio.wav")
		recognized = open("recognized.txt","w+")
		unrecognized = open("unrecognized.txt","w+")
		retry = open("retry.txt","w+")
		print("Audio fetched and preparing to split.... Splitting Chunks.....")
		print("This may take a while.....")
		progress['value'] = 20
		updateDisplayLabel("Splitting the Audio into chunks \n This may take a while...",1.5)
		chunks = split_on_silence(audio, min_silence_len = 750, silence_thresh = -30)
		print("Audio chunks successfully splitted .....")
		progress['value'] = 40
		updateDisplayLabel("Audio chunks successfully splitted", 1.5)
	
		try:
			os.mkdir('audio_chunks')
		except(FileExistsError):
			pass
		
		progress['value'] = 50
		print("audio_chunks directory created and home directory changed to audio_chunks .....")
		updateDisplayLabel("audio_chunks directory created and\n home directory changed to audio_chunks",1)
		os.chdir('audio_chunks')

		i = 0
		for chunk in chunks:
			root.update()
			chunk_silent = AudioSegment.silent(duration = 100)	
			audio_chunk = chunk_silent + chunk + chunk_silent
			#audio_chunk = audio_chunk._spawn(audio_chunk.raw_data, overrides={"frame_rate": int(audio_chunk.frame_rate * 0.90)})
			updateDisplayLabel("Saving chunk{0}.wav --- ".format(i) + time.ctime(),0.75)
			print("Saving chunk{0}.wav ---".format(i) + time.ctime())
			audio_chunk.export("./chunk{0}.wav".format(i), bitrate = '192k', format = "wav")
			filename = 'chunk' + str(i)+ '.wav'
			print("Processing chunk " + str(i))
			updateDisplayLabel("Processing chunk " + str(i)+"---"+ time.ctime(),0.75)
			file = filename
			r = speech_recognition.Recognizer()

			with speech_recognition.AudioFile(file) as source:
				r.adjust_for_ambient_noise(source)
				audio_listened = r.listen(source)

			try:
				rec = r.recognize_google(audio_listened)
				recognized.write( rec + ".\n" )
			
			except speech_recognition.UnknownValueError:
				print("Could not understand audio")
				print("Storing audio chunk as unconvertible chunk")
				unrecognized.write(filename + "\n")

			except speech_recognition.RequestError:
				print("Connectivity Failure!")
				print("Loading audio chunk in failed chunks for retrying")
				retry.write(filename + "\n")

			i += 1
		recognized.close()
		unrecognized.close()
		retry.close()	
		progress['value'] = 80
		updateDisplayLabel("Total number of chunks processed : " + str(i),1.5)
		updateDisplayLabel("Recognized text from audio file is stored at location\n" + path + "/recognized.txt",1.5)
		updateDisplayLabel("Unrecognized audio chunks is stored at location\n " + path + "/unrecognized.txt",1.5)
		updateDisplayLabel("Retry required audio chunks is stored at location\n " + path + "/retry.txt",1.5)
		progress['value'] = 100
		root.update_idletasks()
		tkinter.messagebox.showinfo("Audio Conversion Success", "Successfully converted Audio to Text")
		print("Total number of chunks processed : " + str(i) )
		os.chdir('..')
		print("Returned to home directory.....")
		print("Recognized text from audio file is stored at location " + path + "/recognized.txt")
		print("Unrecognized audio chunks is stored at location " + path + "/unrecognized.txt")
		print("Retry required audio chunks is stored at location " + path + "/retry.txt")
		print("Converting text to another language....")
		updateDisplayLabel("Initiating Language Translation....",2)
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
	progress = tkinter.ttk.Progressbar(root, orient = tkinter.HORIZONTAL, length = 300, mode = "determinate")
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
	progress = tkinter.ttk.Progressbar(root, orient = tkinter.HORIZONTAL, length = 300, mode = "determinate")
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
	progress = tkinter.ttk.Progressbar(root, orient = tkinter.HORIZONTAL, length = 300, mode = "determinate")
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