import os
import sqlite3


class BaseDatabase:
    def __init__(self, table="worddefinition", word="a"):
        self.table = table
        word = word
        self.cursor = None
        self.connection = None

    def update(self, word):
        pass

    def select(self, word):
        pass

    def select_like(self, word):
        pass

    def insert(self, word):
        pass


class WordDicitionary(BaseDatabase):
    def __init__(self, table="worddictionary", word="a"):
        super(WordDicitionary, self).__init__(table, word)
        self.connection = sqlite3.connect('resources/database/wordui.db', timeout=1)
        self.cursor = self.connection.cursor()

    def update(self, word):
        sql = "update  '{}' set wordrank = wordrank+1 where word =trim('{}');".format(self.table, word)
        self.cursor.execute(sql)
        self.connection.commit()

    def select(self, word):
        sql = "select * from '{}' where word = trim('{}') order by wordrank desc".format(self.table, word)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def select_like(self, word):
        sql = "select * from '{}' where word like '{}%' order by wordrank desc".format(self.table, word)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def insert(self, word):
        # sql = "insert into worddictionary(word,wordrank) values (trim('" + word + "'),1)"
        sql = "insert into worddictionary(word,wordrank) values (trim('{}'),1)".format(word)
        self.cursor.execute(sql)
        self.connection.commit()


class Word_Definition_DB(BaseDatabase):
    def __init__(self, table="worddefinition", word="a"):
        super(Word_Definition_DB, self).__init__(table, word)
        self.connection = sqlite3.connect('resources/database/wordui.db', timeout=1)
        self.cursor = self.connection.cursor()

    def select(self, word):
        sql = "select * from worddefinition where word ='{}'".format(word)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def insert(self, word, definition):
        sql = "insert into worddefinition values('{}','{}')".format(word, definition)
        self.cursor.execute(sql)
        self.connection.commit()


class WordCorrection(BaseDatabase):
    def __init__(self, table="wordcorrection", word="a"):
        super(WordCorrection, self).__init__(table, word)
        self.connection = sqlite3.connect('resources/database/wordui.db', timeout=1)
        self.cursor = self.connection.cursor()

    def select(self, word):
        sql = "select vletter from wordcorrection where letter = '{}' order by rank ".format(word)
        self.cursor.execute(sql)
        return self.cursor.fetchall()


class SentenceCompletion(BaseDatabase):
    def __init__(self, table="ngram", word="a"):
        super(SentenceCompletion, self).__init__(table, word)
        self.connection = sqlite3.connect('resources/database/ngramwords.s3db', timeout=1)
        self.cursor = self.connection.cursor()

    def select(self, word):
        sql = "select word2,sum(value) value from (\
                select word2,value from n3gram where word1='{}'\
                union\
                select word3,value from n3gram where word2='{}'      ) group by word2 order by 2 desc""".format(
            word, word)
        self.cursor.execute(sql)
        return self.cursor.fetchall()
