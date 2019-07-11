import pandas as pd
import json
#read the excel file
excel = pd.read_excel('Book.xlsx')

def group_data():
    js = json.loads(json.loads(excel))
    keys = list(excel.keys())

    data = {}

