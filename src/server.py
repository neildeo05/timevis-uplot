#! /usr/bin/env python3.7
import sys
from flask import Flask, request
from flask_cors import CORS
import json
app = Flask(__name__)
CORS(app)
import os
import subprocess
import csv
import time
import numpy as np
import pandas as pd
import io
import base64
datadir = None
def dict_get(dictionary, val ):
    try:
        return dictionary[val]
    except:
        return None

def csv_read(fp, delim='\n'):
    full_data = pd.read_csv(fp, delim, quoting=csv.QUOTE_NONE)
    full_data = full_data.to_numpy().astype('int32').flatten()
    return full_data

def csv_read_inefficient(fp, delim='\n'):
    tmp = []
    with open(fp, 'r') as f:
        reader = csv.reader(f, delimiter='\n')
        for line in reader:
            tmp.append(int(line[0]))
    return tmp[1:]
G_MAX_VALUE = 1_000_000
def find_level(l, h, max):
    delta = (h-l) + 1
    count = 0
    while(delta > max):
        h //= 2
        l //= 2
        delta = (h - l) + 1
        count+=1
    if count == 0:
        return (0, l, h)
    return (count-1, l, h)


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


            
def get_all_anomalous_points(data_source):
    global datadir
    points = []
    with open('./data/%s/anomalous_points.csv' % datadir, 'r') as f:
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
    global datadir
    request_json = json.loads(request.data.decode('utf-8'))
    # plot_type = dict_get(request_json, 'plot_type')
    plot_type = datadir
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

def read_separated(datadir, level_tmp, low_scaled, high_scaled):
    lows = []
    highs = []
    tmp = []
    with open("./data/%s/level_%02d.csv" % (datadir, level_tmp), 'r') as r:
        reader = csv.reader(r, delimiter=',')
        for i, line in enumerate(reader):
            if i < low_scaled:
                continue
            elif i > high_scaled:
                break
            else:
                if i % 2 == 0:
                    lows.append(int(line[0]))
                else:
                    highs.append(int(line[0]))
        tmp.append(lows)
        tmp.append(highs)
    return tmp
        
def query_range(l, h):
    global datadir
    low, high = l, h
   # Centering on a specific level:
   # between 2 million and 3 million timeticks
   # necessary data should be encapsulated from [2 million / (level+1), 3 million/(level+1)]
    # coarsest_data_bounds = (low // (2 ** 7),  high // (2 ** 7)) # Should bet the data range at the highest level
    # coarsest_data_range = int(coarsest_data_bounds[1] - coarsest_data_bounds[0]);
    # level = 0
    level = 0 # If the range is 1_000_000, then you go down by one level. If the range is 500_000 then you go down by 2 levels. If the range is 250,000
    # TODO: Populate this depending on a larger set of levels (maybe for very very large series >1B)
    raw_level = int(5_000_000 // int(high - low)) 
    #TODO:  refactor
    level_tmp = 6 - (raw_level if raw_level <= 6 else 6)
    if level_tmp == 6:
        level_tmp = 5
    level_scaled = 2 ** level_tmp
    low_scaled = low//level_scaled
    high_scaled = high//level_scaled
    print(low_scaled, high_scaled)
    tmp = read_separated(datadir, level_tmp, low_scaled, high_scaled)
    return tmp, level_tmp, low_scaled, high_scaled

@app.route('/getRange', methods=['POST'])
def get_range():
    global G_MAX_VALUE, datadir
    request_json = json.loads(request.data.decode('utf-8'))
    # plot_type = dict_get(request_json, 'plot_type')
    plot_type = datadir
    max_x_values = int(dict_get(request_json, 'max_x_values'))
    range_min = int(dict_get(request_json, 'range_min'))
    range_max = int(dict_get(request_json, 'range_max'))
    
    result = query_range(range_min, range_max);
    level = result[1]
    tmp = []
    for i in range(result[-2], result[-1], 2):
        tmp.append(2 ** level * (i))

    return json.dumps({
        "data": [tmp,result[0][1], result[0][0]],
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
    global G_MAX_VALUE, datadir
    request_json = json.loads(request.data.decode('utf-8'))
    # plot_type = dict_get(request_json, 'plot_type')
    plot_type = datadir
    max_x_values = int(dict_get(request_json, 'max_x_values'))
    level_raw = dict_get(request_json, 'level')
    level = 0 if not level_raw else int(level_raw)
    num_chunks = 0
    #TODO: xs should be 1/2 scaled (two y values for 1 x value)
    # scale_fun = lambda x: (2 ** level) * x
    # xs = scale_fun(np.indices(ys.shape))
    tmp = []
    lows = []
    highs = []
    ys = csv_read("./data/%s/level_%02d.csv" % (plot_type, level))[:G_MAX_VALUE]
    for i,j in enumerate(ys.tolist()):
        if i % 2 == 0:
            lows.append(j)
        else:
            highs.append(j)
    tmp.append(lows)
    tmp.append(highs)
    xs = []
    for i in range(0, ys.shape[0], 2):
        xs.append(2 ** level * (i))
    dat = [xs, tmp[0], tmp[1]]
    len_of_vals=len(dat[0])
    num_levels = find_level(0, max_x_values, G_MAX_VALUE)[0] + 1
    num_chunks = (max_x_values // G_MAX_VALUE) // (level+1)
    if level == 4:
        num_chunks -= 1
    print("BC", max_x_values, len_of_vals, num_chunks)
    if(level == num_levels):
        return json.dumps(
            {
                "num_levels" : num_levels,
                "level":level,
                "data": dat,
                "num_chunks": num_chunks - 1,
                "apoints" : get_all_anomalous_points(plot_type)
            }
        )
    else:
        return json.dumps(
            {
                "num_levels" : num_levels,
                "level":level,
                "data": dat,
                "num_chunks": num_chunks - 1,
                "apoints" : get_anomalous_points_for_chunk(0, plot_type)
            }
        )

@app.route('/getAllDataForChunk', methods=['POST'])
def get_all_data_for_chunk():
    global G_MAX_VALUE, datadir
    request_json = json.loads(request.data.decode('utf-8'))
    # plot_type = dict_get(request_json, 'plot_type')
    plot_type = datadir
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
    global datadir
    request_json = json.loads(request.data.decode('utf-8'))
    # plot_type = dict_get(request_json, 'plot_type')
    plot_type = datadir
    anom_dat = dict_get(request_json, 'anom_dat')
    print(anom_dat);
    with open("./data/%s/user_labelled_anomalous_points.csv" % plot_type, 'w') as f:
        wp = csv.writer(f, delimiter='\n');
        wp.writerows(anom_dat)
    return json.dumps({"status": "SUCCESS"})
def run(dd):
    global datadir
    datadir = dd
    app.run(host='0.0.0.0', port=8000)
