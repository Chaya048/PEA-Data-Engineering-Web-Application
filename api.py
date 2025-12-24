# Web API => http://localhost:5000
import os
import pandas as pd
from flask import Flask
import json

folder_path = "D:\LE408\Fullstack\Small LCL Data"

# list all files in the folder
file_list = []
for file in os.listdir(folder_path):
    if file.endswith(".csv"):
        file_list.append(file)
        
# create a flask app
app = Flask(__name__)

@app.route('/api/files', methods=['GET'])
def get_files():
    return json.dumps(file_list)

@app.route('/api/data/<filename>', methods=['GET'])
def get_meters(filename):
    file_path = os.path.join(folder_path, filename)
    df = pd.read_csv(file_path)
    meters = df.LCLid.unique().tolist()
    return json.dumps(meters)

@app.route('/api/data/<filename>/<meterID>', methods=['GET'])
def get_meter_data(filename, meterID):
    file_path = os.path.join(folder_path, filename)
    df = pd.read_csv(file_path)
    # create a list of dictionaries
    meter_data = {
        'ID': meterID,
        'DateTime': [],
        'kwh': []
    }
    # use exact column name including trailing space
    meter_data['DateTime'] = df.loc[df.LCLid == meterID, 'DateTime'].tolist()
    meter_data['kwh'] = df.loc[df.LCLid == meterID, 'KWH/hh (per half hour) '].tolist()
    meter_data['kwh'] = [0 if kwh == 'Null' else float(kwh) for kwh in meter_data['kwh']]
    return json.dumps(meter_data)

    