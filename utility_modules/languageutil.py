import os
import yaml

class LanguageUtility:
    '''
    get_supported_languages function reads in a yaml file that contains 
    a list of languages this translation bot supports. 

    :param config_filepath: filepath to bot-config.yaml. default is ./config/bot-config.yaml
    :param default_supported_langs: default supported language in dictionary

    :return: a dictionary with supported language where key is the language name, value is the language code
    '''
    def get_supported_languages(self, config_filepath = './config/bot-config.yaml',
                                    default_supported_langs = {
                                            'chinese': 'zh-Hans',
                                            'english': 'en',
                                            'japanese': 'ja',
                                            'korean': 'ko',
                                            'vietnamese': 'vi',
                                            'none': 'none'
                                    }) -> dict:
        
        if os.path.exists(config_filepath):
            with open(config_filepath,'r') as bot_config_file:
                
                bot_config = yaml.safe_load(bot_config_file.read()) 
                return bot_config.get('supported_languages')

        else:
            return default_supported_langs

    '''
    get_language_code function returns the language code of selected language, passed in 
    as argument.
     

    :param language: langauge name
    :return: language code of the language name
    '''   
    def get_language_code(self, language : str) -> str:
        
        return self.get_supported_languages().get(language)
        