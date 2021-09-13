# -*- coding: utf-8 -*-
import pandas as pd
import json

def return_json(names):
    df = pd.read_excel('D:/Exercises/DAAI-API/sample_data/sample_excel.xlsx')
    
    json_obj = []
    for name in names:
        json_data = json.loads(df.loc[df['DB_name'] == name].to_json(orient="index"))
        json_obj.append(json_data)
        
    return(json_obj)

if __name__ == "__main__":
    
    names = ['Sathish kumar','Peter Johns','Peter3 Johns']
    json_result = return_json(names)
    
    print(json_result)
