import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import imageio
from Image_enhance import logger
from Image_enhance.entity.config_entity import ImageEnhancerConfig
import warnings
warnings.filterwarnings("ignore")

class ImageEnhacer():
    def __init__(self, config:ImageEnhancerConfig):
        self.config=config
    
    def preprocess_image(self):
        """
        Preprocesses an image to make it ready for the model.

        Inputs:
            image_path (str): Path to the image file.

        Outputs:
            tf.Tensor: Processed image tensor ready for model input.
        """

        load_low_res_img_path = self.config.load_img_low_res
        # Read the image file and decode it into a tensor.
        image = tf.image.decode_image(tf.io.read_file(load_low_res_img_path))
        logger.info(f"Image obtained from : {load_low_res_img_path}")

        logger.info(f"Transfroming image into a tensor")
        # If PNG, remove the alpha channel. The model only supports images with 3 color channels.
        if image.shape[-1] == 4:
            image = image[...,:-1]

        # get image dimension  divisible by 4
        image_size = (tf.convert_to_tensor(image.shape[:-1]) // 4) * 4


        # Crop the image to ensure its dimensions are divisible by 4.
        image = tf.image.crop_to_bounding_box(image, 0, 0, image_size[0], image_size[1])
        
        # Convert the image to float32 data type.
        image = tf.cast(image, tf.float32)

        # Expand the dimensions of the image tensor to match the expected input shape of the model.
        logger.info(f"Returning tensor image")
        return tf.expand_dims(image, 0)
    
    def low_to_high_res(self, image_tensor):
        # Load Model
        model_url = self.config.model_url
        save_high_res_img_path = self.config.save_high_res_img
        print(model_url)
        model = hub.load(model_url)
        logger.info(f"Model loaded succesfully from {model_url}")

        high_res_img = model(image_tensor)
        high_res_img = tf.squeeze(high_res_img)
        high_res_img = high_res_img.numpy()

        high_res_img = high_res_img.astype(np.uint8)
        logger.info(f"Low resolution image components {image_tensor.shape}")
        logger.info(f"High resolution image components {high_res_img.shape}")
        
        imageio.imwrite(save_high_res_img_path, high_res_img)
        logger.info(f"High resolution image saved in  {save_high_res_img_path}")