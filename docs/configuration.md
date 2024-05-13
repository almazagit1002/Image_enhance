# Configuration
## configuration
Class for managing configuration settings `ConfigurationManager`.

### ConfigurationManager
```py
class ConfigurationManager:
    """
    Class for managing configuration settings.

    Attributes:
        config_filepath (str): Filepath to the configuration file.
        params_filepath (str): Filepath to the parameters file.

    Methods:
        __init__(config_filepath, params_filepath): Initializes ConfigurationManager with provided filepaths.
        get_image_ingestion_config(): Retrieves image ingestion configuration settings.
        get_image_enhancer_config(): Retrieves image enhancer configuration settings.
        get_plot_comparison_config(): Retrieves comparative plot configuration settings.
    """

    def __init__(
        self,
        config_filepath=CONFIG_FILE_PATH,
        params_filepath=PARAMS_FILE_PATH):
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
            pca_components=self.params.PCA.PCA_COMPONENTS
        )

        return image_ingestion_config

    def get_image_enhancer_config(self) -> ImageEnhancerConfig:
        """
        Retrieves image enhancer configuration settings.

        Returns:
            image_enhancer_config (ImageEnhancerConfig): Image enhancer configuration object.
        """
        config = self.config.image_enhance

        image_enhancer_config = ImageEnhancerConfig(
            load_img_low_res=config.load_img_low_res,
            save_high_res_img=config.save_high_res_img,
            model_url=self.params.ENHANCE.MODEL_URL
        )

        return image_enhancer_config

    def get_plot_comparison_config(self) -> ComparativePlotConfig:
        """
        Retrieves comparative plot configuration settings.

        Returns:
            plot_comparison_config (ComparativePlotConfig): Comparative plot configuration object.
        """
        config = self.config.comparative_plot

        plot_comparison_config = ComparativePlotConfig(
            load_img_low_res=config.load_img_low_res,
            load_img_original=config.load_img_original,
            load_img_high_res=config.load_img_high_res,
            save_comp_plot=config.save_comp_plot,
            title=config.title
        )

        return plot_comparison_config
```
