#! /usr/bin/env python
from flask import Flask, request
from flask_cors import CORS
import json
app = Flask(__name__)
CORS(app)
import os
import subprocess
import sys
import csv
import time
import numpy as np
import pandas as pd
import io
import base64
def dict_get(dictionary, val ):
    try:
        return dictionary[val]
    except:
        return None

def csv_read(fp, delim='\n'):
    full_data = pd.read_csv(fp, delim)
    full_data = full_data.to_numpy().astype('int32').flatten()
    return full_data

def csv_read_inefficient(fp, delim='\n'):
    tmp = []
    with open(fp, 'r') as f:
        reader = csv.reader(f, delimiter='\n')
        for line in reader:
            tmp.append(int(line[0]))
    return tmp[1:]

def find_level(l, h, max):
    delta = (h-l) + 1
    count = 0
    while(delta > max):
        h //= 2
        l //= 2
        delta = (h - l) + 1
        count+=1
    return (count-1, l, h)
G_MAX_VALUE = 700000

def get_anomalous_points_for_chunk(chunk, dataset):
    global G_MAX_VALUE
    points = []
    if chunk == 0:
        data_range = (0, G_MAX_VALUE)
    else:
        data_range = ((chunk * G_MAX_VALUE) - G_MAX_VALUE, (chunk * G_MAX_VALUE))
    
    xs = []
    ys = []
    with open('./data/%s/anomalous_points.csv' % dataset, 'r') as f:
        a = csv.reader(f, delimiter='\n');
        for row in a:
            dat = row[0].split(',')
            tmp = int(dat[0])
            if(tmp >= data_range[0] and tmp <= data_range[1]):
                v = (list(map(int, dat)))
                xs.append(v[0])
                ys.append(v[1])
                          
    return [xs, ys]

def query_range(l, h):
    level, low, high = find_level(l, h)
    tmp = []
    with open("./data/rat_unhealthy_all_levels/level_%02d.csv" % level, 'r') as r:
        reader = csv.reader(r, delimiter=',')
        for i, line in enumerate(reader):
            if i < low:
                continue
            elif i > high:
                break
            else:
                tmp.append(int(line[0]))
        return tmp, level

            
def get_all_anomalous_points(data_source):
    points = []
    with open('./data/%s/anomalous_points.csv' % data_source, 'r') as f:
        a = csv.reader(f, delimiter='\n');
        xs = []
        ys = []
        for i in a:

            v = list(map(int, i[0].split(',')))
            xs.append(v[0])
            ys.append(v[1])
    return [xs, ys]

@app.route('/getAnomalousZoom', methods=['POST'])
def get_anomalous_zoom():
    global G_MAX_VALUE;
    request_json = json.loads(request.data.decode('utf-8'))
    plot_type = dict_get(request_json, 'plot_type')
    anomalous_point = dict_get(request_json, 'anomalous_point')
    radius = dict_get(request_json, 'radius')
    xs = []
    ys = []
    with open('./data/%s/anomalous_points.csv' % plot_type, 'r') as f:
        a = csv.reader(f, delimiter='\n');
        for i in a:
            v = list(map(int, i[0].split(',')))
            xs.append(v[0])
            ys.append(v[1])
    idx = xs[ys.index(anomalous_point)]
    minidx = idx - int(radius)
    maxidx = idx + int(radius)
    xs = []
    ys = []
    with open("./data/%s/level_00.csv" % plot_type,'r') as f:
        for i,j in enumerate(f):
            if i >= minidx and i <= maxidx:
                xs.append(i)
                ys.append(int(j.strip()))
    anom_data = [0] * (radius * 2)
    anom_data[radius] = anomalous_point;
    return json.dumps({"data": [xs, ys], "anom_data": anom_data})
    
        
    
@app.route('/getRange', methods=['POST'])
def get_range():
    global G_MAX_VALUE
    request_json = json.loads(request.data.decode('utf-8'))
    plot_type = dict_get(request_json, 'plot_type')
    max_x_values = int(dict_get(request_json, 'max_x_values'))
    range_min = int(dict_get(request_json, 'range_min'))
    range_max = int(dict_get(request_json, 'range_max'))
    result = query_range(range_min, range_max);
    return json.dumps({
        "data": result[0],
        "level": result[1]
    })
    

