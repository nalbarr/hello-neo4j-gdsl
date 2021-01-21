#!/bin/bash

# NAA. Modify images to include plugins.
# - https://community.neo4j.com/t/install-plugins-in-dockerized-neo4j/13644/5
# - https://community.neo4j.com/t/neo4j-in-docker-plugins-are-not-recognized/10494/2
# - https://graphaware.com/neo4j/2020/04/26/graph-datascience-neo4j-4.html

#    --env NEO4J_dbms_security_procedures_unrestricted=gds.*,apoc.* \
#    --env NEO4J_dbms_security_procedures_whitelist=gds.*,apoc.* \
#    --env NEO4J_apoc_import_file_enabled=true \
#    --env NEO4J_dbms_shell_enabled=true \
#    --env NEO4JLABS_PLUGINS=["gds", "apoc"] \

docker run \
    --name demo \
    -p7474:7474 -p7687:7687 \
    -d \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/logs:/logs \
    -v $HOME/neo4j/import:/var/lib/neo4j/import \
    -v $HOME/neo4j/plugins:/plugins \
    --env NEO4J_AUTH=neo4j/neo4j123 \
    --env NEO4J_dbms_security_procedures_unrestricted=gds.*,apoc.* \
    --env NEO4J_dbms_security_procedures_whitelist=gds.*,apoc.* \
    neo4j:latest
