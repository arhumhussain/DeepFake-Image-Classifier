from cnnClassifer.constants.paths import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from cnnClassifer.utils.common import read_yaml, create_directories
from cnnClassifer.entity.config_entity import DataIngestionConfig,BaseModleConfig,PrepareCallbacksConfig,TraningConfig,EvaluationConfig
import os
from pathlib import Path



class ConfiguartionManager:
    def __init__(self, config_filepath=CONFIG_FILE_PATH, params_filepath=PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        create_directories([self.config.artifacts_root])




    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        data_ingestion_config = DataIngestionConfig(
            root_dir=Path(config.root_dir),
            source_URL=config.source_URL,
            local_data_file=Path(config.local_data_file),
            unzip_dir=Path(config.unzip_dir)
        )
        return data_ingestion_config
 


 
    def get_base_model_config(self) -> BaseModleConfig:

        config = self.config.base_model
        create_directories([config.root_dir])

        base_model_config = BaseModleConfig(
            root_dir=Path(config.root_dir),
            base_model_path=Path(config.base_model_path),
            updated_model_path=Path(config.updated_model_path),
            params_image_size = self.params.IMAGE_SIZE,
            params_learning_rate = self.params.LEARNING_RATE,
            params_include_top = self.params.INCLUDE_TOP,
            params_weights = self.params.WEIGHTS,
            params_classes = self.params.CLASSES,

        )

        return base_model_config
    



    def get_callback_config(self) -> PrepareCallbacksConfig:

        config = self.config.prepare_callbacks
        model_ckpt_dir = os.path.dirname(config.checkpoint_model_filepath)
        create_directories(
            [Path(model_ckpt_dir),
             Path(config.tensorboard_root_log_dir)
             
             ])
        callback_config = PrepareCallbacksConfig(
            root_dir = Path(config.root_dir),
            tensorboard_root_log_dir = Path(config.tensorboard_root_log_dir),
            checkpoint_model_filepath = Path(config.checkpoint_model_filepath)
        )

        return callback_config
    

    


    def get_training_config(self) -> TraningConfig:
        training = self.config.training
        base_model = self.config.base_model
        params = self.params
        training_data_path = os.path.join(self.config.data_ingestion.unzip_dir, "Human-Face")

        create_directories([Path(training.root_dir)])

        training_config = TraningConfig(
            root_dir = Path(training.root_dir),
            trained_model_path = Path(training.trained_model_path),
            updated_model_path = Path(base_model.updated_model_path),
            training_data_path=Path(training_data_path),
            params_epochs=params.EPOCHS,
            params_batch_size=params.BATCH_SIZE,
            params_is_augmentation=params.AUGMENTATION,
            params_image_size=params.IMAGE_SIZE
        )
        

        return training_config
    
    
    def get_evaluation_config(self) -> EvaluationConfig:
        evaluation_config = EvaluationConfig(
            root_dir=Path(self.config.evaluation.root_dir),
            model_path=Path("artifacts/training/model.h5"),
            training_data=Path("artifacts/data_ingestion/Human-Face"),
            all_params=self.params,
            mlflow_uri=self.config.evaluation.mlflow_uri,
            params_batch_size=self.params.BATCH_SIZE,
            params_image_size=self.params.IMAGE_SIZE
        )

        return evaluation_config