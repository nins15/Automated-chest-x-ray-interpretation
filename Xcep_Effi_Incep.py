# -*- coding: utf-8 -*-
"""Untitled5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OeMGkEdDmGTrDba2V9KGIhTCEiJzcbCn
"""

import cv2
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
from tqdm import tqdm, tqdm_notebook
from keras.models import Model
from keras.layers import Dropout, Flatten, Dense
from tensorflow.keras import optimizers
from keras.applications import Xception
import tensorflow as tf
from sklearn.model_selection import train_test_split
from keras.applications import InceptionResNetV2
from keras.applications.densenet import DenseNet121
import numpy as np
import keras
from keras.models import Sequential, Model
from keras.layers import Dense, Flatten, Activation, Dropout, GlobalAveragePooling2D
from keras_preprocessing.image import ImageDataGenerator
from keras import  applications
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, TensorBoard, EarlyStopping
from keras import backend as K 
from sklearn.datasets.samples_generator import make_blobs
from sklearn.metrics import accuracy_score
from keras.models import load_model
from keras.utils import to_categorical
from keras.utils import plot_model
from keras.layers import Input
from keras.layers.merge import concatenate
from numpy import argmax
from keras_efficientnets import EfficientNetB0
from keras.models import load_model

def Xceptionnet(image_size = 224, load_previous_weights = True, freeze_cnn = False):
    data_path='/content/Chexperttraining1'#training data 
    data=pd.read_csv('/content/Processed_train_LSR-Zeros.csv')#training dataframe
    base_model =Xception(include_top= False, input_shape=(image_size,image_size,3), weights='imagenet')
    # add a global spatial average pooling layer
    x = base_model.output
    
    #test=pd.read_csv('/content/Processed_test.csv')#testing data
    x = GlobalAveragePooling2D(input_shape=(1024,1,1))(x)
    # Add a flattern layer 
    x = Dense(2048, activation='relu')(x)
    x = keras.layers.normalization.BatchNormalization()(x)
    x = Dropout(0.2)(x)
    # Add a fully-connected layer
    x = Dense(512, activation='relu')(x)
    x = keras.layers.normalization.BatchNormalization()(x)
    x = Dropout(0.2)(x)
    # and a logistic layer --  we have 5 classes
    predictions = Dense(5, activation='sigmoid')(x)
   
    # this is the model we will train
    model = Model(inputs=base_model.input, outputs=predictions)
    features=['Cardiomegaly', 'Edema', 'Consolidation', 'Pleural Effusion','Atelectasis']
    
    #test=pd.read_csv('/content/Processed_test.csv')#testing dataframe
    #data, valid = train_test_split(data, test_size=0.2)
    data=data
    #valid=valid
    # Recover previously trained weights
    if load_previous_weights:
        try:
            model.load_weights('/content/Xception.hdf5')
            print('Weights successfuly loaded')
        except:
            print('Weights not loaded')

    # first: train only the top layers (which were randomly initialized)
    # i.e. freeze all convolutional InceptionV3 layers
    if freeze_cnn:
        for layer in base_model.layers:
            layer.trainable = False
            
    datagen=ImageDataGenerator(rescale=1./255,samplewise_center=True, samplewise_std_normalization=True, 
                                 rotation_range=5,
                                 width_shift_range=0.2,
                                 height_shift_range=0.2,
                                 horizontal_flip=True,
                                 validation_split = 0.25)
    test_datagen=ImageDataGenerator(rescale=1./255)
    image_size=224

  
    valid_generator=datagen.flow_from_dataframe(dataframe=data, directory=data_path, 
                                                    x_col='Path', y_col=features, seed = 42, 
                                                    class_mode='raw', target_size=(image_size,image_size), batch_size=32, subset = "validation")
    train_generator=datagen.flow_from_dataframe(dataframe=data, directory=data_path, 
                                                    x_col='Path', y_col=features, seed = 42, 
                                                    class_mode='raw', target_size=(image_size,image_size), batch_size=32, subset = "training")    
    # compile the model (should be done *after* setting layers to non-trainable)
    train_generator=train_generator

    STEP_SIZE_TRAIN=train_generator.n//train_generator.batch_size
    STEP_SIZE_VALID=valid_generator.n//valid_generator.batch_size
    
    lr_schedule = optimizers.schedules.ExponentialDecay(
    initial_learning_rate=1e-3,
    decay_steps=STEP_SIZE_TRAIN,
    decay_rate=0.1)
    optimizer = optimizers.Adam(learning_rate=lr_schedule)
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy',tf.keras.metrics.AUC(multi_label=True)])
    checkpointer = ModelCheckpoint(filepath='Xception_LSRZerobestauc.hdf5', 
                                verbose=1, save_best_only=True,monitor='val_auc',mode='max')
    checkpointer1=ModelCheckpoint(filepath='Xception_LSRZerobestacc.hdf5', 
                                verbose=1, save_best_only=True,monitor='val_accuracy',mode='max')


    print(STEP_SIZE_TRAIN)
    print(STEP_SIZE_VALID)
    epochs=20
    history = model.fit_generator(generator=train_generator,
                        steps_per_epoch=STEP_SIZE_TRAIN,
                        validation_data=valid_generator,
                        validation_steps=STEP_SIZE_VALID,
                        epochs=epochs, callbacks = [checkpointer,checkpointer1],use_multiprocessing=True)    
  
    

