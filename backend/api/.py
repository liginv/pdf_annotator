import pandas as pd
import json
#read the excel file
excel = pd.read_excel('Book.xlsx')

#simple way
for key in keys(excel):
    