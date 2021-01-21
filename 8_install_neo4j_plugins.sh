#!/bin/bash

SRC1=apoc-4.1.0.2-all.jar
#SRC1=apoc-4.3.0-rc01-all.jar
SRC2=neo4j-graph-data-science-1.4.0-standalone.jar

TARGET=$NEO4J_HOME/plugins

echo overlay neo4j plugin 
echo   $SRC1 to $TARGET
sudo cp ./$SRC1 $TARGET
echo overlay neo4j plugin 
echo   $SRC2 to $TARGET

sudo cp ./$SRC2 $TARGET

echo installed neo4j plugins:
ls $TARGET

