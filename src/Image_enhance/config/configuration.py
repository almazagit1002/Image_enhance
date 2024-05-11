from Image_enhance.constants import *
from Image_enhance.utils.common import read_yaml, create_directories
from Image_enhance.entity.config_entity import (ImageIngestionConfig,ImageEnhancerConfig)



class ConfigurationManager:
    def __init__(
        self,
        config_filepath= CONFIG_FILE_PATH,
        params_filepath= PARAMS_FILE_PATH):
        """
        Initializes ConfigurationManager with provided filepaths.

        Args:
            config_filepath (str): Filepath to configuration file. Defaults to CONFIG_FILE_PATH.
            params_filepath (str): Filepath to parameters file. Defaults to PARAMS_FILE_PATH.
        """
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)


    def get_image_ingestion_config(self) -> ImageIngestionConfig:
        """
        Retrieves image ingestion configuration settings.

        Returns:
            image_ingestion_config (ImageIngestionConfig): Image ingestion configuration object.
        """
        config = self.config.image_ingestion

        create_directories([config.root_dir])

        image_ingestion_config = ImageIngestionConfig(
            root_dir=config.root_dir,
            url=config.url,
            save_img_original=config.save_img_original,
            save_img_low_res=config.save_img_low_res,
            pca_components = self.params.PCA.PCA_COMPONENTS
        )

        return image_ingestion_config


    
    def get_image_enhancer_config(self) -> ImageEnhancerConfig:
        """
        Retrieves image ingestion configuration settings.

        Returns:
            image_ingestion_config (ImageIngestionConfig): Image ingestion configuration object.
        """
        config = self.config.image_enhance
        
        image_enhancer_config = ImageEnhancerConfig(
            load_img_low_res=config.load_img_low_res,
            save_high_res_img=config.save_high_res_img,
            model_url=self.params.ENHANCE.MODEL_URL
        )

        return image_enhancer_config

