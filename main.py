from Image_enhance import logger
from Image_enhance.pipeline.LoadImagePipeline import LoadImagePipeline
from Image_enhance.pipeline.EDRN_Pipeline import EDRNPipeline


STAGE_NAME = "Loading Image Stage"
try:
    logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<")
    load_image = LoadImagePipeline()
    load_image.main()
    logger.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<<\n\nx===============x")

except Exception as e:
    logger.exception(e)
    raise(e)



STAGE_NAME = "Enhance Deep Residual Network Stage"
try:
    logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<")
    EDRN = EDRNPipeline()
    EDRN.main()
    logger.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<<\n\nx===============x")

except Exception as e:
    logger.exception(e)
    raise(e)