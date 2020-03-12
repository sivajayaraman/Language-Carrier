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
from googletrans import Translator
from googletrans import LANGUAGES
from gtts import gTTS

def updateDisplayLabel(displayString,sleepTime):
	displayLabel.set(displayString)
	root.update()
	time.sleep(sleepTime)

def clearFiles():
	open("recognized.txt","w").close()
	open("retry.txt","w").close()
	open("unrecognized.txt","w").close()
	open("translatedText.txt","w").close()

def textToOtherLanguage():
	print("Audio Development Initiated ---" + time.ctime() )
	updateDisplayLabel("Audio Development Initiated",2)
	try:
	    os.mkdir('translated_audio')
	except(FileExistsError):
	    pass
	print("Reading the translated text file....")
	updateDisplayLabel("Reading the translated text file....",1.5)
	translatedText = open("translatedText.txt","r")
	print("translated_audio directory created and home directory changed to translated_audio directory .....")
	os.chdir('translated_audio')
	print("Reading translated text from translatedText.txt")
	audioMerge = AudioSegment.silent(1000)
	data = translatedText.readlines()
	i = 1
	for line in data:
		updateDisplayLabel("Translating line " + str(i) + "---"+ time.ctime(),0)
		print("Translating line " + str(i))
		audio = gTTS(text=line, lang="ta", slow=False) 
		filename = "translated_" + str(i) + ".mp3"
		audio.save(filename) 
		updateDisplayLabel("Translated audio saved as " + filename + "---" + time.ctime(),1.5)
		i = i + 1
	translatedText.close()
	updateDisplayLabel("Audio chunks developed succesfully ---" + time.ctime(),1.5)
	updateDisplayLabel("Audio translated and stored in location\n /home/siva/Translator/translated_audio",1.5)
	path = os.getcwd()
	updateDisplayLabel("Audio Files Merging Initiated",1.5)
	i = 1
	for filename in glob.glob(os.path.join(path,"*.mp3")):
	    updateDisplayLabel("Merging Audio File translated_" +str(i) + ".mp3 ---" + time.ctime(),1.5)
	    print("Merging Audio File translated_" +str(i) + ".mp3 ---" + time.ctime())
	    audio = AudioSegment.from_mp3(filename)
	    audioMerge = audioMerge + audio
	    i = i + 1    
	updateDisplayLabel("Audio files merged and stored at location \n" + os.getcwd() + "---" + time.ctime(),1.5)    
	os.chdir('..')
	path = os.getcwd()
	audioMerge.export(path+"/translatedAudio.mp3", format='mp3')
	print("Audio translated and stored in location " + path )
	tkinter.messagebox.showinfo("Audio Development Success","Audio successfully developed from the text")
	root.destroy()

def translateText():
	updateDisplayLabel("Translation Initiated",1.5)
	translator = Translator()
	languages = googletrans.LANGUAGES
	translatedTextFile = open("translatedText.txt","+w")
	updateDisplayLabel("Reading Recognized Text from file",1.5)
	print("Reading Recognized Text from file....")
	recognized = open("recognized.txt","r")
	data = recognized.readlines()
	i = 1
	for line in data:
		detect = translator.detect(line)
		sourceLanguage = detect.lang
		sourceLanguage = languages.__getitem__(sourceLanguage)
		updateDisplayLabel("Source Language is "+sourceLanguage,1)
		updateDisplayLabel("Tranlating line " + str(i) +"---"+ time.ctime(),1.5)
		print("Tranlating line " + str(i) +"---"+ time.ctime())
		translatedData = translator.translate(line.strip(), src=detect.lang,dest='ta')
		data = translatedData.text
		translatedTextFile.write(data+"\n")
		updateDisplayLabel("Line translated ---" + time.ctime(),1.5)
		print("Line translated ---" + time.ctime())
		i = i + 1
	updateDisplayLabel("Translation Completed",1.5)
	print("Done Translating....")
	updateDisplayLabel("Translated text file is stored at location\n /home/siva/Translator/translatedText.txt",1.5)
	tkinter.messagebox.showinfo("Translation Success","Text translated successfully")
	updateDisplayLabel("Initiating Audio Conversion",1.5)
	print("Translated text file is stored at location /home/siva/Translator/translatedText.txt ")
	root.destroy()

