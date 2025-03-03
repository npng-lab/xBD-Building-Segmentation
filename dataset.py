import math
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img

class xBD(keras.utils.Sequence):
  def __init__(self, batch_size, img_size, input_img_paths, target_img_paths, **kwargs):
    super().__init__(**kwargs)  # 경고 메시지를 해결하기 위한 코드 추가
    self.batch_size = batch_size
    self.img_size = img_size
    self.input_img_paths = input_img_paths
    self.target_img_paths = target_img_paths

  def __len__(self):
    return len(self.target_img_paths) // self.batch_size

  def __getitem__(self, idx):
    i = idx * self.batch_size
    batch_input_img_paths = self.input_img_paths[i:i+self.batch_size]
    batch_target_img_paths = self.target_img_paths[i:i+self.batch_size]
    x = np.zeros((self.batch_size, ) + self.img_size + (3, ), dtype='float32')
    for j, path in enumerate(batch_input_img_paths):
      img = load_img(path, target_size=self.img_size)
      x[j] = img
    y = np.zeros((self.batch_size, ) + self.img_size + (1, ), dtype='uint8')
    for j, path in enumerate(batch_target_img_paths):
      img = load_img(path, target_size=self.img_size, color_mode='grayscale')
      y[j] = np.expand_dims(img, 2)

    return x, y

class xBDInference(keras.utils.Sequence):
  def __init__(self, batch_size, img_size, input_img_paths, **kwargs):
      super().__init__(**kwargs)  # 경고 메시지를 해결하기 위한 코드 추가
      self.batch_size = batch_size
      self.img_size = img_size
      self.input_img_paths = input_img_paths

  def __len__(self):
      return math.ceil(len(self.input_img_paths) / self.batch_size)

  def __getitem__(self, idx):
      i = idx * self.batch_size
      batch_input_img_paths = self.input_img_paths[i: i + self.batch_size]
      x = np.zeros((self.batch_size,) + self.img_size + (3,), dtype='float32')
      for j, path in enumerate(batch_input_img_paths):
          img = load_img(path, target_size=self.img_size)
          x[j] = img
      return x