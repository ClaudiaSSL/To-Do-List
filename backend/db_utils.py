from typing import Generator
import sqlite3
import re

class Model:
    pass


class DBquery():
    def __init__(self,db) -> None:
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

    #for code sanatizer
    @staticmethod
    def check_if_string(variable):
            if type(variable) == str:
                return True
            else:
                return False

    #for code sanatizer
    @staticmethod
    def check_if_has_spaces(variable):
         return bool(re.search(r"\s", variable))

    def fetch_all(self, model, table:str) -> Generator[dict, None, None]:

        #code sanatizer - add security checks to avoid suspicious behavior on db
        if self.check_if_string(table) and not self.check_if_has_spaces(table):
            self.cur.execute(f"SELECT * FROM {table}")
            records = self.cur.fetchall()

        for record in records:
            yield {
                field_name:model.fields[field_name](record[index])
                for index, field_name in enumerate(model.fields.keys())
            }
        return None

    
    def add(self, data:tuple, table:str ) -> None:
        if self.check_if_string(table) and not self.check_if_has_spaces(table):
            self.cur.execute(f"INSERT INTO {table}(description, about, done) VALUES (?, ?, ?)", data)
            self.con.commit()

    
    def update(self, data:tuple, table:str) -> None:
        if self.check_if_string(table) and not self.check_if_has_spaces(table):
            self.cur.execute(f'UPDATE {table} SET description = ?, about = ?, done = ? WHERE id = ?', data)
            self.con.commit()

    def delete(self, id_num:int, table:str) -> None:
        if self.check_if_string(table) and not self.check_if_has_spaces(table):
            self.cur.execute(f'DELETE FROM {table} WHERE id = ?', [id_num])
            self.con.commit()

    def close(self) -> None:
        self.con.close()

    
    def delete_table(self, table:str) -> None:
        if self.check_if_string(table) and not self.check_if_has_spaces(table):
            self.cur.execute(f"DROP TABLE {table}")
            self.close()


    def create_table(self) -> None:
        self.cur.execute("""CREATE TABLE tasks(
                            id INTEGER PRIMARY KEY, 
                            description text NOT NULL, 
                            about text NOT NULL, 
                            done BOOLEAN)""")
        res = self.cur.execute("SELECT name FROM sqlite_master")
        res.fetchone()
        check_c = self.cur.execute("select * from tasks")
        names = list(map(lambda x: x[0], check_c.description))
        self.con.commit()
        self.close()
        print('table created')

    def check_if_table_exists(self) -> bool:
        res = self.cur.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'; """).fetchall()
        if res is not None:
            self.con.commit()
            self.close()
            print('table exists!')
            return True
        else:
            print('table does not exists!')
            self.con.commit()
            self.close()
            return False

    def autocomplete(self, table:str, column: str, value:str) -> Generator[dict, None, None]:
        if self.check_if_string(table) and self.check_if_string(column) and not self.check_if_has_spaces and not self.check_if_has_spaces:
            self.cur.execute(f"SELECT {column} FROM {table} WHERE {column} LIKE '{value}%'")
            records = self.cur.fetchall()
            for record in records:
                yield record[0]
            return None
        






        
