import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from app.models import User, Post, Location
from app import  db



def sendpandas(filename):

    varfile=filename
    df = pd.read_excel('uploads/{0}'.format(varfile), sheetname='Sheet1')
    print(df.columns)
    print(df['Standort'][0])
    location = Location(city=df['Standort'][0], gateway=df['Gateway'][0], network=df['Network'][0],technologie=df['Technologie'][0])
    db.session.add(location)
    db.session.commit()    
