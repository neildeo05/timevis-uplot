SRCDIR=./src
demo: install preprocess plot
install:
	pip install -r requirements.txt;\

preprocess:
	cd $(SRCDIR); python preprocess.py; cd ..

plot:
	python server.py
