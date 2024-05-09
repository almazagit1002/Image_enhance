
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
from ensure import ensure_annotations
from Image_enhance import logger
from box.exceptions import BoxValueError
import yaml
from box import ConfigBox
from pathlib import Path
import os
import cv2
from sklearn.decomposition import PCA
from PIL import Image
import warnings
import requests
import imageio
warnings.filterwarnings("ignore")


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


@ensure_annotations
def preprocess_image(image_path: Path):
    """
    Preprocesses an image to make it ready for the model.

    Inputs:
        image_path (str): Path to the image file.

    Outputs:
        tf.Tensor: Processed image tensor ready for model input.
      """
    # Read the image file and decode it into a tensor.
    image = tf.image.decode_image(tf.io.read_file(image_path))

    # If PNG, remove the alpha channel. The model only supports images with 3 color channels.
    if image.shape[-1] == 4:
        image = image[...,:-1]

    # get image dimension  divisible by 4
    image_size = (tf.convert_to_tensor(image.shape[:-1]) // 4) * 4


    # Crop the image to ensure its dimensions are divisible by 4.
    image = tf.image.crop_to_bounding_box(image, 0, 0, image_size[0], image_size[1])
    print(f"Image shape: {image.shape}")


    # Convert the image to float32 data type.
    image = tf.cast(image, tf.float32)

    # Expand the dimensions of the image tensor to match the expected input shape of the model.
    return tf.expand_dims(image, 0)


def plot_image(image, title=""):
  """
    Plots images from image tensors.
    Args:
      image: 3D image tensor. [height, width, channels].
      title: Title to display in the plot.
  """
  image = np.asarray(image)
  image = tf.clip_by_value(image, 0, 255)
  image = Image.fromarray(tf.cast(image, tf.uint8).numpy())
  plt.imshow(image)
  plt.axis("off")
  plt.title(title)

@ensure_annotations
def save_img_from_url(img_path,url):
    response = requests.get(url)
    with open(img_path, "wb") as f:
        f.write(response.content)



@ensure_annotations
def decrese_resloution(IMAGE_FILE:str,SAVE_IMAGE:Path, PCA_COMPONENTS:int):
    img = cv2.cvtColor(cv2.imread(IMAGE_FILE),cv2.COLOR_BGR2RGB)
    #split by componenets
    r,g,b = cv2.split(img)
    r,g,b = r/255, g/255, b/255

    #PCA components
    pca_r = PCA(n_components=PCA_COMPONENTS)
    reduced_r = pca_r.fit_transform(r)

    pca_g = PCA(n_components=PCA_COMPONENTS)
    reduced_g = pca_g.fit_transform(g)


    pca_b = PCA(n_components=PCA_COMPONENTS)
    reduced_b = pca_b.fit_transform(b)


    reconstructed_r = pca_r.inverse_transform(reduced_r)* 255
    reconstructed_g = pca_g.inverse_transform(reduced_g)* 255
    reconstructed_b = pca_b.inverse_transform(reduced_b)* 255
    img_reconstructed = (cv2.merge((reconstructed_r,reconstructed_g,reconstructed_b)))
    img_reconstructed_transfomred = img_reconstructed.astype(np.uint8)

    imageio.imwrite(SAVE_IMAGE, img_reconstructed_transfomred)
    return img_reconstructed,  img_reconstructed_transfomred

