from flask import Flask, request
from flask_cors import CORS
import json
app = Flask(__name__)
CORS(app)
import os
import sys
def dict_get(dictionary, val ):
    try:
        return dictionary[val]
    except:
        return None
    
def find_level(l, h, max):
    delta = (h-l) + 1
    count = 0
    while(delta > max):
        h //= 2
        l //= 2
        delta = (h - l) + 1
        count+=1
    return (count-1, l, h)
G_MAX_VALUE = 700_000


@app.route('/getAllData', methods=['POST'])
def get_all_data():
    global G_MAX_VALUE
    request_json = json.loads(request.data.decode('utf-8'))
    plot_type = dict_get(request_json, 'plot_type')
    max_x_values = int(dict_get(request_json, 'max_x_values'))
    level_raw = dict_get(request_json, 'level')
    level = 0 if not level_raw else int(level_raw)
    xs = []
    ys = []
    dat = []
    num_chunks = 0
    print(find_level(0, max_x_values, G_MAX_VALUE))
    for i in range(0, max_x_values, G_MAX_VALUE):
        num_chunks += 1
    with open ("./data/rats_all_levels/level_%02d.csv" % level, 'r') as f:
        for i,j in enumerate(f):
            if(i >= G_MAX_VALUE):
                break
            ys.append(int(j.strip()))
            xs.append((2 ** level) * i)
    dat = [xs,ys]
    return json.dumps({"num_levels" : find_level(0, max_x_values, G_MAX_VALUE)[0], "level":level, "data": dat, "num_chunks": num_chunks})


@app.route('/getAllDataForChunk', methods=['POST'])
def get_all_data_for_chunk():
    global G_MAX_VALUE
    request_json = json.loads(request.data.decode('utf-8'))
    plot_type = dict_get(request_json, 'plot_type')
    max_x_values = dict_get(request_json, 'max_x_values')
    chunk_number = dict_get(request_json, 'chunk_number')
    level = dict_get(request_json, 'level')
    num_chunks = 0
    for i in range(0, max_x_values, G_MAX_VALUE):
        num_chunks += 1
    assert chunk_number < num_chunks
    data_min = G_MAX_VALUE * chunk_number
    data_max = (G_MAX_VALUE * chunk_number) + G_MAX_VALUE
    read_mode = False
    dat = []
    xs = []
    test = []
    with open("./data/rats_all_levels/level_%02d.csv" % level, 'r') as f:
        for i,j in enumerate(f):
            if (i == data_min):
                read_mode = True
            if (i == data_max):
                read_mode = False
            if(read_mode):
                test.append(i)
                xs.append((2 ** level) * i)
                dat.append(int(j.strip()))
    returndata = [xs, dat]
    return json.dumps({"data": returndata})

if __name__ == "__main__":
    app.run(port=8000)
