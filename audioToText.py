import subprocess
import os
import speech_recognition as sr
import languageTranslator as lt
from pydub import AudioSegment
from pydub.silence import split_on_silence

def silence_based_conversion():	

	path = "/home/siva/Translator/audio.wav"
	print("Souce Location : " + path)
	
	audio = AudioSegment.from_wav(path)
	
	recognized = open("recognized.txt","w+")
	unrecognized = open("unrecognized.txt","w+")
	retry = open("retry.txt","w+")
	print("Audio fetched and preparing to split....\nSplitting Chunks.....")
	print("This may take a while.....")
	chunks = split_on_silence(audio, min_silence_len = 750, silence_thresh = -30)
	print("Audio chunks successfully splitted .....")
	
	try:
		os.mkdir('audio_chunks')
	except(FileExistsError):
		pass
	
	print("audio_chunks directory created and home directory changed to audio_chunks .....")
	os.chdir('audio_chunks')

	i = 0
	for chunk in chunks:

		chunk_silent = AudioSegment.silent(duration = 100)	
		audio_chunk = chunk_silent + chunk + chunk_silent
		#audio_chunk = audio_chunk._spawn(audio_chunk.raw_data, overrides={"frame_rate": int(audio_chunk.frame_rate * 0.60)})
		print("Saving chunk{0}.wav".format(i))
		audio_chunk.export("./chunk{0}.wav".format(i), bitrate = '192k', format = "wav")
		filename = 'chunk' + str(i)+ '.wav'
		print("Processing chunk " + str(i))
		file = filename
		r = sr.Recognizer()

		with sr.AudioFile(file) as source:
			r.adjust_for_ambient_noise(source)
			audio_listened = r.listen(source)

		try:
			rec = r.recognize_google(audio_listened)
			recognized.write( rec + ".\n" )
		
		except sr.UnknownValueError:
			print("Could not understand audio")
			print("Storing audio chunk as unconvertible chunk")
			unrecognized.write(filename + "\n")

		except sr.RequestError:
			print("Connectivity Failure!")
			print("Loading audio chunk in failed chunks for retrying")
			retry.write(filename + "\n")

		i += 1
	
	print("Total number of chunks processed : " + str(i) )
	os.chdir('..')
	print("Returned to home directory.....")
	print("Recogized text from audio file is stored at location /home/siva/Translator/recognized.txt")
	print("Unrecogized audio chunks is stored at location /home/siva/Translator/unrecognized.txt")
	print("Retry required audio chunks is stored at location /home/siva/Translator/retry.txt")
	print("Converting text to another language....")

silence_based_conversion()
lt.translateText()
