PYTHONCC=python3
PIPCC=pip3
SRCDIR=./src
DATADIR= ./data
DATAFILE= test.csv
demo: install preprocess plot

install:
	$(PIPCC) install --user -r requirements.txt

preprocess:
	cd $(SRCDIR); $(PYTHONCC) preprocess.py --filename=$(DATAFILE) --sourcedatadir=$(DATADIR); cd ..

plot:
	cd $(SRCDIR); $(PYTHONCC) server.py --sourcedatadir=$(DATADIR); cd ..