def silence_based_conversion(displayLabel):	
	root.update()
	path = "/home/siva/Translator/audio.wav"
	print("Souce Location : " + path)
	
	clearFiles()
	audio = AudioSegment.from_wav(path)
	recognized = open("recognized.txt","w+")
	unrecognized = open("unrecognized.txt","w+")
	retry = open("retry.txt","w+")
	print("Audio fetched and preparing to split....\nSplitting Chunks.....")
	print("This may take a while.....")
	displayLabel.set("Splitting the Audio into chunks \n This may take a while...")
	root.update()
	chunks = split_on_silence(audio, min_silence_len = 750, silence_thresh = -30)
	root.update()
	print("Audio chunks successfully splitted .....")
	
	try:
		os.mkdir('audio_chunks')
	except(FileExistsError):
		pass
	
	print("audio_chunks directory created and home directory changed to audio_chunks .....")
	os.chdir('audio_chunks')

	i = 0
	for chunk in chunks:
		displayLabel.set("Processing chunk " + str(i)+"---"+ time.ctime())
		root.update()
		chunk_silent = AudioSegment.silent(duration = 100)	
		audio_chunk = chunk_silent + chunk + chunk_silent
		#audio_chunk = audio_chunk._spawn(audio_chunk.raw_data, overrides={"frame_rate": int(audio_chunk.frame_rate * 0.90)})
		print("Saving chunk{0}.wav".format(i))
		audio_chunk.export("./chunk{0}.wav".format(i), bitrate = '192k', format = "wav")
		filename = 'chunk' + str(i)+ '.wav'
		print("Processing chunk " + str(i))
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
	updateDisplayLabel("Total number of chunks processed : " + str(i),5)
	updateDisplayLabel("Recognized text from audio file is stored at location\n /home/siva/Translator/recognized.txt",5)
	updateDisplayLabel("Unrecognized audio chunks is stored at location\n /home/siva/Translator/unrecognized.txt",5)
	updateDisplayLabel("Retry required audio chunks is stored at location\n /home/siva/Translator/retry.txt",5)
	tkinter.messagebox.showinfo("Audio Conversion Success", "Successfully converted Audio to Text")
	print("Total number of chunks processed : " + str(i) )
	os.chdir('..')
	print("Returned to home directory.....")
	print("Recognized text from audio file is stored at location /home/siva/Translator/recognized.txt")
	print("Unrecognized audio chunks is stored at location /home/siva/Translator/unrecognized.txt")
	print("Retry required audio chunks is stored at location /home/siva/Translator/retry.txt")
	print("Converting text to another language....")
	updateDisplayLabel("Initiating Language Translation....",5)
	root.destroy()


clearFiles()

root = tkinter.Tk()
root.title("Audio Handling")
root.geometry("800x240")
displayLabel = tkinter.StringVar()
label = tkinter.Label(root, textvariable = displayLabel)
label.pack()
button = tkinter.Button(root,text  = "Proceed", command = lambda: silence_based_conversion(displayLabel))
button.pack()
cancel = tkinter.Button(root,text = "Cancel", command = lambda: root.destroy())
cancel.pack()
root.update()
root.mainloop()

root = tkinter.Tk()
root.title("Text Translation")
root.geometry("800x240")
displayLabel = tkinter.StringVar()
label = tkinter.Label(root, textvariable = displayLabel)
label.pack()
button = tkinter.Button(root,text = "Translate Text", command = lambda: translateText())
button.pack()
cancel = tkinter.Button(root,text = "Cancel", command = lambda: root.destroy())
cancel.pack()
root.update()
root.mainloop()

root = tkinter.Tk()
root.title("Audio Translation")
root.geometry("800x240")
displayLabel = tkinter.StringVar()
label = tkinter.Label(root, textvariable = displayLabel)
label.pack()
button = tkinter.Button(root,text = "Develop Audio", command = lambda: textToOtherLanguage())
button.pack()
cancel = tkinter.Button(root,text = "Cancel", command = lambda: root.destroy())
cancel.pack()
root.update()
root.mainloop()