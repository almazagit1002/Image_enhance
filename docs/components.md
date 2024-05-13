# Components
## components

Includes all the classes to run in the pipelines `ImageProcessor`, `ImageEnhancer`,and  `PlotComparison`.

### ImageProcessor
Stored in `load_image.py`.

```py
class ImageProcessor():
    """
    Class for processing images.

    Attributes:
        config (ImageIngestionConfig): Configuration object containing image ingestion settings.

    Methods:
        __init__(config): Initializes ImageProcessor with the provided configuration.
        save_img_from_url(): Downloads and saves the original image from the specified URL.
        decrease_img_resolution(): Decreases the resolution of the original image.
    """

    def __init__(self, config: ImageIngestionConfig):
        """
        Initializes ImageProcessor with the provided configuration.

        Args:
            config (ImageIngestionConfig): Configuration object containing image ingestion settings.
        """
        self.config = config

    def save_img_from_url(self):
        """
        Downloads and saves the original image from the specified URL.
        """
        url = self.config.url
        self.save_original_img_path = self.config.save_img_original
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception if response is not OK
            with open(self.save_original_img_path, "wb") as f:
                f.write(response.content)
            logger.info(f"Image saved in file: {self.save_original_img_path}")
        except requests.RequestException as e:
            logger.error(f"Failed to download image from {url}: {e}")

    def decrease_img_resolution(self):
        """
        Decreases the resolution of the original image.
        """
        logger.info("Decreasing the quality of the original image")
        save_low_res_img_path = self.config.save_img_low_res
        pca_components = self.config.pca_components

        try:
            img = cv2.cvtColor(cv2.imread(self.save_original_img_path), cv2.COLOR_BGR2RGB)
            logger.info(f"Image loaded from {self.save_original_img_path}")

            # Split into components and normalize
            r, g, b = cv2.split(img)
            r, g, b = r / 255, g / 255, b / 255

            # Apply PCA to each color component
            logger.info("Initializing PCA")
            pca_r = PCA(n_components=pca_components)
            reduced_r = pca_r.fit_transform(r)

            pca_g = PCA(n_components=pca_components)
            reduced_g = pca_g.fit_transform(g)

            pca_b = PCA(n_components=pca_components)
            reduced_b = pca_b.fit_transform(b)

            # Reconstruct the image
            reconstructed_r = pca_r.inverse_transform(reduced_r) * 255
            reconstructed_g = pca_g.inverse_transform(reduced_g) * 255
            reconstructed_b = pca_b.inverse_transform(reduced_b) * 255
            img_reconstructed = cv2.merge((reconstructed_r, reconstructed_g, reconstructed_b)).astype(np.uint8)
            logger.info(f"Original image components: {img.shape}")
            logger.info(f"Low resolution image components: {img_reconstructed.shape}")

            # Save the low-resolution image
            imageio.imwrite(save_low_res_img_path, img_reconstructed)
            logger.info(f"Low resolution image saved to {save_low_res_img_path}")
        except Exception as e:
            logger.error(f"Error processing image: {e}")

```

### ImageEnhancer
Stored in `EDRN.py`.

```py
class ImageEnhancer():
    """
    Class for enhancing images using a pre-trained model.

    Attributes:
        config (ImageEnhancerConfig): Configuration object containing image enhancement settings.

    Methods:
        __init__(config): Initializes ImageEnhancer with the provided configuration.
        preprocess_image(): Preprocesses an image to make it ready for the model.
        low_to_high_res(image_tensor): Enhances the low-resolution image to high resolution using a pre-trained model.
    """

    def __init__(self, config: ImageEnhancerConfig):
        """
        Initializes ImageEnhancer with the provided configuration.

        Args:
            config (ImageEnhancerConfig): Configuration object containing image enhancement settings.
        """
        self.config = config
    
    def preprocess_image(self):
        """
        Preprocesses an image to make it ready for the model.

        Returns:
            tf.Tensor: Processed image tensor ready for model input.
        """
        load_low_res_img_path = self.config.load_img_low_res
        try:
            # Read the image file and decode it into a tensor.
            image = tf.image.decode_image(tf.io.read_file(load_low_res_img_path))
            logger.info(f"Image obtained from : {load_low_res_img_path}")

            logger.info(f"Transforming image into a tensor")
            # If PNG, remove the alpha channel. The model only supports images with 3 color channels.
            if image.shape[-1] == 4:
                image = image[..., :-1]

            # Crop the image to ensure its dimensions are divisible by 4.
            image = tf.image.crop_to_bounding_box(image, 0, 0, image.shape[0] // 4 * 4, image.shape[1] // 4 * 4)
            
            # Convert the image to float32 data type.
            image = tf.cast(image, tf.float32)

            logger.info(f"Returning tensor image")
            return tf.expand_dims(image, 0)
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")

    def low_to_high_res(self, image_tensor):
        """
        Enhances the low-resolution image to high resolution using a pre-trained model.

        Args:
            image_tensor (tf.Tensor): Low-resolution image tensor.

        Returns:
            np.ndarray: High-resolution image array.
        """
        try:
            # Load the pre-trained model
            model_url = self.config.model_url
            save_high_res_img_path = self.config.save_high_res_img
            model = hub.load(model_url)
            logger.info(f"Model loaded successfully from {model_url}")

            # Perform image enhancement
            high_res_img = model(image_tensor)
            high_res_img = tf.squeeze(high_res_img)
            high_res_img = high_res_img.numpy()

            # Convert to uint8 data type
            high_res_img = high_res_img.astype(np.uint8)
            logger.info(f"Low resolution image components {image_tensor.shape}")
            logger.info(f"High resolution image components {high_res_img.shape}")
            
            imageio.imwrite(save_high_res_img_path, high_res_img)
        except Exception as e:
            logger.error(f"Error enhancing image: {e}")
            return None

```

### PlotComparison
Stored in `plot_comparison.py`.

```py
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
   
```