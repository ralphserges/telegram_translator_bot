import sqlite3
from teleuser import TeleUser
from utility_modules.myloggerutil import MyLoggerUtil

class TeleDatabase: 

    def __init__(self) -> None:
        self.mylogger = MyLoggerUtil(__name__).logger
        self.con = sqlite3.connect('./sqlite_records/telegramuser.db')
        self.__setup_table()


    '''
    setup_table is a private function that is called when TeleDatabase is initialized.
    This function will create table, if not exists, to store user state,including userid, 
    chatid and selected language user chose. The composite key is userid and chatid.
    '''
    def __setup_table(self) -> None: 
        create_table_stmt = '''
            CREATE TABLE IF NOT EXISTS telegramuser (
                userid TEXT NOT NULL,
                chatid TEXT NOT NULL,
                selected_lang TEXT,

                PRIMARY KEY (userid, chatid)
            )
        '''
        with self.con:
            try:
                cur = self.con.cursor()
                cur.execute(create_table_stmt)
                self.mylogger.info('telegramuser table has set up successfully in sqlite.')

            except sqlite3.Error as e:
                self.mylogger.error(e.args[0])


    '''
    add_teleuser is a function that adds a new telegram user state to the telegramuser table. 
    If successfully added, this function will return 0 to denote success.
    Else, this function will return 1 to denote failure. Failing to add could be due to duplicate entry.

    :param teleuser: TeleUser entity to be stored to db
    :return: int 0 or 1
    '''
    def add_teleuser(self, teleuser : TeleUser) -> int:
        with self.con:
            try:
                cur = self.con.cursor()
                cur.execute('INSERT INTO telegramuser VALUES (:teleuserid, :telechatid, :selected_lang)',
                                                                {'teleuserid':teleuser.userid, 
                                                                'telechatid': teleuser.chatid,
                                                                'selected_lang': teleuser.selected_lang})
                
                return 0
            
            except sqlite3.Error as e:
                self.mylogger.error(e.args[0])
                return 1
    


    '''
    get_teleuser is a function that search for an unique entry, using userid and chatid.

    :param userid: userid of the user for searching.
    :param chatid: chatid of the chat user is in.
    :return: TeleUser entity if found. Else, return None.
    '''
    def get_teleuser(self, userid : str, chatid : str) -> TeleUser:
        
        try:
            cur = self.con.cursor()
            cur.execute('SELECT * FROM telegramuser WHERE userid=:teleuserid AND chatid=:telechatid', 
                                                                {'teleuserid': userid,
                                                                'telechatid' : chatid})

            resultset = cur.fetchone()

            if resultset is not None:
                self.mylogger.info(f'userid:{userid} with chatid:{chatid} is found.')
                return TeleUser(resultset[0],resultset[1],resultset[2])
            else:
                self.mylogger.info(f'userid:{userid} with chatid:{chatid} is not found.')
                return None

        except sqlite3.Error as e:
            self.mylogger.error(e.args[0])
            return None

    

    '''
    update_language is a function that perform update to existing user's selected language
    to another supported language.

    :param teleuser: TeleUser to perform update on.
    :return: 0 if update is successful. 1 if update is failure.
    '''
    def update_language(self, teleuser : TeleUser) -> int :
        
        with self.con:
            try:
                cur = self.con.cursor()
                cur.execute('UPDATE telegramuser SET selected_lang=:selected_lang WHERE userid=:teleuserid AND chatid=:telechatid',
                                                                {'teleuserid':teleuser.userid, 
                                                                'telechatid': teleuser.chatid,
                                                                'selected_lang': teleuser.selected_lang})
                
                self.mylogger.info(f'userid:{teleuser.userid} language is updated to {teleuser.selected_lang} for chatid:{teleuser.chatid}.')
                return 0
            
            except sqlite3.Error as e:
                self.mylogger.error(e.args[0])
                return 1        
       

    '''
    close_connection is a function that closes the connection to the database.
    '''
    def close_connection(self) -> None:
        self.con.close()
        self.mylogger.info('db connection is closed')



if __name__ == '__main__':
    db = TeleDatabase()
    db.update_language(TeleUser('123','456','englishh'))
    print(db.get_teleuser('123','456').selected_lang)
    db.close_connection()
    