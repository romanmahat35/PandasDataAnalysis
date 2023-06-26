import pandas as pd
import numpy as np
import os
from datetime import datetime
from datetime import date

"""
#sample data 
  name   salary         dob
  1  roman   1000.0  1995-06-10
  2  ashis   1100.0  1996-07-10
  3    raj  11000.0  1993-08-01
  2  ashis   1100.0  1996-07-10
"""

#extracting a multiple file 
def ExtractDFLargeNumberodFile(FilePath):
    path,dirs,files = next(os.walk(FilePath))
    FileCount = len(files)
    ListofDataFrame = []

    for i in range(FileCount):
        TempDF = pd.read_csv(FilePath+files[i])
        ListofDataFrame.append(TempDF)

    df = pd.concat(ListofDataFrame)
    return df
    print('File is Sucessfully Loaded Into DataFrame')

def CalculateAge(dob):
    dob = datetime.strptime(dob,"%Y-%m-%d").date()
    today = date.today()
    return today.year-dob.year - ((today.month,today.day) >(dob.month,dob.day))
 

def DataCleaning(df):
    #Check primary key if it is null then delete it
    df.dropna(how ='any',axis = 0,inplace = True)

    
    #check null value in salary column and replace with median value of salary column 
    meanvalue  = df[df['salary'].notnull()]
    medianvalue = np.median(meanvalue['salary'])
    if pd.isnull(df['salary']).any():
        df['salary'].fillna(medianvalue,inplace=True)
    
    #Check a null value in dob column and replace null value with max occurance value 
    res = {i:list(df['dob']).count(i) for i in list(df['dob'])}
    maxoccurencedob = max(res,key=res.get)
    if pd.isnull(df['dob']).any():
        df['dob'].fillna(maxoccurencedob,inplace=True)
    
    df['age'] = df['dob'].apply(CalculateAge)
    df['tax'] = (df['salary'] * 8) /100
    df['salary'] = df['salary'] - df['tax']

#Convert a id,salary and tax column from float to int 
    if df['id'].dtypes == float:
        df = df.astype({'id':int})

    if df['salary'].dtypes == float:
        df = df.astype({'salary':int})
    if df['tax'].dtypes == float:
        df = df.astype({'tax':int})

    print(df)

if __name__== "__main__":
    FilePath = input('Enter a File Path : ')
    print('This is a data Frame')
    df = ExtractDFLargeNumberodFile(FilePath)
    DataCleaning(df)

    #print(df)
    



