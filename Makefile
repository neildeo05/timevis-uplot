PYTHONCC=python3
PIPCC=pip3
SRCDIR=./src
DATADIR= ./data
DATAFILE= test.csv

all: preprocess plot clean

plot:
	cd $(SRCDIR); $(PYTHONCC) server.py --sourcedatadir=$(DATADIR); cd ..

preprocess:
	cd $(SRCDIR); $(PYTHONCC) preprocess.py --filename=$(DATAFILE) --sourcedatadir=$(DATADIR); cd ..

install:
	$(PIPCC) install --user -r requirements.txt

clean:
	cd $(DATADIR); rm -rf test_all_levels
