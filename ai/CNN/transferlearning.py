import tensorflow as tf
from keras.models import load_model
import keras
import os
from PIL import Image
from keras import backend as K
from sklearn.preprocessing import OneHotEncoder
import numpy as np

import tensorflow_datasets as tfds
from time import time
import json
from ai.gpu_solve import *
from django.contrib.auth.models import User
from ai.models import CustomFilePathModel
gpu_solve()

#input
# imageList
# label
# modelName0
#params

IMG_SIZE = 160
BATCH_SIZE = 2 #32
SHUFFLE_BUFFER_SIZE = 1000
base_learning_rate = 0.0001
# initial_epochs = 10
fine_tune_epochs = 10
total_epochs =  fine_tune_epochs
fine_tune_at = 12
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def image_formatter(imageList, label):
  imgs = []
  illegal_imgs=[]
  for i, image in enumerate(imageList):
    image = Image.open(image)
    image = np.array(image, dtype=np.float32)
    if image.shape[-1]!=3:
      illegal_imgs.append([i, image, image.shape])
    else:
      image = (image/127.5) - 1
      image = np.resize(image, (IMG_SIZE, IMG_SIZE, 3))
      imgs.append(image)
  return imgs, label, illegal_imgs


def processer(trainingDataList):
  illegal_imgs = []
  labelList = []
  imageList = []
  for label, imgs in trainingDataList.items() :
    imgs, label, illegal_img = image_formatter(imgs, label)
    illegal_imgs += illegal_imgs
    for i in imgs:
      labelList.append(str(label))
      imageList.append(i)

  if illegal_imgs:
    print(f'錯誤格式之圖片： {illegal_imgs}')
  label_num = len(set(labelList))
  
  labelList = np.asarray(labelList).reshape((-1,1))
  enc = OneHotEncoder(handle_unknown='ignore')
  labelList_ = enc.fit_transform(labelList).toarray()
  labelList_l = labelList_.tolist()
  label_l = enc.inverse_transform(labelList_).tolist()

  image_label = {}

  for i, label in enumerate(labelList_l):
    for j, each in enumerate(label):
      if each == 1.0:
        image_label[j] = label_l[i][0]


  return imageList, labelList_, label_num, image_label

def custom_training(data, user):
  sequential = []

  imageList, labelList, label_num, image_label = processer(data['trainingData'])

  #validation_set

  #print('imageList'+len(imageList[0]))
  #print('labellist'+len(labelList))
  #print(image_label)

  IMG_SHAPE = (IMG_SIZE, IMG_SIZE, 3)
  base_model = tf.keras.applications.VGG16(input_shape=IMG_SHAPE,
                include_top=False,
                weights='imagenet')
  # base_model.summary()
  base_model.trainable = True
  for layer in base_model.layers[:12]:
    layer.trainable = False
    sequential.append(layer)

  for layer in base_model.layers[12:]:
    layer.trainable = True
    sequential.append(layer)
  
  #Add a classification head
  global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
  prediction_layer = tf.keras.layers.Dense(label_num)
  sequential.append(global_average_layer)
  sequential.append(prediction_layer)

  model = tf.keras.Sequential(sequential)
  

  model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=data['learningRate']),
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=[tf.keras.metrics.BinaryAccuracy(threshold=0.0, name='accuracy')])
  
  # model.summary()
  imageList=np.array(imageList)
  print(imageList)
  imageList = tf.concat(imageList, axis=0)
  print(imageList)

  start_t = time()
  model.fit(x=imageList, y=labelList, epochs=data['epoch'], steps_per_epoch=2)

  end_t = time()
  print("training time:", end_t-start_t, "seconds.")
  model.trainable = False
  user_folder_path = f'ai/CNN/tf_model/user_{user.id}'
  if not os.path.exists(user_folder_path):
    #如果不存在，則建立新目錄
    os.makedirs(user_folder_path)
    print('-----建立成功-----')
  else:
    #如果目錄已存在，則不建立，提示目錄已存在
    print(user_folder_path+'目錄已存在')

  pjName = data['pjName']
  model_path = 'ai/CNN/tf_model/user_{0}/{1}'.format(user.id, pjName)
  model.save(model_path,save_format="h5")
  cfpm = CustomFilePathModel()
  cfpm.modelname = pjName
  cfpm.file_path = model_path
  cfpm.user = user
  cfpm.save()
  print(model_path)
  del model

  # print(image_label)
  model_txt_path = 'ai/CNN/tf_model/user_{0}/{1}.txt'.format(user.id, pjName)
  with open(model_txt_path, 'w') as outfile:
    json.dump(image_label, outfile) 
  status = True
  return status


def load_custom_model(data, user):
  pjName = data['pjName']
  model_path = 'ai/CNN/tf_model/user_{0}/{1}'.format(user.id, pjName)
  model_txt_path = 'ai/CNN/tf_model/user_{0}/{1}.txt'.format(user.id, pjName)
  with open(model_txt_path) as json_file:
    labelName = json.load(json_file)

  image = Image.open(data['image'])
  image = np.array(image, dtype=np.float32)
  if image.shape[-1]!=3:
    print(image.shape)
  else:
    image = (image/127.5) - 1
    image = np.resize(image, (1, IMG_SIZE, IMG_SIZE, 3))
  model = load_model(model_path)

  image = tf.concat(np.array(image), axis=0)

  # model.summary()
  result = model.predict(image, steps=1).tolist()[0]
  result_index = result.index(max(result))

  return labelName[str(result_index)]