import tensorflow as tf
import keras
import os
from PIL import Image
from keras import backend as K

# import tensorflow_datasets as tfds

x = [os.path.join('~\songs\song1.jpg'),os.path.join('~\songs\song2.jpg'),os.path.join('~\songs\song3.jpg'),
    os.path.join('~\songs\song4.jpg'),os.path.join('~\songs\song5.jpg'),os.path.join('~\songs\song6.jpg')
    ,os.path.join('~\songs\song7.jpg'),os.path.join('~\songs\song8.jpg'),os.path.join('~\songs\song9.jpg')
    ,os.path.join('~\songs\song10.jpg'),os.path.join('~\songs\song11.jpg'),os.path.join('~\songs\song12.jpg')
    ,os.path.join('~\songs\song13.jpg'),os.path.join('~\songs\song14.jpg'),os.path.join('~\songs\song15.jpg')]
y = ['song','song','song','song','song']


IMG_SIZE = 160 # All images will be resized to 160x160

def format_example(image, label):
  image = tf.cast(image, tf.float32)
  image = (image/127.5) - 1
  image = tf.image.resize(image, (IMG_SIZE, IMG_SIZE))
  return image, label

BATCH_SIZE = 32
SHUFFLE_BUFFER_SIZE = 1000

################################################################
# Deal with training dataset

train = raw_train.map(format_example)
## not sure if we can use this
for image_batch, label_batch in train_batches.take(1):
   pass

print(image_batch.shape)

IMG_SHAPE = (IMG_SIZE, IMG_SIZE, 3)

################################################################
# Create the base model from the pre-trained model MobileNet V2
base_model = tf.keras.applications.VGG16(input_shape=IMG_SHAPE,
                  include_top=False,
                  weights='imagenet')

feature_batch = base_model(image_batch)
print(feature_batch.shape)

base_model.trainable = False

################################################################
# Model Summary
base_model.summary()

################################################################
# Connection layer
first_layer = tf.keras.layers.Conv2D(64,(3,3), input_shape = feature_batch.shape, activation='relu', padding='same')
inputs = first_layer(feature_batch)
input_shape = inputs.shape
sequential = [base_model, first_layer]

################################################################
# Comes Variables
for i in range(5):
  new_layer = tf.keras.layers.Conv2D(64,(3,3), input_shape = input_shape, activation='relu', padding='same') #pow(2, i+1)
  inputs = new_layer(inputs)
  sequential.append(new_layer)
  input_shape = inputs.shape

flatten_layer = tf.keras.layers.Flatten()
inputs = flatten_layer(inputs)
sequential.append(flatten_layer)

################################################################
# Prediction
prediction_layer = tf.keras.layers.Dense(1)
prediction_batch = prediction_layer(inputs)
sequential.append(prediction_layer)

model = tf.keras.Sequential(sequential)

base_learning_rate = 0.0001
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=base_learning_rate),
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=[tf.keras.metrics.BinaryAccuracy(threshold=0.0, name='accuracy')])
model.summary()

################################################################
# No validation needed
# Training
initial_epochs = 10

start_t = time()
history = model.fit(train_batches,
                    epochs=initial_epochs)

end_t = time()
print("training time:", end_t-start_t, "seconds.")