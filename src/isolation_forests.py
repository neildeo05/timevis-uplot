import pandas as pd
import numpy as np
import csv
def val(data):
    mini = min(data)
    maxi = max(data)
    return (maxi-mini)*np.random.random()+mini
# [40]
def split(data, sv):
    lower_value = []
    higher_value = []
    for i in data:
        if i <= sv:
            lower_value.append(i)
        else:
            higher_value.append(i)
    return lower_value, higher_value

def classify_data(data):
    # remove duplicates
    if(len(data) == 0):
        return 0
    unique_classes, counts_unique_classes = np.unique(data, return_counts=True)
    # get max value - the max value is the index of the value that occurs the most in the data
    index = counts_unique_classes.argmax()
    # return the value that occurs the most in the dataset
    return unique_classes[index]

def isolation_tree(data,counter=0, max_depth=4):
    if (counter >= max_depth) or len(data)<=1:
        classification = classify_data(data)
        return classification
    else:
        counter +=1
        split_value = val(data)
        data_below, data_above = split(data,split_value)
        q = str(split_value)
        sub_tree = {q: []}
        below_answer = isolation_tree(data_below, counter,max_depth=max_depth)
        above_answer = isolation_tree(data_above, counter,max_depth=max_depth)
        if below_answer == above_answer:
            sub_tree = below_answer
        else:
            sub_tree[q].append(below_answer)
            sub_tree[q].append(above_answer)
        return sub_tree

def isolation_forest(df,n_trees=5, max_depth=5, subspace=256):
    forest = []
    for i in range(n_trees):
        tree = isolation_tree(df,max_depth=max_depth)
        forest.append(tree)
    return forest

def pathLength(example,iTree,path=0,trace=False):
    #increment path length for each recursive call
    path=path+1
    question = list(iTree.keys())[0]
    if example <= float(question):
        answer = iTree[question][0]
    else:
        answer = iTree[question][1]
    # base case
    if not isinstance(answer, dict):
        return path
    
    # recursive part
    else:
        residual_tree = answer
        return pathLength(example, residual_tree,path=path)

    return path

def evaluate_instance(instance,forest):
    paths = []
    for tree in forest:
        paths.append(pathLength(instance,tree))
    return paths

def find_anomalies(filepath, num_anomalies, print_anomalies=False):
    df = []
    with open(filepath, 'r') as t:
        reader = csv.reader(t, delimiter='\n')
        for i in reader:
            df.append(int(i[0]))
    iso = isolation_forest(df)
    vals = {}
    for i in df:
        val = np.mean((evaluate_instance(i, iso)))
        vals[val] = i
    if print_anomalies:
        print(vals)
    if len(vals) < num_anomalies:
        t = (sorted(list(vals.keys())))
        return [vals[t[i]] for i in range(len(vals))]
    else:
        t = (sorted(list(vals.keys())))
        return [vals[t[i]] for i in range(num_anomalies)]
 
if __name__ == '__main__':
    print(find_anomalies("../source_datafiles/top500.csv", 2))
