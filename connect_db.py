from neo4j import GraphDatabase
from neo4j.exceptions import ClientError
import os

bolt_url = os.getenv("NEO4J_BOLT_URL", "bolt://localhost")
user = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "neo4j123")
driver = GraphDatabase.driver("bolt://localhost", auth=(user, password))


def connect_db():
    with driver.session() as session:
        try:
            results = session.run(
            """
            CREATE (a:Greeting)
            SET a.message = 'Hello, Neo4j'
            RETURN a.message
            AS message
            """
            )
            result_list = [record['message'] for record in results]
            message = result_list[0]
            print('message: {0}'.format(message))
        except ClientError as ex:
            print(ex)

def main():
    connect_db()


if __name__ == "__main__":
    main()

