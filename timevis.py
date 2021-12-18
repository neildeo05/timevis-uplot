import sys
sys.path.append('./src/lib')
import os
import argparse
import subprocess
from os.path import exists
import src.server as server
import filecmp
parser = argparse.ArgumentParser()
parser.add_argument("--filename", type=str, help='CSV File that timevis will run on')
parser.add_argument('--force', type=str, help='[y/n] If true, the preprocessor will overwrite previously preprocessed files, otherwise. If false, the preprocessor will not run, and will immediately handoff to the plotter')
parser.add_argument('--install', type=str, help='[y/n] If true, all packages in requirements.txt will be installed, if necessary')


if len(sys.argv) < 3:
    parser.print_help()
    parser.exit(1)

args = parser.parse_args()

if args.install:
    if (filecmp.cmp('requirements.txt', 'installed_packages.txt')):
        print("already installed required packages... skipping step")
    else:
        try:
            subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
            subprocess.run(['cp', 'requirements.txt', 'installed_packages.txt'])
        except Exception as e:
            subprocess.run(['pip', 'install','-U', '-r', 'requirements.txt'])
            subprocess.run(['cp', 'requirements.txt', 'installed_packages.txt'])



if not exists(args.filename):
    print('ERROR: filename `%s` does not exist.' % args.filename)
    parser.print_help()
    parser.exit(1)



base_data_path =args.filename.split('.')[0] + "_preprocessed_levels"
data_path = './data/' + base_data_path

force = False
if args.force == 'y' or args.force == 'Y':
    force = True

if not exists(data_path) and not force:
    print('ERROR: directory `%s` does not exist, and force argument was False. Cannot create directory with force being false' % data_path)
    parser.print_help()
    parser.exit(1)


if not force:
    try:
        subprocess.run(['open', './templates/index.html'])
        print("+ python plot.py")
        server.run(base_data_path)
    except Exception as e:
        print("+ python plot.py")
        print("open this link in your browser: file://%s/templates/index.html" % os.getcwd())
        server.run(base_data_path)

else:
    print('+ python preprocess.py')
    subprocess.run(['python', './src/preprocess.py', '--filename=%s'%args.filename])
    subprocess.run(['touch', data_path + '/anomalous_points.csv'])
    try:
        subprocess.run(['open', './templates/index.html'])
        print("+ python plot.py")
        server.run(base_data_path)
    except Exception as e:
        print("+ python plot.py")
        print("open this link in your browser: file://%s/templates/index.html" % os.getcwd())
        server.run(base_data_path)
