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
engine=create_engine('mysql+pymysql://sqltest:Katze7436!@localhost:3306/dynamic')
connection=engine.connect()


def create_table(tablename,col_dict):
	tablename = Table(tablename, metadata,
	Column('customer_id', Integer(), primary_key=True),	
	for i in dict_data:
		Column(i, dict_data.get(i)),

	)

	metadata.create_all(engine)





col_dict={ 'col1': String(140)}



create_table('testtable',col_dict)


