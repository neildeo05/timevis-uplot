from io import TextIOWrapper
import os
import argparse
import time
import sys

parser = argparse.ArgumentParser() 
parser.add_argument('-d', "--decompress_arg", type=str, help='decompress argument for preprocessing', default='all')
parser.add_argument('-f', '--filename', type=str, help='filename for preprocessing', default='test.csv')
parser.add_argument('-s', '--sourcedatadir', type=str, help='source data dir for preprocessing', default='data')
args = parser.parse_args()
print(args.filename)
inputFilePath = args.filename
datadir = args.sourcedatadir
decomp_arg = args.decompress_arg
# TODO: Don't hardcode this
size = 100_000_000

tic = time.perf_counter()
topFourList = [None] * 4
total:int = 0
fourCounter:int = 0

if __name__ == "__main__":
    # TODO: This has to work based on the Data directory
    fullpath_for_data = args.filename.split('.')[0] + ("_preprocessed_levels")
    if not os.path.isdir(datadir):
        os.mkdir(datadir)
    os.chdir(datadir)
    if not os.path.isdir(fullpath_for_data):
        os.mkdir(fullpath_for_data)
    os.chdir(fullpath_for_data)

    #TODO: Work with the Data directory
    for i in range(7):
        basename = "level_%02d.csv"
        writeTo: TextIOWrapper = open(basename %i,'w')
        print("Creating %s"%(basename%i))
        with open ("../../" + inputFilePath if i == 0 else basename % (i-1), "r") as myFile:
            myNum = myFile.readline()
            while (myNum):  
                total += 1
                topFourList[fourCounter] = myNum
                fourCounter += 1
                if len(topFourList) == 4 and None not in topFourList:
                     minNum = min(topFourList)
                     maxNum = max(topFourList)
                     writeTo.writelines([minNum,maxNum])
                     fourCounter = 0
                     topFourList = [None] * 4
                if (total % 1_000_000 == 0):
                    print("reached: ", total)
                    toc = time.perf_counter()
                    print(f"Took {toc - tic:0.4f} seconds")
                myNum = myFile.readline()
        writeTo.close()


