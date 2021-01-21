from neo4j import GraphDatabase
from neo4j.exceptions import ClientError
import os

bolt_url = os.getenv("NEO4J_BOLT_URL", "bolt://localhost")
user = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "neo4j123")
driver = GraphDatabase.driver("bolt://localhost", auth=(user, password))


def delete_db():
    with driver.session() as session:
        try:
            session.run("""
                MATCH (n)
                DETACH DELETE n
            """)
            print('database deleted.')
        except ClientError as ex:
            print(ex)


def main():
    delete_db()


if __name__ == '__main__':
    main()
