from Image_enhance.config.configuration import ConfigurationManager
from Image_enhance.components.EDRN import ImageEnhacer
from Image_enhance import logger
from pathlib import Path
import time



STAGE_NAME = "Enhance Deep Residual Network Stage"


class EDRNPipeline():
    def __init__(self):
        pass

    def main(self):

        start = time.time()
        config = ConfigurationManager()
        image_enhance_config = config.get_image_enhancer_config()
        image_enhancer = ImageEnhacer(image_enhance_config)
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