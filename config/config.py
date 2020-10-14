import yaml
from util.dict import deep_update

config = None

class Config:
    def __init__(self, config_name = ''):
        config_filename = f'config/{config_name}_config.yml'
        with open('config/base_config.yml', 'r') as ymlfile:
            self.cfg = yaml.safe_load(ymlfile)
        if config_name:
            additional_config = {}
            with open(config_filename, 'r') as ymlfile:
                additional_config = yaml.safe_load(ymlfile)
                self.cfg = deep_update(self.cfg, additional_config)
        global config
        config = self.cfg
