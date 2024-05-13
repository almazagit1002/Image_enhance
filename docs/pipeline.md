# Pipeline
## pipline
Includes the pipeline stages  `Loading Image Stage`, `Enhance Deep Residual Network Stage`,and `Plot Comparison Stage`, runed by the classes `LoadImagePipeline`, `EDRNPipeline`, and `PlotComparisonPipeline` respectively. 

### Loading Image Stage

Stored in `LoadImagePipeline.py` runs the methods form the `ImageProcessor` imported from the `load_image.py` from the  `components` directory.
```py
class LoadImagePipeline():
    """
    Class for executing the image loading stage of the pipeline.

    Methods:
        __init__(): Initializes LoadImagePipeline.
        main(): Executes the main functionality of the image loading stage.
    """

    def __init__(self):
        """
        Initializes LoadImagePipeline.
        """
        pass

    def main(self):
        """
        Executes the main functionality of the image loading stage.
        
        This method initializes ConfigurationManager to retrieve image ingestion configuration settings,
        then initializes ImageProcessor with the retrieved configuration.
        It saves images from the specified URL and decreases their resolution.
        """
        start = time.time()
        config = ConfigurationManager()
        image_ingestion_config = config.get_image_ingestion_config()
        image_processor = ImageProcessor(image_ingestion_config)
        image_processor.save_img_from_url()
        image_processor.decrease_img_resolution()
        logger.info(f"Image processor latency: {(time.time() - start):.4f} seconds")

```
### Enhance Deep Residual Network Stage
Stored in `EDRN_Pipeline.py` runs the methods form the `ImageEnhancer` imported from the `EDRN.py` from the  `components` directory.
```py
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

```

### Plot Comparison Stage
Stored in `PlotComparisonPipeline.py` runs the methods form the `PlotComparison` imported from the `plot_comparison.py` from the  `components` directory.
```py
class PlotComparisonPipeline:
    """
    Class for executing the plot comparison stage of the pipeline.

    Attributes:
        STAGE_NAME (str): Name of the plot comparison stage.

    Methods:
        __init__(): Initializes PlotComparisonPipeline.
        main(): Executes the main functionality of the plot comparison stage.
    """

    def __init__(self):
        """
        Initializes PlotComparisonPipeline.
        """
        pass

    def main(self):
        """
        Executes the main functionality of the plot comparison stage.
        """
        start = time.time()
        config = ConfigurationManager()
        plot_config = config.get_plot_comparison_config()
        plot_comp = PlotComparison(plot_config)
        plot_comp.get_plot_img_comparison()
        logger.info(f"Plot comparison latency: {(time.time() - start):.4f} seconds")

```