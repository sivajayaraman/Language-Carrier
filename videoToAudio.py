import subprocess
import os

locationPath = input("ENTER YOUR VIDEO FILE PATH ")
locationPath = locationPath[1:-1]
exception = False
print("Location Grasped.....")
print("Seeking Location.....")

isFileExisting = os.path.isfile(locationPath)
print ("Expected File Location : " + locationPath)
if isFileExisting == True:
    print("Reached Location " + locationPath)
    print("Searching your Source file....")
    command = "ffmpeg -i "+ locationPath +" -ab 20k -ac 2 -ar 44100 -vn audio.wav"
    subprocess.call(command, shell=True)
else:
    exception = True
    print("File Not Found!!!")

if exception == False:
    print("Resource file fetched and Audio extracted successfully....")
    print("Extracted Audio is stored at /home/siva/Translator as audio.wav file....")
    print("Executing Audio to Text Conversion.....")
    command = "python3 audioToText.py"
    subprocess.call(command, shell=True)
    print("Successfully completed conversion.....")
else:
    print("Unsuccessful Conversion. Please Try Again!!!")