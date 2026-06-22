import os
import urllib.request as request
import zipfile
from cnnClassifer.utils.common import get_size,create_directories
from cnnClassifer import logger
from cnnClassifer.config.configuration import DataIngestionConfig

from pathlib import Path


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):

        create_directories([self.config.root_dir])

        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url =self.config.source_URL,
                filename = self.config.local_data_file
            )
            logger.info(f"{filename} downloaded with following info: \n{headers}")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")


    def extract_zip_file(self):
        
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(file=self.config.local_data_file, mode="r") as zip_ref:
            zip_ref.extractall(unzip_path)









