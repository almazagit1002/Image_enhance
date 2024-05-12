import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import imageio
from Image_enhance import logger
from Image_enhance.entity.config_entity import ImageEnhancerConfig
import warnings
warnings.filterwarnings("ignore")

class ImageEnhancer():
    """
    Class for enhancing images using a pre-trained model.

    Attributes:
        config (ImageEnhancerConfig): Configuration object containing image enhancement settings.

    Methods:
        __init__(config): Initializes ImageEnhancer with the provided configuration.
        preprocess_image(): Preprocesses an image to make it ready for the model.
        low_to_high_res(image_tensor): Enhances the low-resolution image to high resolution using a pre-trained model.
    """

    def __init__(self, config: ImageEnhancerConfig):
        """
        Initializes ImageEnhancer with the provided configuration.

        Args:
            config (ImageEnhancerConfig): Configuration object containing image enhancement settings.
        """
        self.config = config
    
    def preprocess_image(self):
        """
        Preprocesses an image to make it ready for the model.

        Returns:
            tf.Tensor: Processed image tensor ready for model input.
        """
        load_low_res_img_path = self.config.load_img_low_res
        try:
            # Read the image file and decode it into a tensor.
            image = tf.image.decode_image(tf.io.read_file(load_low_res_img_path))
            logger.info(f"Image obtained from : {load_low_res_img_path}")

            logger.info(f"Transforming image into a tensor")
            # If PNG, remove the alpha channel. The model only supports images with 3 color channels.
            if image.shape[-1] == 4:
                image = image[..., :-1]

            # Crop the image to ensure its dimensions are divisible by 4.
            image = tf.image.crop_to_bounding_box(image, 0, 0, image.shape[0] // 4 * 4, image.shape[1] // 4 * 4)
            
            # Convert the image to float32 data type.
            image = tf.cast(image, tf.float32)

            logger.info(f"Returning tensor image")
            return tf.expand_dims(image, 0)
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")

    def low_to_high_res(self, image_tensor):
        """
        Enhances the low-resolution image to high resolution using a pre-trained model.

        Args:
            image_tensor (tf.Tensor): Low-resolution image tensor.

        Returns:
            np.ndarray: High-resolution image array.
        """
        try:
            # Load the pre-trained model
            model_url = self.config.model_url
            model = hub.load(model_url)
            logger.info(f"Model loaded successfully from {model_url}")

            # Perform image enhancement
            high_res_img = model(image_tensor)
            high_res_img = tf.squeeze(high_res_img)
            high_res_img = high_res_img.numpy()

            # Convert to uint8 data type
            high_res_img = high_res_img.astype(np.uint8)
            logger.info(f"Low resolution image components {image_tensor.shape}")
            logger.info(f"High resolution image components {high_res_img.shape}")
            
            return high_res_img
        except Exception as e:
            logger.error(f"Error enhancing image: {e}")
            return None