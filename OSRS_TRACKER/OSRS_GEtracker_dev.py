import json
import pandas as pd

with open('data.json') as data_file:    
    json = json.load(data_file)

df = pd.DataFrame(json['items'])
print (df)