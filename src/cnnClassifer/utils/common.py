import os
from box.exceptions import BoxValueError
import yaml
from cnnClassifer import logger
import joblib
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64



def create_directories(path_to_directories : list[Path], verbose=True):
    """
    Creates directories if they do not exist.

    Args:
        path_to_directories (list[Path]): A list of paths to the directories to be created.
        verbose (bool): If True, logs the creation of each directory.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Directory created at: {path}")



def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a YAML file and returns its contents as a ConfigBox object.

    Args:
        path_to_yaml (Path): The path to the YAML file.
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"YAML file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError as e:
        logger.error(f"Error while converting YAML content to ConfigBox: {e}")
        raise
    except Exception as e:
        logger.error(f"Error while reading YAML file: {e}")
        raise e
    



def save_json(path: Path, data: dict):
    """
    Saves a dictionary as a JSON file.

    Args:
        path (Path): The path to the JSON file.
        data (dict): The dictionary to be saved.
    """
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
            logger.info(f"JSON file saved at: {path}")
    except Exception as e:
        logger.error(f"Error while saving JSON file: {e}")
        raise e


def load_json(path: Path) -> ConfigBox:
    """
    Loads a JSON file and returns its contents as a dictionary.

    Args:
        path (Path): The path to the JSON file.
    """
    try:
        with open(path, "r") as f:
            data = json.load(f)
            logger.info(f"JSON file loaded from: {path}")
            return ConfigBox(data)
    except Exception as e:
        logger.error(f"Error while loading JSON file: {e}")
        raise e
    


def save_binary_file(path: Path, data: Any):
    """
    Saves data to a binary file using joblib.

    Args:
        path (Path): The path to the binary file.
        data (Any): The data to be saved.
    """
    try:
        joblib.dump(data, path)
        logger.info(f"Binary file saved at: {path}")
    except Exception as e:
        logger.error(f"Error while saving binary file: {e}")
        raise e
    

def load_bin(path: Path) -> Any:
    """
    Loads data from a binary file using joblib.

    Args:
        path (Path): The path to the binary file.
    """
    try:
        data = joblib.load(path)
        logger.info(f"Binary file loaded from: {path}")
        return data
    except Exception as e:
        logger.error(f"Error while loading binary file: {e}")
        raise e
    

def get_size(path: Path) -> str:
    """
    Returns the size of a file in a human-readable format.

    Args:
        path (Path): The path to the file.
    """
    size_in_bytes = os.path.getsize(path)
    size_in_kb = size_in_bytes / 1024
    size_in_mb = size_in_kb / 1024
    if size_in_mb >= 1:
        return f"{size_in_mb:.2f} MB"
    elif size_in_kb >= 1:
        return f"{size_in_kb:.2f} KB"
    else:
        return f"{size_in_bytes} bytes"
    


def decodeImage(imgstring: str,filePath: Path) -> None:
    """
    Decodes a base64 encoded image string and saves it to a specified file path.

    Args:
        imgstring (str): The base64 encoded image string.
        filePath (Path): The path where the decoded image will be saved.
    """
    try:
        imgdata = base64.b64decode(imgstring)
        with open(filePath, 'wb') as f:
            f.write(imgdata)
        logger.info(f"Image decoded and saved at: {filePath}")
    except Exception as e:
        logger.error(f"Error while decoding and saving image: {e}")
        raise e
    

def encodeImage(filePath: Path) -> str:
    """
    Encodes an image file to a base64 string.

    Args:
        filePath (Path): The path to the image file to be encoded.
    """
    try:
        with open(filePath, 'rb') as f:
            imgdata = f.read()
            imgstring = base64.b64encode(imgdata).decode('utf-8')
            logger.info(f"Image at {filePath} encoded successfully")
            return imgstring
    except Exception as e:
        logger.error(f"Error while encoding image: {e}")
        raise e