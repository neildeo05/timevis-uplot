$(SRCDIR)=./src
install:
	pip install -r requirements.txt

preprocess:
	cd $(SRCDIR); python preprocess.py; cd ..

build:
	python server.py
