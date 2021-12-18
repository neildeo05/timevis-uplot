PYTHONCC=python3
PIPCC=pip3
SRCDIR=./src
DATADIR= ./data
DATAFILE= test.csv

all: clean preprocess plot

plot: 
	cd $(SRCDIR); $(PYTHONCC) server.py --sourcedatadir=$(DATADIR); cd ..

preprocess:
	cd $(SRCDIR); $(PYTHONCC) preprocess.py --filename=$(DATAFILE) --sourcedatadir=$(DATADIR); cd ..;
	cd $(DATADIR); cd test_all_levels; touch anomalous_points.csv;

install:
	$(PIPCC) install --user -r requirements.txt

clean:
	cd $(DATADIR); rm -rf test_all_levels
