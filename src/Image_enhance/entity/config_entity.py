from dataclasses import dataclass
from pathlib import Path

# Configuration class for image ingestion settings
@dataclass(frozen=True)
class ImageIngestionConfig:
    """
    Configuration class for image ingestion settings.

    Attributes:
        root_dir (Path): Root directory for storing images.
        url (str): URL for fetching images.
        save_img_original (Path): Path to save original-resolution images.
        save_img_low_res (Path): Path to save low-resolution images.
        pca_components (int): Number of principal components for image compression.
    """
    root_dir: Path
    url: str
    save_img_original: Path
    save_img_low_res: Path
    pca_components: int

# Configuration class for image enhancer settings
@dataclass(frozen=True)
class ImageEnhancerConfig:
    """
    Configuration class for image enhancer settings.

    Attributes:
        load_img_low_res (Path): Path to the low-resolution image.
        save_high_res_img (Path): Path to save the enhanced high-resolution image.
        model_url (str): URL for the image enhancement model.
    """
    load_img_low_res: Path
    save_high_res_img: Path
    model_url: str

# Configuration class for comparative plot settings
@dataclass(frozen=True)
class ComparativePlotConfig:
    """
    Configuration class for comparative plot settings.

    Attributes:
        load_img_low_res (Path): Path to the low-resolution image.
        load_img_original (Path): Path to the original-resolution image.
        load_img_high_res (Path): Path to the high-resolution image.
        save_comp_plot (Path): Path to save the comparative plot.
        title (str): Title of the comparative plot.
    """
    load_img_low_res: Path
    load_img_original: Path
    load_img_high_res: Path
    save_comp_plot: Path
    title: str
