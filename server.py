from flask import Flask, request
from flask_cors import CORS
import json
app = Flask(__name__)
CORS(app)
import os
import sys
import csv

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
    for i in range(0, max_x_values // (2 ** level), G_MAX_VALUE):
        num_chunks += 1

    with open (("./data/%s/level_%02d.csv" % (plot_type, level)), 'r') as f:
        for i,j in enumerate(f):
            if(i >= G_MAX_VALUE):
                break
            ys.append(int(j.strip()))
            xs.append((2 ** level) * i)
    dat = [xs,ys]
    print(len(xs))
    num_levels = find_level(0, max_x_values, G_MAX_VALUE)[0] + 1
    print(level, num_levels);
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
    read_mode = False
    dat = []
    xs = []
    test = []
    with open("./data/%s/level_%02d.csv" % (plot_type,level), 'r') as f:
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
    app.run(port=8000)
