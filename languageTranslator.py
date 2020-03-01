from googletrans import Translator

def translateText():

    #translator = Translator()

    print("Reading Recognized Text from file....")
    recognized = open("recognized.txt","r")
    data = recognized.readlines()
    for line in data: 
        print("........................................................\n")
        print(line.strip())
    #dt = translator.translate(text1, src='ta',dest='en')
    #print (dt.text)

translateText()