from peewee import *
import os
db_path = 'db/data.sqlite'
#db_path = 'data.sqlite'
mainDB = SqliteDatabase(db_path,
                        pragmas = ( ('busy_timeout', 100),
                                    ('journal_mode', 'WAL')),
                                    threadlocals = True)
                                    
class dbModel(Model):
    class Meta:
        database = mainDB
        
class Community(dbModel):
    name = CharField(primary_key=True)
    
    def __str__(self):
        return str(self.name)
    
class Comments(dbModel):
    CID      = PrimaryKeyField()
    community = ForeignKeyField(Community)
    sentence  = CharField()
    neg       = FloatField()
    neu       = FloatField()
    pos       = FloatField()
    compound  = FloatField()
    cm_type   = CharField(null = True)