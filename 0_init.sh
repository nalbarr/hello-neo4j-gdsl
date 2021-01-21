#!/bin/bash

make clean
# NAA.
# - ensure there is mount point available for 6_docker_run.sh
mkdir ~/neo4j
sudo apt-get install python3-venv
python3 -m venv venv
