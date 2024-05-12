from Image_enhance import logger
from Image_enhance.pipeline.LoadImagePipeline import LoadImagePipeline
from Image_enhance.pipeline.EDRN_Pipeline import EDRNPipeline
from Image_enhance.pipeline.PlotComparisonPipeline import PlotComparisonPipeline
import yaml
from Image_enhance.constants import *


# Function to load and update PCA_COMPONENTS value in the parameters file
def update_pca_components(params_file_path):
    try:
        with open(params_file_path, 'r') as yaml_file:
            data = yaml.safe_load(yaml_file)

        new_pca_components = input("Enter new value for PCA_COMPONENTS: ")
        data['PCA']['PCA_COMPONENTS'] = int(new_pca_components)

        with open(params_file_path, 'w') as yaml_file:
            yaml.dump(data, yaml_file)

        logger.error(f"Updated PCA_COMPONENTS value has been written to {params_file_path}")
    except Exception as e:
        print(f"Error updating PCA_COMPONENTS: {e}")

# Function to execute a stage of the pipeline
def execute_pipeline_stage(stage_name, pipeline_instance):
    try:
        logger.error(f">>>>>>> stage {stage_name} started <<<<<<<<<<<<")
        pipeline_instance.main()
        logger.error(f">>>>>>> stage {stage_name} completed <<<<<<<<<<<<\n\nx===============x")
    except Exception as e:
        logger.error(f"Error in stage {stage_name}: {e}")
        raise e

if __name__ =='__main__':
    # Update PCA_COMPONENTS value
    update_pca_components(PARAMS_FILE_PATH)

    # Execute stages of the pipeline
    stages = [
        ("Loading Image Stage", LoadImagePipeline()),
        ("Enhance Deep Residual Network Stage", EDRNPipeline()),
        ("Plot Comparison Stage", PlotComparisonPipeline())
    ]

    for stage_name, pipeline_instance in stages:
        execute_pipeline_stage(stage_name, pipeline_instance)