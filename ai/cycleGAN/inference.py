"""Translate an image to another image
An example of command-line usage is:
python export_graph.py --model pretrained/apple2orange.pb \
                       --input input_sample.jpg \
                       --output output_sample.jpg \
                       --image_size 256
"""

import tensorflow.compat.v1 as tf
import os
from .model import CycleGAN
from . import utils
from ai.gpu_solve import *


FLAGS = tf.flags.FLAGS

tf.flags.DEFINE_string('model', '', 'model path (.pb)')
tf.flags.DEFINE_string('input', 'input_sample.jpg', 'input image path (.jpg)')
tf.flags.DEFINE_string('output', 'output_sample.jpg', 'output image path (.jpg)')
tf.flags.DEFINE_integer('image_size', '256', 'image size, default: 256')

def inference():
  graph = tf.Graph()

  with graph.as_default():
    with tf.gfile.FastGFile(FLAGS.input, 'rb') as f:
      image_data = f.read()
      input_image = tf.image.decode_jpeg(image_data, channels=3)
      input_image = tf.image.resize_images(input_image, size=(FLAGS.image_size, FLAGS.image_size))
      input_image = utils.convert2float(input_image)
      input_image.set_shape([FLAGS.image_size, FLAGS.image_size, 3])

    with tf.gfile.FastGFile(FLAGS.model, 'rb') as model_file:
      graph_def = tf.GraphDef()
      graph_def.ParseFromString(model_file.read())
    [output_image] = tf.import_graph_def(graph_def,
                          input_map={'input_image': input_image},
                          return_elements=['output_image:0'],
                          name='output.jpg')

  with tf.Session(graph=graph) as sess:
    generated = output_image.eval()
    with open(FLAGS.output, 'wb') as f:
      f.write(generated)

def main(unused_argv):
  inference()

if __name__ == '__main__':
  tf.app.run()

def ganConvert(model_name, input_image, output_name):
  gpu_solve()
  graph = tf.Graph()

  with graph.as_default():
    with tf.gfile.FastGFile(os.path.join('./media/cycleGAN/'+input_image), 'rb') as f:
      image_data = f.read()
      input_image = tf.image.decode_jpeg(image_data, channels=3)
      input_image = tf.image.resize_images(input_image, size=(256, 256))
      input_image = utils.convert2float(input_image)
      input_image.set_shape([256, 256, 3])

    with tf.gfile.FastGFile(os.path.join('./ai/cycleGAN/pretrained/'+model_name), 'rb') as model_file:
      graph_def = tf.GraphDef()
      graph_def.ParseFromString(model_file.read())
    [output_image] = tf.import_graph_def(graph_def,
                          input_map={'input_image': input_image},
                          return_elements=['output_image:0'],
                          name=output_name)

  with tf.Session(graph=graph) as sess:
    generated = output_image.eval()
    with open(os.path.join('./GANresult/'+output_name), 'wb') as f:
      f.write(generated)
      return f