from neo4j import GraphDatabase
from neo4j.exceptions import ClientError
import os
import altair

bolt_url = os.getenv("NEO4J_BOLT_URL", "bolt://localhost")
user = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "neo4j123")
driver = GraphDatabase.driver("bolt://localhost", auth=(user, password))


def create_db():
    with driver.session() as session:
        try:
            session.run(
            """
            CREATE CONSTRAINT ON (p:Place) ASSERT p.name IS UNIQUE;
            """
            )
            print('database created.')
        except ClientError as ex:
            print(ex)

        result = session.run(
            """
            USING PERIODIC COMMIT 1000
            LOAD CSV WITH HEADERS FROM "https://github.com/neo4j-examples/graph-embeddings/raw/main/data/roads.csv"
            AS row

            MERGE (origin:Place {name: row.origin_reference_place})
            MERGE (originCountry:Country {code: row.origin_country_code})

            MERGE (destination:Place {name: row.destination_reference_place})
            MERGE (destinationCountry:Country {code: row.destination_country_code})
            
            MERGE (origin)-[:IN_COUNTRY]->(originCountry)
            MERGE (destination)-[:IN_COUNTRY]->(destinationCountry)

            MERGE (origin)-[eroad:EROAD {number: row.road_number}]->(destination)
            SET eroad.distance = toInteger(row.distance), eroad.watercrossing = row.watercrossing;
        """
        )
        # display(result.consume().counters)


def main():
    create_db()


if __name__ == "__main__":
    main()

