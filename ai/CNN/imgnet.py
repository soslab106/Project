from django.shortcuts import render
from keras.applications.vgg16 import VGG16
# from keras.applications.resnet import ResNet101
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input, decode_predictions
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image
from keras import backend as K

def recogImgnet(img_path, modelName):
    K.clear_session()

    if modelName == 'VGG16':
        model = VGG16(weights='imagenet', include_top=True) 
    elif modelName == 'ResNet50':
        model = ResNet50(weights='imagenet')

    # Input：要辨識的影像
    # D:\106\Project\media\tiger.jpg
    img_path = os.path.join('.'+img_path)
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    # 預測，取得features，維度為 (1,7,7,512)
    features = model.predict(x)
    # 取得前三個最可能的類別及機率
    result = []
    for each in decode_predictions(features, top=5)[0]:
        result.append(each[1:])
    return result