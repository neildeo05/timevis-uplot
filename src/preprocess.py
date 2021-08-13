import csv
import backend
import os
from confparser import parse, setopt
import sys
from datetime import datetime
from tqdm import trange
import os.path
arg = parse('COMPRESS_MODE')
fullpath_for_data = parse("SOURCE_FILE").split('.')[0] + "_" + arg + "_levels"

if arg == 'all':
    arg = backend.Decompress_Arg.ALL
elif arg == 'min':
    arg = backend.Decompress_Arg.MIN
else:
    arg = backend.Decompress_Arg.MAX

def read_csv(filename):
    # Open file as IO object
    with open(filename, 'r') as csv_file:
        # Initialize csv_reader with the IO object of the file passed in as a parameter
        csv_reader = csv.reader(csv_file, delimiter = '\n')
        # The csv_reader is iterable, so list(csv_reader) turns the data of the file into a list and returns it.
        # In order to return a list of ints, the items in the list have to be converted to ints, so map(int, list) does that
        # return list(map(int, list(csv_reader)))
        return list(map(lambda x: int(x[0]), list(csv_reader)))

def build_tree(data):
    # This function converts the raw_data (of type list) into a hierarchy (tree/graph)
    return backend.query_select_data(data)

def write(root, levels):
    tmp = root
    basename = "level_%02d.csv"
    for i in trange(levels+2, desc = "Level:"):
        with open(basename % i, 'w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter = ',')
            csv_writer.writerows(backend.convert_node_array_to_list(tmp.layer,arg))
        tmp = tmp.next


if __name__ == "__main__":
    filename = "../" + parse("SOURCE_DIR") + "/" + parse("SOURCE_FILE")
    raw_data = read_csv(filename)
    print("READ FILE %s" % filename)
    os.chdir("../data")
    if not os.path.isdir(fullpath_for_data):
        os.mkdir(fullpath_for_data)
        
    os.chdir(fullpath_for_data)
    print(os.getcwd())

    root = build_tree(raw_data)
    write(*root)
    os.chdir("../../src")