Xceptionnet()

def InceptionResNet_V2(image_size = 224, load_previous_weights = True, freeze_cnn = False):
    data_path='CheXpert_dataset'#training data 
    data=pd.read_csv('/content/Processed_train_LSR-Zeros.csv')#training dataframe
    base_model = InceptionResNetV2(include_top= False, input_shape=(image_size,image_size,3), weights='imagenet')
    # add a global spatial average pooling layer
    x = base_model.output
    
    #test=pd.read_csv('/content/Processed_test.csv')#testing data
    x = GlobalAveragePooling2D(input_shape=(1024,1,1))(x)
    # Add a flattern layer 
    x = Dense(2048, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)
    # Add a fully-connected layer
    x = Dense(512, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)
    # and a logistic layer --  we have 5 classes
    predictions = Dense(5, activation='sigmoid')(x)
   
    # this is the model we will train
    model = Model(inputs=base_model.input, outputs=predictions)
    features=['Cardiomegaly', 'Edema', 'Consolidation', 'Pleural Effusion','Atelectasis']
    
    #test=pd.read_csv('/content/Processed_test.csv')#testing dataframe
    data, valid = train_test_split(data, test_size=0.2)
    data=data
    valid=valid
    # Recover previously trained weights
    if load_previous_weights:
        try:
            model.load_weights('../input/chexpert-keras-base/weights.hdf5')
            print('Weights successfuly loaded')
        except:
            print('Weights not loaded')

    # first: train only the top layers (which were randomly initialized)
    # i.e. freeze all convolutional InceptionV3 layers
    if freeze_cnn:
        for layer in base_model.layers:
            layer.trainable = False
            
    datagen=image.ImageDataGenerator(rescale=1./255,samplewise_center=True, samplewise_std_normalization=True, 
                                 rotation_range=5,
                                 width_shift_range=0.2,
                                 height_shift_range=0.2,
                                 horizontal_flip=True,
                                 validation_split = 0.1)
    test_datagen=image.ImageDataGenerator(rescale=1./255)
    image_size=224

  
    valid_generator=datagen.flow_from_dataframe(dataframe=valid, directory=data_path, 
                                                    x_col='Path', y_col=features, seed = 42, 
                                                    class_mode='raw', target_size=(image_size,image_size), batch_size=32, subset = "validation")
    train_generator=datagen.flow_from_dataframe(dataframe=data, directory=data_path, 
                                                    x_col='Path', y_col=features, seed = 42, 
                                                    class_mode='raw', target_size=(image_size,image_size), batch_size=32, subset = "training")    
    # compile the model (should be done *after* setting layers to non-trainable)
    train_generator=train_generator

    STEP_SIZE_TRAIN=train_generator.n//train_generator.batch_size
    STEP_SIZE_VALID=valid_generator.n//valid_generator.batch_size
    lr_schedule = optimizers.schedules.ExponentialDecay(
    initial_learning_rate=1e-3,
    decay_steps=STEP_SIZE_TRAIN,
    decay_rate=0.1)
    optimizer = optimizers.Adam(learning_rate=lr_schedule)
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy',tf.keras.metrics.AUC(multi_label=True)])
    checkpointer = ModelCheckpoint(filepath='InceptionResNetmodelLSRZero_bestauc.hdf5', 
                                verbose=1, save_best_only=True,monitor='val_auc',mode='max')
    checkpointer1=ModelCheckpoint(filepath='InceptionResNetmodelLSRZero_bestacc.hdf5', 
                                verbose=1, save_best_only=True,monitor='val_accuracy',mode='max')


    print(STEP_SIZE_TRAIN)
    print(STEP_SIZE_VALID)
    epochs=20
    history = model.fit_generator(generator=train_generator,
                        steps_per_epoch=STEP_SIZE_TRAIN,
                        validation_data=valid_generator,
                        validation_steps=STEP_SIZE_VALID,
                        epochs=epochs, callbacks = [checkpointer,checkpointer1],use_multiprocessing=True)    
 
    

