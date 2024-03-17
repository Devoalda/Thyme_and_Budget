# settings/env_singleton.py
import os
from pathlib import Path

import environ

ENV_FILE_PATH = "../.env"

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class EnvSingleton(metaclass=Singleton):
    def __init__(self):
        self.env = environ.Env(# set casting, default value
            DEBUG=(bool, True))
        # Build paths inside the project like this: BASE_DIR / 'subdir'.
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        environ.Env.read_env(os.path.join(self.BASE_DIR, ENV_FILE_PATH))
