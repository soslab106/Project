# coding=UTF-8
from PIL import Image, ImageDraw
from IPython.display import display
import face_recognition
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from IPython.display import display
import os

# This is an example of running face recognition on a single image
# and drawing a box around each person that was identified.
def FaceRecognition(learnImgpath, nameList, recogImgpath):
    known_face_encodings = []
    known_face_names = nameList

    for i in learnImgpath:
        i = os.path.join('.'+i)
        image = face_recognition.load_image_file(i)
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding)

    print('Learned encoding for', len(known_face_encodings), 'images.')

    # Load an image with an unknown face
    recogImgpath = os.path.join('.'+recogImgpath)
    unknown_image = face_recognition.load_image_file(recogImgpath)

    # Find all the faces and face encodings in the unknown image
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    # Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
    # See http://pillow.readthedocs.io/ for more about PIL/Pillow
    pil_image = Image.fromarray(unknown_image)
    # Create a Pillow ImageDraw Draw instance to draw with
    draw = ImageDraw.Draw(pil_image)

    # Loop through each face found in the unknown image
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

        # Draw a label with a name below the face
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))


    # Remove the drawing library from memory as per the Pillow docs
    del draw

    # Return the resulting image
    pil_image.save(recogImgpath)
    return recogImgpath

def faceTraining(learnImgpath, nameList, pjName):
    known_face_encodings = []

    for i in learnImgpath:
        i = os.path.join('.'+i)
        image = face_recognition.load_image_file(i)
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding)
    
    print('Learned encoding for', len(known_face_encodings), 'images.')
    print(known_face_encodings)
    np.savetxt('ai/CNN/face_model/{0}.csv'.format(pjName), known_face_encodings, delimiter=',')
    with open('ai/CNN/face_model/{0}.txt'.format(pjName), 'w') as filehandle:
        filehandle.writelines("%s\n" % name for name in nameList)

def join_faceTraining(learnImgpath, nameList, pjName):
    df = pd.read_csv('ai/CNN/face_model/{0}.csv'.format(pjName), sep=',',header=None)
    df_list = df.values.tolist()
    pre_face_encodings = []
    for i in df_list:
        pre_face_encodings.append(np.array(i))
    known_face_names = nameList
    print (pre_face_encodings)
    for i in learnImgpath:
        i = os.path.join('.'+i)
        image = face_recognition.load_image_file(i)
        face_encoding = face_recognition.face_encodings(image)[0]
        pre_face_encodings.append(face_encoding)

    print('Learned encoding for', len(pre_face_encodings), 'images.')
    np.savetxt('ai/CNN/face_model/{0}.csv'.format(pjName), pre_face_encodings, delimiter=',')
    # define empty list
    places = []

    # open file and read the content in a list
    with open('ai/CNN/face_model/{0}.txt'.format(pjName), 'r') as filehandle:
        filecontents = filehandle.readlines()

        for line in filecontents:
            # remove linebreak which is the last character of the string
            current_place = line[:-1]

            # add item to the list
            places.append(current_place)
    nameList = places + known_face_names
    with open('ai/CNN/face_model/{0}.txt'.format(pjName), 'w') as filehandle:
        filehandle.writelines("%s\n" % name for name in nameList)

def join_faceRecognition(pjName, recogImgpath):

    df = pd.read_csv('ai/CNN/face_model/{0}.csv'.format(pjName), sep=',',header=None)
    df_list = df.values.tolist()
    pre_face_encodings = []
    for i in df_list:
        pre_face_encodings.append(np.array(i))

    known_face_encodings = pre_face_encodings
    # define empty list
    places = []

    # open file and read the content in a list
    with open('ai/CNN/face_model/{0}.txt'.format(pjName), 'r') as filehandle:
        filecontents = filehandle.readlines()

        for line in filecontents:
            # remove linebreak which is the last character of the string
            current_place = line[:-1]

            # add item to the list
            places.append(current_place)
    known_face_names = places

    # Load an image with an unknown face
    recogImgpath = os.path.join('.'+recogImgpath)
    unknown_image = face_recognition.load_image_file(recogImgpath)

    # Find all the faces and face encodings in the unknown image
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    # Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
    # See http://pillow.readthedocs.io/ for more about PIL/Pillow
    pil_image = Image.fromarray(unknown_image)
    # Create a Pillow ImageDraw Draw instance to draw with
    draw = ImageDraw.Draw(pil_image)

    # Loop through each face found in the unknown image
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

        # Draw a label with a name below the face
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))


    # Remove the drawing library from memory as per the Pillow docs
    del draw

    # Return the resulting image
    pil_image.save(recogImgpath)
    return recogImgpath