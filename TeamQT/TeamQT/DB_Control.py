import sqlite3


class DBControl:
    def __init__(self, dbName):
        self.db = self.__getDB(dbName)

    def __del__(self):
        self.db.close()

    def __getDB(self, dbName):
        return sqlite3.connect(dbName)

    def init_DB(self):
        self.cur = self.db.cursor()
        self.cur.execute('drop table if exists music;')
        self.cur.execute('create table music(artist string not null);')
        self.db.commit()

    def insertData(self, data):
        self.cur = self.db.cursor()
        self.cur.execute('insert into music(artist) values(?);', [data])
        self.db.commit()

    def insertDataList(self, dataList):
        self.cur = self.db.cursor()
        for self.item in dataList:
            self.cur.execute('insert into music(artist) values(?);', [self.item])
        self.db.commit()

    def getDataList(self):
        self.cur = self.db.cursor()
        self.list = self.cur.execute('select * from music')
        self.reList = self.list.fetchall()
        return self.reList

    def findArtist(self, name):
        self.cur = self.db.cursor()
        return self.cur.execute('select * from music where artist = ?', [name])