#TODO: find a better way to do this cause this is bad code
def gen_indices(shape, scale_fun=None):
    t = [None] * shape[0]
    counter = 0
    for i in range(0, len(t)-2, 2):
        t[i] = scale_fun(counter)
        t[i+1] = t[i]
        counter+=1
    return np.array(t[:-1])


@app.route('/getAllData', methods=['POST'])
def get_all_data():
    global G_MAX_VALUE
    request_json = json.loads(request.data.decode('utf-8'))
    plot_type = dict_get(request_json, 'plot_type')
    max_x_values = int(dict_get(request_json, 'max_x_values'))
    level_raw = dict_get(request_json, 'level')
    level = 0 if not level_raw else int(level_raw)
    num_chunks = 0
    #TODO: xs should be 1/2 scaled (two y values for 1 x value)
    # scale_fun = lambda x: (2 ** level) * x
    # xs = scale_fun(np.indices(ys.shape))
    tmp = []
    ys = csv_read("./data/%s/level_%02d.csv" % (plot_type, level))[:G_MAX_VALUE]
    for i in range(ys.shape[0]):
        tmp.append(2 ** level * (i))
    xs = np.array(tmp)
    dat = [xs.tolist(), ys.tolist()]
    num_levels = find_level(0, max_x_values, G_MAX_VALUE)[0] + 1
    for i in range(0, max_x_values // (2 ** level), G_MAX_VALUE):
        num_chunks += 1
    if(level == num_levels):
        return json.dumps(
            {
                "num_levels" : num_levels,
                "level":level,
                "data": dat,
                "num_chunks": num_chunks-1,
                "apoints" : get_all_anomalous_points(plot_type)
            }
        )
    else:
        return json.dumps(
            {
                "num_levels" : num_levels,
                "level":level,
                "data": dat,
                "num_chunks": num_chunks-1,
                "apoints" : get_anomalous_points_for_chunk(0, plot_type)
            }
        )

@app.route('/getAllDataForChunk', methods=['POST'])
def get_all_data_for_chunk():
    global G_MAX_VALUE
    request_json = json.loads(request.data.decode('utf-8'))
    plot_type = dict_get(request_json, 'plot_type')
    max_x_values = dict_get(request_json, 'max_x_values')
    chunk_number = dict_get(request_json, 'chunk_number')
    level = dict_get(request_json, 'level')
    num_chunks = 0
    for i in range(0, max_x_values // (2 ** level), G_MAX_VALUE):
        num_chunks += 1
    assert chunk_number < num_chunks
    data_min = G_MAX_VALUE * chunk_number
    data_max = (G_MAX_VALUE * chunk_number) + G_MAX_VALUE
    ys = csv_read("./data/%s/level_%02d.csv" % (plot_type, level))[data_min:data_max]
    tmp = []
    print(data_min, data_min + ys.shape[0])
    for i in range(data_min, data_min + ys.shape[0]):
        tmp.append((2 ** level) * i)
    xs = np.array(tmp)
    print(xs)
    start = time.time()
    dat = [xs.tolist(), ys.tolist()]
    end = time.time()
    print(end - start)
    return json.dumps({"data": dat})
    
@app.route('/setLabelledAnomalousPoints', methods=['POST'])
def setLabelledAnomalousPoints():
    request_json = json.loads(request.data.decode('utf-8'))
    plot_type = dict_get(request_json, 'plot_type')
    anom_dat = dict_get(request_json, 'anom_dat')
    print(anom_dat);
    with open("./data/%s/user_labelled_anomalous_points.csv" % plot_type, 'w') as f:
        wp = csv.writer(f, delimiter='\n');
        wp.writerows(anom_dat)
    return json.dumps({"status": "SUCCESS"})
if __name__ == "__main__":
    url = "./templates/index.html"
    subprocess.call(['open', url])
    app.run(port=8000, debug=True)
