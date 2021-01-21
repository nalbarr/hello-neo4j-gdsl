from neo4j import GraphDatabase
from neo4j.exceptions import ClientError
import os
import altair

bolt_url = os.getenv("NEO4J_BOLT_URL", "bolt://localhost")
user = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "neo4j123")
driver = GraphDatabase.driver("bolt://localhost", auth=(user, password))


def get_place_count():
    with driver.session() as session:
        try:
            results = session.run(
                """
                MATCH (p:Place)
                RETURN COUNT(p)
                AS count
                """
            )
            count_list = [record["count"] for record in results]
            count = count_list[0]
            print('count(Place): {}'.format(count))
            # assert count == 894
        except ClientError as ex:
            print(ex)


def get_eroad_count():
    with driver.session() as session:
        try:
            results = session.run(
                """
                MATCH (p:Place)-[r:EROAD]-(p2:Place)
                RETURN COUNT(r)
                AS count
                """
            )
            count_list = [record["count"] for record in results]
            count = str(count_list[0])
            print('count(EROAD): ' + count)
            print('count(Place): {}'.format(count))
        except ClientError as ex:
            print(ex)


def main():
    get_place_count()
    get_eroad_count()


if __name__ == "__main__":
    main()
