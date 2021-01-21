#!/bin/bash 

APOC_URL=https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/4.1.0.2/apoc-4.1.0.2-all.jar
GDSL_URL=https://s3-eu-west-1.amazonaws.com/com.neo4j.graphalgorithms.dist/graph-data-science/neo4j-graph-data-science-1.4.0-standalone.zip
# APOC_URL=https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/tag/4.3.0-rc01/apoc-4.3.0-rc01-all.jar
# GDSL_URL=https://s3-eu-west-1.amazonaws.com/com.neo4j.graphalgorithms.dist/graph-data-science/neo4j-graph-data-science-1.4.0-standalone.zip
GDSL_FILE=neo4j-graph-data-science-1.4.0-standalone.zip

wget $APOC_URL
wget $GDSL_URL

unzip ./$GDSL_FILE
rm ./$GDSL_FILE
