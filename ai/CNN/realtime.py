# -*-coding:utf-8 -*-

from cv2 import cv2 as cv
import numpy as np
import dlib
import imutils
import os
from keras.preprocessing import image
def realtimeDetec():
    #開啟影片檔案
    cap = cv.VideoCapture(0)

    #Dlib 的人臉偵測器
    detector = dlib.get_frontal_face_detector()

    #以迴圈從影片檔案讀取影格，並顯示出來
    while(cap.isOpened()):
        ret, frame = cap.read()

        #偵測人臉
        face_rects, scores, idx = detector.run(frame, 0)

        #取出偵測結果
        for i, d in enumerate(face_rects):
            x1 = d.left()
            y1 = d.top()
            x2 = d.right()
            y2 = d.bottom()
            text = "%2.2f(%d)" % (scores[i], idx[i])

            #以方框標示人臉
            cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4, cv.LINE_AA)

            # 標示分數
            cv.putText(frame, text, (x1, y1), cv.FONT_HERSHEY_DUPLEX,
            0.7, (255, 255, 255), 1, cv.LINE_AA)

            #結果
            cv.imshow("Face Detection", frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()
    cv.destroyAllWindows()