InceptionResNet_V2()

def Efficientnet(image_size = 224, load_previous_weights = True, freeze_cnn = False):
    data_path='/content/Chexperttraining1'#training data 
    data=pd.read_csv('/content/Processed_train_LSR-Zeros.csv')#training dataframe
    base_model = EfficientNetB0(include_top= False, input_shape=(image_size,image_size,3), weights='imagenet')
    # add a global spatial average pooling layer
    x = base_model.output
    
    #test=pd.read_csv('/content/Processed_test.csv')#testing data
    x = GlobalAveragePooling2D(input_shape=(1024,1,1))(x)
    # Add a flattern layer 
    x = Dense(2048, activation='relu')(x)
    x = keras.layers.normalization.BatchNormalization()(x)
    x = Dropout(0.2)(x)
    # Add a fully-connected layer
    x = Dense(512, activation='relu')(x)
    x = keras.layers.normalization.BatchNormalization()(x)
    x = Dropout(0.2)(x)
    # and a logistic layer --  we have 5 classes
    predictions = Dense(5, activation='sigmoid')(x)
   
    # this is the model we will train
    model = Model(inputs=base_model.input, outputs=predictions)
    features=['Cardiomegaly', 'Edema', 'Consolidation', 'Pleural Effusion','Atelectasis']
    
    #test=pd.read_csv('/content/Processed_test.csv')#testing dataframe
    data, valid = train_test_split(data, test_size=0.2)
    data=data
    valid=valid
    # Recover previously trained weights
    if load_previous_weights:
        try:
            model.load_weights('../input/chexpert-keras-base/weights.hdf5')
            print('Weights successfuly loaded')
        except:
            print('Weights not loaded')

    # first: train only the top layers (which were randomly initialized)
    # i.e. freeze all convolutional InceptionV3 layers
    if freeze_cnn:
        for layer in base_model.layers:
            layer.trainable = False
            
    datagen=ImageDataGenerator(rescale=1./255,samplewise_center=True, samplewise_std_normalization=True, 
                                 rotation_range=5,
                                 width_shift_range=0.2,
                                 height_shift_range=0.2,
                                 horizontal_flip=True,
                                 validation_split = 0.1)
    test_datagen=ImageDataGenerator(rescale=1./255)
    image_size=224

  
    valid_generator=datagen.flow_from_dataframe(dataframe=valid, directory=data_path, 
                                                    x_col='Path', y_col=features, seed = 42, 
                                                    class_mode='raw', target_size=(image_size,image_size), batch_size=32, subset = "validation")
    train_generator=datagen.flow_from_dataframe(dataframe=data, directory=data_path, 
                                                    x_col='Path', y_col=features, seed = 42, 
                                                    class_mode='raw', target_size=(image_size,image_size), batch_size=32, subset = "training")    
    # compile the model (should be done *after* setting layers to non-trainable)
    train_generator=train_generator

    STEP_SIZE_TRAIN=train_generator.n//train_generator.batch_size
    STEP_SIZE_VALID=valid_generator.n//valid_generator.batch_size
    
    lr_schedule = optimizers.schedules.ExponentialDecay(
    initial_learning_rate=1e-3,
    decay_steps=STEP_SIZE_TRAIN,
    decay_rate=0.1)
    optimizer = optimizers.Adam(learning_rate=lr_schedule)
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy',tf.keras.metrics.AUC(multi_label=True)])
    checkpointer = ModelCheckpoint(filepath='EffiecientNetLSRZero_bestauc.hdf5', 
                                verbose=1, save_best_only=True,monitor='val_auc',mode='max')
    checkpointer1=ModelCheckpoint(filepath='EffiecientNetLSRZero_bestacc.hdf5', 
                                verbose=1, save_best_only=True,monitor='val_accuracy',mode='max')


    print(STEP_SIZE_TRAIN)
    print(STEP_SIZE_VALID)
    epochs=20
    history = model.fit_generator(generator=train_generator,
                        steps_per_epoch=STEP_SIZE_TRAIN,
                        validation_data=valid_generator,
                        validation_steps=STEP_SIZE_VALID,
                        epochs=epochs, callbacks = [checkpointer,checkpointer1],use_multiprocessing=True)    
 
    

Efficientnet()