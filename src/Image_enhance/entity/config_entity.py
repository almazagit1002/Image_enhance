from dataclasses import dataclass
from pathlib import Path



@dataclass(frozen=True)
class ImageIngestionConfig:
    root_dir: Path
    url: str
    save_img_original: Path
    save_img_low_res: Path
    pca_components: int


@dataclass(frozen=True)
class ImageEnhancerConfig:
    load_img_low_res: Path
    save_high_res_img: Path
    model_url: str