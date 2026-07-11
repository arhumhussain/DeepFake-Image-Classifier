
from cnnClassifer.config.configuration import ConfiguartionManager
from cnnClassifer.components.evaluation import Evaluation
from cnnClassifer import logger




STAGE_NAME = "Model Evaluation"

class EvaluationPipeline:
    def __init__(self):
         pass
    
    def main(self):
        config = ConfiguartionManager()
        evaluation_config = config.get_evaluation_config()
        evaluation = Evaluation(config=evaluation_config)
        evaluation.evaluation()
        evaluation.save_score()
        evaluation.log_into_mlflow()

if __name__ == "__main__":
    logger.info(f">>>>>>>  {STAGE_NAME} Started <<<<<<<<")
    try:

        obj =EvaluationPipeline()
        obj.main()
        logger.info(f">>>>> {STAGE_NAME} Sucessfully Completed<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e
