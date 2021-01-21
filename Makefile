NEO4J_INSTANCE=demo

help:
	@echo make start
	@echo make stop
	@echo make create_db
	@echo make delete_db
	@echo make clean
	@echo make clean-docker-run
	@echo make shell
	@echo make notebook
	@echo ""
	@echo make install
	@echo make test
	@echo make run

# install:
# pip3 install -r requirements.txt

start:
	docker start $(NEO4J_INSTANCE)

stop:
	docker stop $(NEO4J_INSTANCE)

create_db:
	python3 create_db.py

create_db2:
	python3 create_db2.py	

get_counts:
	python3 get_counts.py

delete_db:
	python3 delete_db.py

delete_db2:
	python3 delete_db2.py

lint:
	flake8 get_counts.py

format:
	black get_counts.py

run:
	# python3 get_counts.py
	python3 run_gdsl.py

clean-neo4j-plugins:
	rm ./*.jar
	rm ./*.zip

clean-docker-run:
	sudo rm -fr ~/neo4j/*

shell:
	docker exec -it demo bash

notebook:
	jupyter notebook

SRC_ROOT=src
TEST_ROOT=tests
SRC = $(SRC_ROOT)/foo/foo.py
#	$(SRC_ROOT)/eroads/helper.py

TEST = $(TEST_ROOT)/foo/test_foo.py
#	$(TEST_ROOT)/eroads/test_gdsl.py

install:
	pip3 install -e $(SRC_ROOT)

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-cache:
	rm -fr __pycache__

clean-log:
	rm -fr *.log

clean: clean-pyc clean-build clean-cache clean-log

test: clean install
	PYTHONPATH=$(SRC_DIR)
	@echo $(PYTHONPATH); pytest $(TEST)
