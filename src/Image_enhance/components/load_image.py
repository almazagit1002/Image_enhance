from Image_enhance import logger
import requests
import imageio
import cv2
from sklearn.decomposition import PCA
import numpy as np
from Image_enhance.entity.config_entity import ImageIngestionConfig

import requests
import cv2
import imageio
import numpy as np
from sklearn.decomposition import PCA

class ImageProcessor():
    """
    Class for processing images.

    Attributes:
        config (ImageIngestionConfig): Configuration object containing image ingestion settings.

    Methods:
        __init__(config): Initializes ImageProcessor with the provided configuration.
        save_img_from_url(): Downloads and saves the original image from the specified URL.
        decrease_img_resolution(): Decreases the resolution of the original image.
    """

    def __init__(self, config: ImageIngestionConfig):
        """
        Initializes ImageProcessor with the provided configuration.

        Args:
            config (ImageIngestionConfig): Configuration object containing image ingestion settings.
        """
        self.config = config

    def save_img_from_url(self):
        """
        Downloads and saves the original image from the specified URL.
        """
        url = self.config.url
        self.save_original_img_path = self.config.save_img_original
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception if response is not OK
            with open(self.save_original_img_path, "wb") as f:
                f.write(response.content)
            logger.info(f"Image saved in file: {self.save_original_img_path}")
        except requests.RequestException as e:
            logger.error(f"Failed to download image from {url}: {e}")

    def decrease_img_resolution(self):
        """
        Decreases the resolution of the original image.
        """
        logger.info("Decreasing the quality of the original image")
        save_low_res_img_path = self.config.save_img_low_res
        pca_components = self.config.pca_components

        try:
            img = cv2.cvtColor(cv2.imread(self.save_original_img_path), cv2.COLOR_BGR2RGB)
            logger.info(f"Image loaded from {self.save_original_img_path}")

            # Split into components and normalize
            r, g, b = cv2.split(img)
            r, g, b = r / 255, g / 255, b / 255

            # Apply PCA to each color component
            logger.info("Initializing PCA")
            pca_r = PCA(n_components=pca_components)
            reduced_r = pca_r.fit_transform(r)

            pca_g = PCA(n_components=pca_components)
            reduced_g = pca_g.fit_transform(g)

            pca_b = PCA(n_components=pca_components)
            reduced_b = pca_b.fit_transform(b)

            # Reconstruct the image
            reconstructed_r = pca_r.inverse_transform(reduced_r) * 255
            reconstructed_g = pca_g.inverse_transform(reduced_g) * 255
            reconstructed_b = pca_b.inverse_transform(reduced_b) * 255
            img_reconstructed = cv2.merge((reconstructed_r, reconstructed_g, reconstructed_b)).astype(np.uint8)
            logger.info(f"Original image components: {img.shape}")
            logger.info(f"Low resolution image components: {img_reconstructed.shape}")

            # Save the low-resolution image
            imageio.imwrite(save_low_res_img_path, img_reconstructed)
            logger.info(f"Low resolution image saved to {save_low_res_img_path}")
        except Exception as e:
            logger.error(f"Error processing image: {e}")
