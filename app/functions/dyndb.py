from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, Numeric, String, ForeignKey, Boolean
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import PrimaryKeyConstraint, UniqueConstraint, CheckConstraint
from sqlalchemy import Index
from sqlalchemy.sql import select
from sqlalchemy import desc
from sqlalchemy.sql import func
from sqlalchemy import cast
from sqlalchemy import update
from sqlalchemy import insert


metadata=MetaData()
engine=create_engine('mysql+pymysql://sqltest:Katze7436!@localhost:3306/sqltest')
connection=engine.connect()

def create_db(tablename,col_list):

    tablename = Table(tablename, metadata,*col_list)
    metadata.create_all(engine)

def queryall(table):
    s = select([table])
    rp = connection.execute(s)

    return rp
    



col_list=[Column('customer4_id', Integer(), primary_key=True),Column('customer4_name', String(140), index=True)]
create_db('customer4',col_list)



