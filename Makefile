install:
	pip install -r requirements.txt

preprocess:
	cd src; python preprocess.py; cd ..


build: server.py
	./server.py
