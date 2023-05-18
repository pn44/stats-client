import configparser
import csv
import functools
import os

from client.config.constants import SETTINGS_FILE_NAMES, DEFAULT_SETTINGS


class Config():
    config = configparser.ConfigParser
    
    def __init__(self, filenames=SETTINGS_FILE_NAMES):
        self.filenames = filenames
        
        self.config = configparser.ConfigParser()
        self.config.read_dict(DEFAULT_SETTINGS)
        
        self.get = self.config.get
        self.set = self.config.set
        self.getint = self.config.getint
        self.getfloat = self.config.getfloat
        self.getboolean = self.config.getboolean
        self.remove_option = self.config.remove_option
        
    def getlist(self, *a, **kw):
        cols2show = self.config.get(*a, **kw)
        return next(csv.reader([cols2show], skipinitialspace=True))
        
    def write(self):
        with open(self.filenames[-1], "w") as f:
            self.config.write(f)

    def _read_config(self):
        self.config.read(self.filenames)
    
    def _init_config(self):
        os.makedirs(os.path.split(self.filenames[-1])[0])

    def read_config(self):
        if not os.path.isfile(self.filenames[-1]):
            self._init_config()
            self.write()
        self._read_config()
