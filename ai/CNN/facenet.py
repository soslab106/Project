# -*-coding:utf-8 -*-

from cv2 import cv2 as cv
import numpy as np
import dlib
import imutils
import os
from keras.preprocessing import image
def imageFaceDetec(img_path, myfile):
    # 讀取照片圖檔
    img_path = os.path.join('.'+img_path)
    img = cv.imread(img_path)
    img = imutils.resize(img, width=1280)

    # Dlib 的人臉偵測器
    detector = dlib.get_frontal_face_detector()

    # 偵測人臉
    face_rects = detector(img, 0)

    # 取出所有偵測的結果
    for i, d in enumerate(face_rects):
        x1 = d.left()
        y1 = d.top() 
        x2 = d.right()
        y2 = d.bottom()
    # 以方框標示偵測的人臉
        cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 4, cv.LINE_AA)

    cv.imwrite(img_path, img)
    cv.waitKey(0)
    
    img_path = img_path[1:]

    return img_path
    