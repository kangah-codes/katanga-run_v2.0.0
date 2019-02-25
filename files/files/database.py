"""
Database module for storing game highscores
This code isn't really necessary as there are easier ways for storing game highscores,
Was just experimenting and learning how to use sqlite3
"""

__author__ = 'Joshua Akangah'

import sqlite3


class Database:
    """
    Database class
    """

    def __init__(self, name='scores.sqlite'):
        """
        Init method
        :param name: Preferred name of database file to create
        BY default it is set to scores.db
        """
        try:
            self.name = name
            self.conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
            self.cursor = self.conn.cursor()
            self.conn.commit()

        except sqlite3.OperationalError:
            raise sqlite3.OperationalError('Could not connect to the database file')

        finally:
            self.conn.close()

    def create_table(self, name):
        """
        Method to create a table in the database
        :param name: Name of table
        :return: Bool
        """
        try:
            self.conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
            self.cursor = self.conn.cursor()
            self.cursor.execute(
                '''
                CREATE TABLE {} (ID INTEGER PRIMARY KEY AUTOINCREMENT, SCORE INT NOT NULL)
                '''.format(name)
            )
            return True

        except sqlite3.OperationalError:
            return False

        finally:
            self.conn.close()

    def get_length(self, table):
        """
        Method to return number of items in a table
        :param table: Table name
        :return: int
        """
        self.conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.conn.cursor()
        str_all = "SELECT COUNT(*) FROM {}".format(table)
        self.cursor.execute(str_all)
        return self.cursor.fetchone()[0]

    def insert(self, score, table_name):
        """
        Metthod to insert items into the database
        :param date: Date when the score was made
        :param score: Score to insert into SCORE column
        :param table_name: Table name
        :return: Bool
        """
        insert = "INSERT INTO {} (SCORE) VALUEs (%s)".format(table_name)
        try:
            self.conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
            self.cursor = self.conn.cursor()
            self.cursor.execute(insert % (score))
            self.conn.commit()
            return True

        except sqlite3.OperationalError:
            return False

        finally:
            self.conn.close()

    def update_data(self, table, score, ids):
        """
        Method to change records of an existing item in the database table
        :param table: Table name
        :param score: ScoreValue to update into the table
        :param ids: ID of item
        :param date: Date to insert
        :return: Bool
        """
        self.conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.conn.cursor()
        str_update = "UPDATE {} SET SCORE={} WHERE ID={}".format(table, score, ids)

        try:
            self.cursor.execute(str_update)
            self.conn.commit()
            return True

        except IndexError:
            return False

        finally:
            self.conn.close()

    def max(self, table):
        self.conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.conn.cursor()
        str_selected = "SELECT SCORE FROM {table}".format(table=table)
        collected = []
        try:
            self.cursor = self.cursor.execute(str_selected)
            for i in self.cursor:
                collected.append(i)

            return max(collected)[0]

        except sqlite3.OperationalError:
            return False

        finally:
            self.conn.close()
