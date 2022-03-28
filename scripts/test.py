from datetime import datetime
import json
import os


data = {'id':"12345"}
now = datetime.now()
year_dir = "./data/"+str(now.year)
if(os.path.exists(year_dir) == False):
    os.makedirs(year_dir)    
    
file = year_dir+"/id.json"
with open(file, 'w') as outfile:
    json.dump(data, outfile)

file = year_dir+"/month_"+str(now.month)+".json"
with open(file, 'w') as outfile:
    json.dump(data, outfile)

with open('./data/2022/id.json') as json_file:
    data = json.load(json_file)
    print(data.get("id"))
