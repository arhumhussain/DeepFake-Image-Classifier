from cnnClassifer import logger
from cnnClassifer.pipeline.step_01_data_ingestion import DataIngestionPipeline





STAGE_NAME = "Data Ingestion"

if __name__ == "__main__":
    logger.info(f">>>>>>>  {STAGE_NAME} Started <<<<<<<<")
    try:

        obj = DataIngestionPipeline()
        obj.main()
        logger.info(f">>>>> {STAGE_NAME} Sucessfully Completed<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e
