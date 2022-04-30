from teleuser import TeleUser
from utility_modules.myloggerutil import MyLoggerUtil
from utility_modules.botutil import BotUtil

from dotenv import load_dotenv
from telethon import TelegramClient, events 

import os 

# get logger for logging purposes
mylogger = MyLoggerUtil(__name__).logger 

# Reads the key,value pair from .env and adds them to environment variable
load_dotenv()

# creating bot as telegram client to connect to telegram server
bot = TelegramClient('./session/translator-bot', os.getenv('API_ID'),  os.getenv('API_HASH')).start(bot_token=os.getenv('BOT_TOKEN'))
bot_util = BotUtil()

'''
help_handler is a callback function that will be called when 
user types '/help' in chat. It will reply with a brief guide msg
on how to use this translator bot.
'''
@bot.on(events.NewMessage(pattern=r'/help|/start')) # python raw string will treat each char as literal char, including slashes or backslashes
async def help_handler(event):

    sender = await event.get_sender()
    username = sender.username
    mylogger.info(f'{username} has requested for brief guide.' )

    help_msg = bot_util.get_help_msg(username)

    await event.reply(help_msg)
    mylogger.info(f'bot has responded to {username} with brief guide.' )


'''
get_lang_handler is a callback fucntion that will be called when 
user types '/get' in chat. It will go fetch user's selected language from
db. 

If found, db will return TeleUser entity and then this function will extract
and return the value of selected language.

If not found, then bot will reply to user that record is not found and will 
ask user to type '/set' to start using the translation service.

'''
@bot.on(events.NewMessage(pattern=r'/get'))
async def get_lang_handler(event):

    sender = await event.get_sender()
    username = sender.username
    userid = event.sender_id
    chatid = event.chat_id
    mylogger.info(f'{username} has requested to get selected language. ')

    resultset = bot_util.get_language(userid=userid, chatid=chatid)
    if resultset is not None:
        await event.reply(f'{username} selected language: {resultset}.')
        mylogger.info(f'bot has responded to {username} with the selected language:{resultset}.')

    else:
        await event.reply(f'{username} record is not found in the bot. Type /set to start the translation service :)')
        mylogger.info(f'{username} is not found in db.')


      
'''
set_lang_handler is a callback function that will be called when 
user types '/set' in chat. It will display a InlineKeyboardButton 
where a list of supported languages for user to choose which langauge
they want their msg to translate to. 
'''
@bot.on(events.NewMessage(pattern=r'/set'))
async def set_lang_handler(event):

    sender = await event.get_sender()
    username = sender.username
    mylogger.info(f'{username} has requested to set language to translate to.')

    # diplays inline buttons 
    await bot.send_message(event.chat_id, f'Hi {username}, Choose an option:', buttons=bot_util.get_button_inline())
    mylogger.info(f'bot has responded to {username} with a list of supported languages to choose.' )


'''
callbackquery_handler is a callback function that will be called when 
user selects an option on inlinekeyboard upon sending '/set' command.

If user selects a language, the selected option will be set as the user 
preferred language to translate to. 

If none is selected, user messages will not be translated
'''
@bot.on(events.CallbackQuery)
async def setlang_callbackquery_handler(event):

    sender = await event.get_sender()
    username = sender.username

    userid = event.sender_id
    chatid = event.chat_id
    selected_language = ''

    if event.data == b'zh-Hans':
        selected_language = 'chinese'
        
    elif event.data == b'en':
        selected_language = 'english'
        
    elif event.data == b'ja':
        selected_language = 'japanese'
        
    elif event.data == b'ko':
        selected_language = 'korean'
        
    elif event.data == b'vi':
        selected_language = 'vietnamese'
       
    else:
        selected_language = 'none'
        
    # if set language action has performed successfully
    if bot_util.set_language(teleuser=TeleUser(userid,chatid,selected_language)) == 0:
        
        # if selected language is none, display message user msg will not be translated
        if selected_language != 'none':
            await event.edit(f'{username} has selected {selected_language} as the language to translate to.')
            mylogger.info(f'{userid} in {chatid} has chosen {selected_language}.')

        #else display message that user msg will be translated accordingly to their selection
        else:
            await event.edit(f'{username} messages will not be translated as instructed.')
            mylogger.info(f'{userid} in {chatid} has chosen not to translate messages.')
    
    # if set language action has failed
    else:
        await event.edit('Something went wrong :( Pls contact the admin @liuziannn.')
        mylogger.error('Something went wrong when interacting with sqlite.')



'''
translate_handler 

'''
@bot.on(events.NewMessage(pattern=r'[^/]'))
async def translate_handler(event):
    sender = await event.get_sender()
    username = sender.username
    
    message = event.raw_text
    userid = event.sender_id
    chatid = event.chat_id
    
    result = bot_util.translate_msg(message=message,userid=userid,chatid=chatid)
    await event.reply(f'{username}: {result}')


def main():
    bot.run_until_disconnected()
    
    

if __name__ == '__main__':
    main()