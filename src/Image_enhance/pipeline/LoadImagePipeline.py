from Image_enhance.config.configuration import ConfigurationManager
from Image_enhance.components.load_image import ImageProcessor
from Image_enhance import logger
import time



STAGE_NAME = "Loading Image Stage"


class LoadImagePipeline():
    def __init__(self):
        pass

    def main(self):

        start = time.time()
        config = ConfigurationManager()
        image_ingestion_config = config.get_image_ingestion_config()
        image_processor = ImageProcessor(image_ingestion_config)
        image_processor.save_img_from_url()
        image_processor.decrese_img_resloution()
        logger.info(f"Image processor latency: {(time.time() - start):.4f} seconds")


if __name__ =='__main__':
    try:
        logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<")
        obj = LoadImagePipeline()
        obj.main()
        logger.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<<\n\nx===============x")

    except Exception as e:
        logger.exception(e)
        raise(e)