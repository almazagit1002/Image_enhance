from Image_enhance.config.configuration import ConfigurationManager
from Image_enhance.components.plot_comparison import PlotComparison
from Image_enhance import logger
import time


STAGE_NAME = "Plot Comparison Stage"

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

if __name__ =='__main__':
    try:
        logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<")
        obj = PlotComparisonPipeline()
        obj.main()
        logger.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<<\n\nx===============x")

    except Exception as e:
        logger.exception(e)
        raise(e)
