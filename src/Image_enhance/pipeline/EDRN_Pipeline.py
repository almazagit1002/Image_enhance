from Image_enhance.config.configuration import ConfigurationManager
from Image_enhance.components.EDRN import ImageEnhancer
from Image_enhance import logger
from pathlib import Path
import time



STAGE_NAME = "Enhance Deep Residual Network Stage"


class EDRNPipeline():
    """
    Class for executing the Enhanced Deep Residual Network (EDRN) stage of the pipeline.

    Methods:
        __init__(): Initializes EDRNPipeline.
        main(): Executes the main functionality of the EDRN stage.
    """

    def __init__(self):
        """
        Initializes EDRNPipeline.
        """
        pass

    def main(self):
        """
        Executes the main functionality of the EDRN stage.
        
        This method initializes ConfigurationManager to retrieve image enhancer configuration settings,
        then initializes ImageEnhancer with the retrieved configuration.
        It preprocesses the low-resolution image, converts it to high resolution using the EDRN model,
        and logs the image processing latency.
        """
        start = time.time()
        config = ConfigurationManager()
        image_enhance_config = config.get_image_enhancer_config()
        image_enhancer = ImageEnhancer(image_enhance_config)
        low_res_image_tensor = image_enhancer.preprocess_image()
        image_enhancer.low_to_high_res(low_res_image_tensor)
        logger.info(f"Image processor latency: {(time.time() - start):.4f} seconds")

if __name__ =='__main__':
    try:
        logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<")
        obj = EDRNPipeline()
        obj.main()
        logger.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<<\n\nx===============x")

    except Exception as e:
        logger.exception(e)
        raise(e)