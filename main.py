from src.cnnClassifer import logger
from src.cnnClassifer.pipeline.step_01_data_ingestion import DataIngestionPipeline
from src.cnnClassifer.pipeline.step_02_base_model_prepare import BaseModelPipeline
from src.cnnClassifer.pipeline.step_03_training import ModelTrainingPipeline
from src.cnnClassifer.pipeline.step_04_evaluation import EvaluationPipeline



STAGE_NAME = "Data Ingestion "

if __name__ == "__main__":
    logger.info(f">>>>>>>  {STAGE_NAME} Started <<<<<<<<")
    try:

        obj = DataIngestionPipeline()
        obj.main()
        logger.info(f">>>>> {STAGE_NAME} Sucessfully Completed<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e




STAGE_NAME = "Base Model Praparation"

if __name__ == "__main__":
    logger.info(f">>>>>>>  {STAGE_NAME} Started <<<<<<<<")
    try:

        obj =BaseModelPipeline()
        obj.main()
        logger.info(f">>>>> {STAGE_NAME} Sucessfully Completed<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e




STAGE_NAME = "Training"

if __name__ == "__main__":
    logger.info(f">>>>>>>  {STAGE_NAME} Started <<<<<<<<")
    try:

        obj =ModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>> {STAGE_NAME} Sucessfully Completed<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e
    



STAGE_NAME = "Model Evaluation"

if __name__ == "__main__":
    logger.info(f">>>>>>>  {STAGE_NAME} Started <<<<<<<<")
    try:

        obj =EvaluationPipeline()
        obj.main()
        logger.info(f">>>>> {STAGE_NAME} Sucessfully Completed<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e
