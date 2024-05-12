from Image_enhance import logger
import matplotlib.pyplot as plt
from PIL import Image
from Image_enhance.entity.config_entity import ComparativePlotConfig


class PlotComparison():
    """
    Class to generate a comparative plot of three images.

    Args:
        config (ComparativePlotConfig): Configuration object containing image paths and plot settings.

    Attributes:
        config (ComparativePlotConfig): Configuration object containing image paths and plot settings.

    Methods:
        load_image(self, image_path, image_type): Loads an image from the specified path.
        get_plot_img_comparison(self): Generates a comparative plot of the loaded images.
    """
    def __init__(self,config:ComparativePlotConfig):
        """
        Initializes the PlotComparision object with the provided configuration.

        Args:
            config (ComparativePlotConfig): Configuration object containing image paths and plot settings.
        """
        self.config = config

    def load_image(self, image_path, image_type):
        """
        Loads an image from the specified path.

        Args:
            image_path (str): Path to the image file.
            image_type (str): Type of the image (e.g., "Low resolution", "Original", "High resolution").

        Returns:
            Image: The loaded image object if successful, None otherwise.
        """
        try:
            image = Image.open(image_path)
            logger.info(f"{image_type} image loaded from {image_path}")
            return image
        except Exception as e:
            logger.error(f"Error loading {image_type} image from {image_path}: {e}")
            return None
        
    def get_plot_img_comparison(self):

        """
        Generates a comparative plot of the loaded images.

        If any image fails to load, the plot generation is aborted.

        Returns:
            None
        """
        # Load images
        low_res = self.load_image(self.config.load_img_low_res, "Low resolution")
        original = self.load_image(self.config.load_img_original, "Original")
        high_res = self.load_image(self.config.load_img_high_res, "High resolution")

        if None in (low_res, original, high_res):
            logger.error("Failed to load images. Aborting plot generation.")
            return

        # Create subplots
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

  
        axes[0].imshow(low_res)
        axes[0].set_title('Low Resolution')

        axes[1].imshow(original)
        axes[1].set_title('Original')

        axes[2].imshow(high_res)
        axes[2].set_title('High Resolution')

        # Hide axes
        for ax in axes:
            ax.axis('off')

        plt.suptitle(self.config.title, fontsize=20)
        plt.savefig(self.config.save_comp_plot)
        logger.info(f"Comparative plot saved in {self.config.save_comp_plot}")
   
