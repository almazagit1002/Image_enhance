from Image_enhance import logger
import requests
import imageio
import cv2
from sklearn.decomposition import PCA
import numpy as np
from Image_enhance.entity.config_entity import ImageIngestionConfig


class ImageProcessor:
    def __init__(self, config:ImageIngestionConfig):
        self.config = config

    def save_img_from_url(self):
        url = self.config.url
        self.save_original_img_path = self.config.save_img_original
        logger.info(f"Image obtained from : {url}")
        response = requests.get(url)
        with open(self.save_original_img_path, "wb") as f:
            f.write(response.content)
        logger.info(f"Image saved  in file: {self.save_original_img_path}")
        



    def decrese_img_resloution(self):
        logger.info(f"Decreasing the quality of the original image")
        save_low_res_img_path = self.config.save_img_low_res
        pca_components = self.config.pca_components

        img = cv2.cvtColor(cv2.imread(self.save_original_img_path),cv2.COLOR_BGR2RGB)
        logger.info(f"Image loaded from {self.save_original_img_path}")
        #split by componenets
        r,g,b = cv2.split(img)
        #normalize
        r,g,b = r/255, g/255, b/255

        #PCA components
        logger.info(f"Initializing PCA")
        pca_r = PCA(n_components=pca_components)
        reduced_r = pca_r.fit_transform(r)

        pca_g = PCA(n_components=pca_components)
        reduced_g = pca_g.fit_transform(g)


        pca_b = PCA(n_components=pca_components)
        reduced_b = pca_b.fit_transform(b)


        reconstructed_r = pca_r.inverse_transform(reduced_r)* 255
        reconstructed_g = pca_g.inverse_transform(reduced_g)* 255
        reconstructed_b = pca_b.inverse_transform(reduced_b)* 255
        img_reconstructed = (cv2.merge((reconstructed_r,reconstructed_g,reconstructed_b)))
        img_reconstructed_transfomred = img_reconstructed.astype(np.uint8)
        logger.info(f"Original image components: {img.shape}")
        logger.info(f"Low resolution image components: {img_reconstructed_transfomred.shape}")

        imageio.imwrite(save_low_res_img_path, img_reconstructed_transfomred)
        logger.info(f"Low resolution image loaded to {save_low_res_img_path}")
