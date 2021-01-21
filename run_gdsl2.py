from neo4j import GraphDatabase
from neo4j.exceptions import ClientError
import os
import altair
from sklearn.manifold import TSNE
import numpy as np
import pandas as pd

# NAA
# - https://github.com/AliciaFrame/GDS_Retail_Demo

bolt_url = os.getenv("NEO4J_BOLT_URL", "bolt://localhost")
user = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "neo4j123")
driver = GraphDatabase.driver("bolt://localhost", auth=(user, password))


def check_apoc():
    with driver.session() as session:
        print('*** check_apoc().')
        try:
            results = session.run(
               """
CALL dbms.procedures() yield name
    where name starts with "apoc"
    return count(*) as count;
              """
            )
            count_list = [record["count"] for record in results]
            count = count_list[0]
            assert count > 0
            print('dbms.procedures() for apoc count: {0}'.format(count))
        except ClientError as ex:
            print(ex)


def check_gds():
    print('*** check_gds().')
    with driver.session() as session:
        try:
            results = session.run(
               """
CALL dbms.procedures() yield name
    where name starts with "gds"
    return count(*) as count;
              """
            )
            count_list = [record["count"] for record in results]
            count = count_list[0]
            assert count > 0
            print('dbms.procedures() for gds count: {0}'.format(count))
        except ClientError as ex:
            print(ex)


def main():
    # check_apoc()
    check_gds()


if __name__ == "__main__":
    main()
