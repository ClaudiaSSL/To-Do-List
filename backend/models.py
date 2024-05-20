from db_utils import Model, DBquery

class Task(Model):
    fields={
        'id':int,
        'description':str,
        'about':str,
        'done':bool
    }
    def fetchall(self,  model, table:str) -> None:
       DBquery.fetch_all(self, model, table)