import sqlite3, time
from Encrypt import *

def toBinary(string):
    return bytes(string, 'UTF-8')

class Login(object):
    def __init__(self, database):
        self.connected = False
        self.user = ''
        self.__password = ''
        self.db = database
        self.conn = sqlite3.connect(database)
        self.create_table()

    def connect(self, username, password):
        password = Hash(toBinary(password))
        cursor = self.conn.execute('SELECT username, password FROM ACCOUNTS')
        for row in cursor:
            if row[0] == username and row[1] == password:
                self.connected = True
                self.user = username
                self.__password = password
                return True
        else:
            return False

    def checkUsername(self, username):
        cursor = self.conn.execute('SELECT username from ACCOUNTS')
        for row in cursor:
            if row[0] == username:
                return True
        else:
            return False

    def create_table(self):
        self.conn.execute('CREATE TABLE IF NOT EXISTS ACCOUNTS \
                        (username TEXT, password TEXT)')

    def createAccount(self, username, password):
        password = Hash(toBinary(password))
        if not self.checkUsername(username):
            self.conn.execute('INSERT INTO ACCOUNTS (username, password)\
                                VALUES (\'{username}\',\'{password}\')'.format(username = username, password = password))
            self.conn.commit()
            self.connected = True
            self.user = username
            self.__password = password
            return True
        else:
            return False

    def deleteAccount(self):
        if self.connected:
            self.conn.execute('DELETE from ACCOUNTS where username=\'{username}\' and password=\'{password}\''.format(username = self.user, password = self.__password))
            self.conn.commit()
            self.connected = False
            self.user = ''
            return True
        else:
            return false

    def addColumn(self, column, column_type):
        if self.user == 'Administrator':
            try:
                self.conn.execute('ALTER table ACCOUNTS add column \'{}\' \'{}\''.format(column, column_type))
                return True
            except sqlite3.OperationalError:
                return False

    def getColumns(self):
        if self.user == 'Administrator':
            cursor = self.conn.execute('SELECT * from ACCOUNTS')
            descriptions = list()
            for description in cursor.description:
                descriptions.append(description[0])
            return descriptions

    def getAll(self):
        cursor = self.conn.execute("SELECT * from ACCOUNTS")
        description = list()
        for row in cursor:
            person = dict()
            for i, column in enumerate(row):
                person[cursor.description[i][0]] = column
            description.append(person)
        return description

    def getValue(self, column):
        values = self.getAll()
        for value in values:
            if value['username'] == self.user:
                return value[column]

    def setValue(self, column, value):
        self.conn.execute('UPDATE ACCOUNTS SET {c} = {v} WHERE username = "{u}"'\
                    .format(c = column, v = value, u = self.user))
        self.conn.commit()
        return value
            
if __name__ == '__main__':
    login = Login('Data.db')
    login.createAccount('Joseph','joseph')
    login.connect('Joseph', 'joseph')
    if login.connected:
        print('[+] Connected succesfully with {}'.format(login.user))
    else:
        print('[-] Conection Failed')
    login.addColumn('Money','INT')
    print(login.getColumns())
    print(login.getAll())
    print(login.getValue('password'))
    login.setValue('username', '\'Joseph\'')




