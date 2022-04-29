import logging.config
import yaml
import os

class MyLoggerUtil():


    def __init__(self, name: str) -> None:
        self.__setup_logging()
        self.logger = logging.getLogger(name)
        

    '''
    setup_logging is a private function that read log configuration file and set the configuration to logging 

    :param logfilepath: filepath to log configuration file. Default is provided.
    :param loglevel: default log level just in case log configuration file fail to read in.    
    '''
    def __setup_logging(self, logfilepath = './config/log-config.yaml', loglevel = logging.INFO) -> None:

        if os.path.exists(logfilepath):
            with open(logfilepath,'r') as log_config_file:
                
                # safe_load will only parse YAML tags and no others. Returns dictc
                config = yaml.safe_load(log_config_file.read()) 
                logging.config.dictConfig(config)

        else:
            logging.basicConfig(level=loglevel)


    