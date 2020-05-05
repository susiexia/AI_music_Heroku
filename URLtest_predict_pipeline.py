
import numpy as np
#import pandas as pd 

import librosa
import librosa.display
from sklearn.preprocessing import normalize
#from keras.models import load_model

# buff depedence 
#import os
import io
from cv2 import cv2 
import matplotlib.pyplot as plt

# URL 
import cloudinary
import soundfile as sf
from six.moves.urllib.request import urlopen

import tensorflow as tf

# unuse dependencies

#import tensorflow_core
#import keras
#import pickle
#from keras.models import Model

'''This python script includes 4 functions, predict_pitch() and predict_instrument()
 And 2 functions for visualize spectrogram'''

# create a function for pitch pred
def predict_pitch(url):
    '''This function includes ETL process, loading trained model, 
        and using model to get prediction'''
    
    # -------------------------------ETL preprocessing part------------------------------------
    '''TESTING: USE LOCAL FILE PATH AS input_audioFile '''

    # use librosa convert audio file to spectrogram
    #audio, sample_rate = librosa.load(input_audioFile) # remove offset=length/6, duration=1, res_type='kaiser_fast'

    #URL 
    audio, samplerate = sf.read(io.BytesIO(urlopen(url).read()))
    #
    #audio, samplerate = sf.read(io.BytesIO(urlopen(url).read()), start=0, stop=44100)
    #data = urlopen(url)
    #audio = audio.T
    data_22k = librosa.resample(audio, samplerate, 21395)
    #print(data_22k)
    fig = plt.figure(figsize=[1.5,10])
    # Convert audio array to 'Constant-Q transform'. 86 bins are created to take pitches form C1 to C#8
    
    conQfit = librosa.cqt(data_22k,hop_length=4096,n_bins=86)
    librosa.display.specshow(conQfit)
               
    # Capture image and convert into 2D array
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=(56/5))
    buf.seek(0)
    img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    img = cv2.imdecode(img_arr, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
    # normalize
    mfccs_norm = normalize(img, axis=0, norm='max')
        
    # close the plotted image so it wont show while in the loop
    plt.close()
    fig.clf()
    plt.close(fig)
    plt.close('all')

    # convert mfccs_norm into 4d array

    channels = 1 # number of audio channels
    row = 1 
    spectrogram_shape1 = (row,) + mfccs_norm.shape + (channels,)

    #x_reshape = np.array(i.reshape( (spectrogram_shape1) ) for i in mfccs_norm) 
    pitch_ETL_4d_output = mfccs_norm.reshape( (spectrogram_shape1) ) 

    #print(pitch_ETL_4d_output.shape)
    
    # --------------------------------Load trained pitch model--------------------------
    # load trained pitch model
    #with open('PKL_trained_pitch_model.pkl', 'rb') as pitch_f:        
     #   pitch_model = pickle.load(pitch_f)
    pitch_model = tf.keras.models.load_model('pitch_model.h5')
    

    # --------------------------------PREDICTION --------------------------
    # pitch_model (from app.py) to predict
    pitch_result = pitch_model.predict(pitch_ETL_4d_output)
    
    # reverse to_categorical() function, get correlated pitch_name
    pitch_scalar =  np.argmax(pitch_result, axis=None, out=None)
    
    # extract pitch names from csv to be a list
    #pitch_Name_df = pd.read_csv('pitchName.csv')
    #pitch_name_list = pitch_Name_df['0'].tolist()

    pitch_name_list = ['A#1', 'A#2', 'A#3', 'A#4', 'A#5', 'A#6', 'A#7',
    'A1','A2', 'A3', 'A4', 'A5', 'A6', 'A7',
    'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 
    'C#2', 'C#3', 'C#4', 'C#5', 'C#6', 'C#7' ,'C#8',
    'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 
    'D#2', 'D#3', 'D#4', 'D#5', 'D#6', 'D#7',
    'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 
    'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7',  
     'F#1', 'F#2', 'F#3', 'F#4', 'F#5','F#6', 'F#7',
    'F1', 'F2', 'F3', 'F4','F5','F6', 'F7',
    'G#1', 'G#2', 'G#3','G#4', 'G#5', 'G#6', 'G#7',
     'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7']
    
    
    # reverse labelEncoder() function to get prediction label
    pitch_pred = pitch_name_list[pitch_scalar]
    
    return pitch_pred 



def predict_instrument(url):
    '''This function includes ETL process, loading trained model, 
        and using model to get prediction'''
    
    # -------------------------------ETL preprocessing part------------------------------------
    '''TESTING: USE LOCAL FILE PATH AS input_audioFile '''

    # use librosa convert audio file to spectrogram
    #audio, sample_rate = librosa.load(input_audioFile) # remove offset=length/6, duration=1, res_type='kaiser_fast'

    #URL 
    audio, samplerate = sf.read(io.BytesIO(urlopen(url).read()))

    #audio, samplerate = sf.read(io.BytesIO(urlopen(url).read()), start=0, stop=44100)
    #data = urlopen(url)
    #audio = audio.T
    data_22k = librosa.resample(audio, samplerate, 21395)

    fig = plt.figure(figsize=[6,4])
    # Convert audio array to 'Constant-Q transform'. 86 bins are created to take pitches form C1 to C#8
    mfccs = librosa.feature.melspectrogram(data_22k, hop_length = 1024)  
    mel_spec = librosa.power_to_db(mfccs, ref=np.max,)
    librosa.display.specshow(mel_spec)

    # Capture image and convert into 2D array
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=(43/3))
    buf.seek(0)
    img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    img = cv2.imdecode(img_arr, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # normalize
    inst_mfccs_norm = normalize(img, axis=0, norm='max')
    
    # close the plotted image so it wont show while in the loop
    plt.close()
    fig.clf()
    plt.close(fig)
    plt.close('all')
        
    # convert mfccs_norm into 4d array

    channels = 1 # number of audio channels
    row = 1 
    spectrogram_shape1 = (row,) + inst_mfccs_norm.shape + (channels,)

    #x_reshape = np.array(i.reshape( (spectrogram_shape1) ) for i in mfccs_norm) 
    inst_ETL_4d_output = inst_mfccs_norm.reshape( (spectrogram_shape1) ) 

    #print(inst_ETL_4d_output.shape)
    
    # --------------------------------Load trained inst model--------------------------
    # load trained inst model
    #with open('CV_PKL_trained_instruments_model.pkl', 'rb') as inst_f:        
    #    inst_model = pickle.load(inst_f)
    #from keras.models import load_model
    inst_model = tf.keras.models.load_model('CV_trained_intruments_model.h5')

    # --------------------------------PREDICTION --------------------------
    # inst_model (from app.py) to predict
    inst_result = inst_model.predict(inst_ETL_4d_output)
    
    # reverse to_categorical() function, get correlated inst_name
    inst_scalar =  np.argmax(inst_result, axis=None, out=None)
    
    # extract inst names from csv to be a list
    #inst_Name_df = pd.read_csv('CV_inst_Name.csv')
    #inst_name_list = inst_Name_df['0'].tolist()
    inst_name_list = ['Accordion', 'Alto Saxophone', 'Bass Tuba', 'Bassoon', 'Cello',
       'Clarinet in Bb', 'Contrabass', 'Flute', 'French Horn', 'Oboe',
       'Trombone', 'Trumpet in C', 'Viola', 'Violin']
    # reverse labelEncoder() function to get prediction label
    inst_pred = inst_name_list[inst_scalar]
    
    return inst_pred  

# create a functions to get pitch and instrument spectrogram
def get_spect_pitch(url):
    '''This function gets the spectrogram for pitch'''
    
    #direclt use URL and convert to audio file
    audio, samplerate = sf.read(io.BytesIO(urlopen(url).read()))
    
    audio = audio.T
    data_22k = librosa.resample(audio, samplerate, 21395) # local files: sampleRate = 22050
    fig = plt.figure(figsize=[1.5,10])

    # Convert audio array to 'Constant-Q transform'. 86 bins are created to take pitches form E1 to C#8
    conQfit = librosa.cqt(data_22k,hop_length=4096,n_bins=86)
    librosa.display.specshow(conQfit)
               
    # Capture image and convert into 2D array
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=(56))
    buf.seek(0)
    data = buf.read()
    buf.close()
    
    return data

def get_spect_inst(url):
    '''This function get the spectrogram for instrument'''

    #URL 
    audio, samplerate = sf.read(io.BytesIO(urlopen(url).read()))

    audio = audio.T
    data_22k = librosa.resample(audio, samplerate, 21395)

    fig = plt.figure(figsize=[6,4])

    # Convert audio array to 'Constant-Q transform'. 86 bins are created to take pitches form E1 to C#8
    mfccs = librosa.feature.melspectrogram(data_22k, hop_length = 1024)  
    mel_spec = librosa.power_to_db(mfccs, ref=np.max,)
    librosa.display.specshow(mel_spec)

    # Capture image and convert into 2D array
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=(90))
    buf.seek(0)
    data = buf.read()
    buf.close()
    
    
    return data 