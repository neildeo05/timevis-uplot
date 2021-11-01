PYTHONCC=python3
PIPCC=pip3
SRCDIR=./src
DATADIR= ./data
DATAFILE= test.csv

all: install preprocess plot
plot:
	cd $(SRCDIR); $(PYTHONCC) server.py --sourcedatadir=$(DATADIR); cd ..

preprocess:
	cd $(SRCDIR); $(PYTHONCC) preprocess.py --filename=$(DATAFILE) --sourcedatadir=$(DATADIR); cd ..

install:
	$(PIPCC) install --user -r requirements.txt
