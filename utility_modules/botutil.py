from urllib.parse import non_hierarchical
from teledatabase import TeleDatabase
from teleuser import TeleUser
from telethon import Button
from typing import List
from utility_modules.languageutil import LanguageUtility
from utility_modules.translationutil import TranslationUtil

class BotUtil:

    def __init__(self) -> None:
        self.language_util = LanguageUtility()
        self.teledb = TeleDatabase()
        self.translation_svc = TranslationUtil()
    
    '''
    get_help_msg function returns a brief guide on how to use the translation bto

    :param username: the username of the Telegram user who requested for help  
    :return: help message
    '''
    def get_help_msg(self, username : str) -> str:
        
        help_msg = f'''Hi {username}! Thanks for using lza_translator_bot. :)\n\n/get - to retrieve your language selection.\n/set - to set a language to translate to.\n/help - to get basic guide on using this bot.

        '''
        return help_msg

    '''
    get_button_inline is a function that fetches a dict of supperted language. 
    for each supported language, an inline button, representing the language, will
    be created and added to a list.

    :return: a list of inline buttons
    
    '''
    def get_button_inline(self) -> List[Button]:
        
        supported_language = self.language_util.get_supported_languages()
        inline_buttons = []

        # convert each language into a list of Button inline
        for key,value in supported_language.items():
            inline_buttons.append([Button.inline(key,f'{value}'.encode())])
        
        return inline_buttons

    '''
    set_language is a function that set user selected language and persist 
    user choice to db. If user 

    :return: a list of inline buttons
    
    '''
    def set_language(self, teleuser : TeleUser) -> int:

        # teleuser exist in db and perform update of selected language 
        if self.teledb.get_teleuser(userid=teleuser.userid, chatid=teleuser.chatid) is not None:

            return self.teledb.update_language(teleuser=teleuser)

        # teleuser does not exist in db so insert is called
        else:
            return self.teledb.add_teleuser(teleuser=teleuser)


    '''
    get_language is a function that returns user selected language.

    :param userid: user id
    :param chatid: chat id
    :return: selected language or None
    '''
    def get_language(self,userid : str, chatid : str) ->  str:
        teleuser = self.teledb.get_teleuser(userid=userid, chatid=chatid)
        if teleuser is not None:
            return teleuser.selected_lang
        else:
            return None


    '''
    translate_msg is a function that first get user's selected language, then take 
    msg from the argument and translate into the selected language. User with selected_language as
    'none' or User record not found in db
    
    :param message: user original message
    :param userid: user id
    :param chatid: chat id
    :return: translated message or error message
    '''
    def translate_msg(self, message : str, userid : str, chatid : str) -> str:

        teleuser = self.teledb.get_teleuser(userid=userid, chatid=chatid)
        if teleuser is not None:
            selected_language = teleuser.selected_lang

            # if user has selected a language to translate to
            if selected_language != 'none':
                language_code = self.language_util.get_language_code(selected_language)
                translated_result = self.translation_svc.translate(msg=message, lang_code=language_code)

                if translated_result is not None:
                    return translated_result
                else:
                    return 'There is error when translating messages' 
        
