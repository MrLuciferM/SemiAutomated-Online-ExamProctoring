import speech_recognition as sr
import pyaudio
import wave
import time
import threading
import os

def save_audio(stream, filename):
    """
    Saving the recorded audio sample in record.
    """
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt32  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = 10  # Number of seconds to record at once
    
    
    path = "./audio_logs/audios/"
    filename = path + filename
    
    frames = []  # Initialize array to store frames
    
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)
    
    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    # Stop and close the stream
    stream.stop_stream()
    stream.close()

def convert(i):
    '''
    Recognizing text from the audio 
    and then adding it to recognized_words.txt file 
    and and deleting the audio file.
    '''
    path = "./audio_logs/audios/"
    if i >= 0:
        sound = path+ 'record' + str(i) +'.wav'
        r = sr.Recognizer()
        
        with sr.AudioFile(sound) as source:
            r.adjust_for_ambient_noise(source)
            print("Converting Audio To Text and saving to file..... ") 
            audio = r.listen(source)
        try:
            value = r.recognize_google(audio) ##### API call to google for speech recognition
            os.remove(sound)
            if str is bytes: 
                result = u"{}".format(value).encode("utf-8")
            else: 
                result = "{}".format(value)

            with open("./audio_logs/Intermediate/recognized_words.txt","a") as f:
                f.write(result)
                f.write(" ")
                f.close()
                
        except sr.UnknownValueError:
            print("")
        except sr.RequestError as e:
            print("{0}".format(e))
        except KeyboardInterrupt:
            pass

def read_audio(i):
    """
    Creates an audio stream to be readed from the microphone.
    """
    stream = p.open(format=sample_format,channels=channels,rate=fs,
                frames_per_buffer=chunk, input=True)
    print("Listening...")
    filename = 'record'+str(i)+'.wav'
    save_audio(stream, filename)


p = pyaudio.PyAudio()  # Create an interface to PortAudio

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt32  # 16 bits per sample
channels = 2
fs = 44100

for i in range(30//10): # Number of total seconds to record/ Number of seconds per recording
    t1 = threading.Thread(target=read_audio, args=[i]) 
    x = i-1
    t2 = threading.Thread(target=convert, args=[x]) # send one earlier than being recorded
    t1.start() 
    t2.start() 
    t1.join() 
    t2.join() 
    if i==2:
        flag = True
if flag:
    convert(i)
    p.terminate()




# NATURAL LANGUAGE PROCESSING
import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

file = open("./audio_logs/Intermediate/recognized_words.txt") ## Student speech file
data = file.read()
file.close()
stop_words = set(stopwords.words('english'))   
word_tokens = word_tokenize(data) ######### tokenizing sentence
# filtered_sentence = [w for w in word_tokens if not w in stop_words]  
filtered_sentence = [] 

for w in word_tokens:   ####### Removing stop words
    if w not in stop_words: 
        filtered_sentence.append(w) 

####### creating a final file
f=open('./audio_logs/Outputs/final.txt','w')
for element in filtered_sentence:
    f.write(element+' ')
f.close()
    
##### checking whether proctor needs to be alerted or not
file = open("./audio_logs/Inputs/paper.txt",encoding='utf8') ## Question file
data = file.read()
file.close()
stop_words = set(stopwords.words('english'))   
word_tokens = word_tokenize(data) ######### tokenizing sentence
# filtered_questions = [w for w in word_tokens if not w in stop_words]  
filtered_questions = [] 

for w in word_tokens:   ####### Removing stop words
    if w not in stop_words: 
        filtered_questions.append(w) 
        
def common_member(a, b):     
    a_set = set(a) 
    b_set = set(b) 
    # check length  
    if len(a_set.intersection(b_set)) > 0: 
        return(a_set.intersection(b_set))   
    else: 
        return([]) 

comm = common_member(filtered_questions, filtered_sentence)
print('Number of common elements:', len(comm))
print(comm)