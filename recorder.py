<<<<<<< HEAD
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from playsound import playsound

'''
    records audio and writes it on the same Dir
'''


def record(file_name='output.wav'):
    fs = 44100  # Sample rate
    seconds = 3  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    data = myrecording
    try:
        y = (np.iinfo(np.int32).max * (data / np.abs(data).max())).astype(np.int32)
    except:
        print('error occured in recorder.py')
    write(file_name, fs, y)  # Save as WAV file
    # playsound(file_name) # for debuggig
||||||| merged common ancestors
=======
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from playsound import playsound

'''
    records audio and writes it on the same Dir
'''


def record(file_name='output.wav'):
    fs = 44100  # Sample rate
    seconds = 3  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    data = myrecording
    try:
        y = (np.iinfo(np.int32).max * (data / np.abs(data).max())).astype(np.int32)
    except:
        print('error occured in recorder.py')
    write(file_name, fs, y)  # Save as WAV file
    #file_name.close() # newly
    # playsound(file_name) # for debuggig
>>>>>>> 8a9b78e950abf9841e5ef7fc3533fffa4398f5ca
