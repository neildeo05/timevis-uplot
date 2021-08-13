import math
import random
from enum import Enum

import numpy as np


class Box_Type(Enum):
    LEFT = 1
    RIGHT = 2
    CENTER = 3


class Decompress_Arg(Enum):
    MIN = 1
    MAX = 2
    ALL = 3


class Node:
    def __init__(self, low, high):
        self.low = low
        self.high = high

    @staticmethod
    def init_node_array(data):
        ret = []
        for i in range(0, len(data)-1, 2):
            if data[i] < data[i+1]:
                ret.append(Node(data[i], data[i+1]))
            else:
                ret.append(Node(data[i+1], data[i]))
        return ret

    @staticmethod
    def node_array(data):
        ret = []
        for i in range(0, len(data) - 1, 2):
            tmp = [data[i].low, data[i].high, data[i+1].low, data[i+1].high]
            ret.append(Node(min(tmp), max(tmp)))
        return ret

    def __repr__(self):
        return "Node(" + str(self.low) + " " + str(self.high) + ")"


class Hierarchy:
    def __init__(self, layer, next):
        self.next = next
        self.layer = layer

    @staticmethod
    def build_hierarchy(data):
        combos = int(math.log(len(data), 2))
        root = Hierarchy(data, None)
        tmp = root
        for i in range(combos):
            tmp.next = Hierarchy(Node.node_array(tmp.layer), None)
            tmp = tmp.next
        return root

    def __repr__(self):
        for i in self.layer:
            print(i)
        return "" + str(len(self.layer))

    @staticmethod
    def print_h(root):
        tmp = root
        while(tmp):
            print(tmp)
            print()
            tmp = tmp.next


def num_bars(length):
    return int(math.log(length, 2)) - 1


def bar(root, barNumber):
    try:
        tmp = root
        for i in range(barNumber):
            tmp = tmp.next
        return tmp.layer
    except Exception as e:
        print("Bar number too high")
        quit()


def box(vals, box_size, box_type):
    if box_type == Box_Type.LEFT:
        return vals[0:box_size]
    elif box_type == Box_Type.RIGHT:
        return vals[-box_size:]
    elif box_type == Box_Type.CENTER:
        size = len(vals)
        disp = box_size//2
        return vals[size-disp-2:size+disp+2]


def decompress_node_array(data, Decomp_Arg):
    if Decomp_Arg == Decompress_Arg.ALL:
        vals = []
        for i in range(len(data) - 1):
            vals.append([i, data[i].low])
            vals.append([i, data[i].high])

        return np.array(vals)
    elif Decomp_Arg == Decompress_Arg.MIN:
        vals = np.zeros(len(data))
        for i, c in enumerate(data):
            vals[i] = c.low
        return (vals)
    elif Decomp_Arg == Decompress_Arg.MAX:
        vals = np.zeros(len(data))
        for i, c in enumerate(data):
            vals[i] = c.high
        return (vals)


def convert_node_array_to_list(data, Decomp_Arg):
    vals = []
    for i in range(len(data)):
        if Decomp_Arg == Decompress_Arg.MIN or Decomp_Arg == Decompress_Arg.ALL:
            vals.append([data[i].low])
        if Decomp_Arg == Decompress_Arg.MAX or Decomp_Arg == Decompress_Arg.ALL:
            vals.append([data[i].high])

    return vals

def query_select_data(data):
    data = Node.init_node_array(data)
    root = Hierarchy.build_hierarchy(data)
    # dat = bar(root, int(msg))
    return root, num_bars(len(data))

def closest_power(x):
    val = math.log(x, 2)
    if(val - int(val) > 0.5):
        return math.ceil(val)
    else:
        return math.floor(val)

def query_select_data_range(s, l, data, PAD_CONSTANT):
    # 2 ^ 10 = 1024
    # If we don't pad it, then we have to get the one below 1024, to fit in the 1024 box. Thus, we have to get the length of the data - 8 to get the 
    # bar that has data closest to 2 ^ 9
    if not PAD_CONSTANT:
        rng = data[s:l]
        data = Node.init_node_array(rng)
        root = Hierarchy.build_hierarchy(data)
        dat = bar(root, num_bars(len(data)) -8)
        return dat
    else:
        rng = data[s:l]
        val = 2 ** (closest_power(len(rng)) + 1) if 2 ** closest_power(len(rng)) < len(rng) else 2 ** closest_power(len(rng))
        val -= len(rng)
        rng += [0] * val
        data = Node.init_node_array(rng)
        root = Hierarchy.build_hierarchy(data)
        dat = bar(root, num_bars(len(data)) - 9)
        print(len(dat))
        return dat

