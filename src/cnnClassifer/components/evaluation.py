
import tensorflow as tf
from cnnClassifer.constants.paths import *
from cnnClassifer.utils.common import read_yaml,create_directories,save_json
from cnnClassifer.entity.config_entity import EvaluationConfig
from cnnClassifer import logger
import mlflow
import mlflow.keras
from urllib.parse import urlparse



class Evaluation:

    def __init__(self, config: EvaluationConfig):
        self.config = config

        create_directories([self.config.root_dir])

    def _valid_generator(self):

        datagenerator_kwargs = dict(
            rescale=1./255,
            validation_split=0.3
        )

        dataflow_kwargs = dict(
            target_size=tuple(self.config.params_image_size[:2]),
            batch_size=self.config.params_batch_size,
            interpolation="bilinear"
        )

        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset="validation",
            shuffle=False,
            **dataflow_kwargs
        )

    @staticmethod
    def load_model(path: Path):
        return tf.keras.models.load_model(path)

    def evaluation(self):
        self.model = self.load_model(self.config.model_path)

        self._valid_generator()

        self.score = self.model.evaluate(
            self.valid_generator
        )

    def save_score(self):
        scores = {
            "loss": float(self.score[0]),
            "accuracy": float(self.score[1])
        }

        save_json(
            path=Path("artifacts/evaluation/score.json"), data=scores)

    def log_into_mlflow(self):
        try:
            mlflow.set_registry_uri(self.config.mlflow_uri)
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

            with mlflow.start_run():
                mlflow.log_params(self.config.all_params)
                mlflow.log_metrics({
                    "loss": self.score[0],
                    "accuracy": self.score[1]
                })

                # Model Registry works with a database-backed store (e.g. dagshub, postgres, mysql, sqlite)
                if tracking_url_type_store != "file":
                    mlflow.keras.log_model(self.model, "model", registered_model_name="DeepFakeVGG16Model")
                else:
                    mlflow.keras.log_model(self.model, "model")
        except Exception as e:
            logger.warning(f"Failed to log to remote MLflow: {e}. Falling back to local MLflow log.")
            mlflow.set_tracking_uri("file:./mlruns")
            with mlflow.start_run():
                mlflow.log_params(self.config.all_params)
                mlflow.log_metrics({
                    "loss": self.score[0],
                    "accuracy": self.score[1]
                })
                mlflow.keras.log_model(self.model, "model")