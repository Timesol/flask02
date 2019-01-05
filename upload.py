import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile


df = pd.read_excel('uploads/test1.xlsx', sheetname='Sheet1')



def printexcel(f):
    print(df.columns)




printexcel(df)
