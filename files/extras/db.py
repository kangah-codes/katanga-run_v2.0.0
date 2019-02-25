"""
Database module for storing game highscores
"""

__author__ = 'Joshua Akangah'

import sqlite3
import datetime


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
            raise OperationalError('Could not connect to the database file')

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
                    CREATE TABLE {} (ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT NOT NULL, SCORE INT NOT NULL)
                    '''.format(name)
                )
            return True

        except sqlite3.OperationalError:
            return False

        finally:
            self.conn.close()

    def insert(self, name, score, table_name):
        """
        Metthod to insert items into the database
        :param name: Item to insert into NAME column
        :param score: Score to insert into SCORE column
        :param table_name: Table name
        :return: Bool
        """
        insert = "INSERT INTO {} (NAME, SCORE) VALUES ('%s', %s)".format(table_name)
        try:
            self.conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
            self.cursor = self.conn.cursor()
            self.cursor.execute(insert % (name, score))
            self.conn.commit()
            return True

        except sqlite3.OperationalError:
            return False

        finally:
            self.conn.close()
        
    def select_all(self, table_name):
        """
        Method to return all items in the database into a list
        :param table_name: Table name to select items from
        :return: List
        """
        self.conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
        str_top_score = "SELECT ID, NAME, SCORE FROM {}".format(table_name)
        self.cursor = self.conn.cursor()
        item_list = self.cursor.execute(str_top_score)
        items = []

        try:
            for item in item_list:
                for i in range(len(item)):
                    items.append(item[i])

            return items

        except sqlite3.OperationalError:
            return False

        finally:
            self.conn.close()

    def delete_item(self, table, name):
        """
        Mthod to delete an item from a table in the database
        :param table: Table name
        :param name: Name to delete
        :return: Bool
        """
        self.conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.conn.cursor()
        str_delete = "DELETE FROM {} WHERE NAME='{}'".format(table, name)

        try:
            self.cursor.execute(str_delete)
            self.conn.commit()
            return True

        except sqlite3.OperationalError:
            return False

        finally:
            self.conn.close()

    def search_db(self, table, name):
        """
        Method to search for item in a table
        :param table: Table name
        :param name: Name of item
        :return: Bool
        """
        self.conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.conn.cursor()
        str_selected = "SELECT NAME, SCORE FROM {table} WHERE NAME='{name}'".format(name=name, table=table)
        collected = []
        try:
            self.cursor = self.cursor.execute(str_selected)
            for i in self.cursor:
                collected.append(list(i))
            return collected
            
        except sqlite3.OperationalError:
            return False

        finally:
            self.conn.close()

    def search(self, table, name):
        """
        This method returns the outcome of the search_db method
        :param table: Table name
        :param name: Name of item
        :return: Bool
        """

        if self.search_db(table, name) is not None:
            return self.search_db(table, name)

        return False

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

    def update_data(self, table, val, name):
        """
        Method to change records of an existing item in the database table
        :param table: Table name
        :param val: Value to update into the table
        :param name: Name of item
        :return: Bool
        """
        self.conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.conn.cursor()
        str_update = "UPDATE {} SET SCORE = {} WHERE NAME='{}'".format(table, val, name)

        try:
            self.cursor.execute(str_update)
            self.conn.commit()
            return True

        except sqlite3.OperationalError:
            return False

        finally:
            self.conn.close()


