import unittest

from dotenv import load_dotenv
from utility_modules.botutil import BotUtil
from utility_modules.languageutil import LanguageUtility

class TestBotUtil(unittest.TestCase):

    '''
    Test get_help_msg function from module utility_modules.languageutil
    '''
    def test_get_help_msg(self):
        load_dotenv()
        mock_help_msg = BotUtil().get_help_msg(username='John')
        correct_output = '''Hi John! Thanks for using lza_translator_bot. :)\n\n/get - to retrieve your language selection.\n/set - to set a language to translate to.\n/help - to get basic guide on using this bot.

        ''' 
        self.assertEqual(mock_help_msg,correct_output)
        

if '__name__'=='__main__':
    unittest.main()