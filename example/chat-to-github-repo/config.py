# config.py
import yaml
from dotenv import load_dotenv


def load_config(config_file="config.yaml"):
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    return config


Config = load_config()

load_dotenv()
