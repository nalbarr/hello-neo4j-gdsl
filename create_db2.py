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
CALL gds.graph.create(
  'retail_graph',
  {
    Item: {
      label: 'Item',
      properties: {
        price: {
          property: 'Price',
          defaultValue: 0.0
        },
        StockCode: {
         property: 'StockCode',
         defaultValue: 0
       }
     }
    },
    Transaction: {
      label: 'Transaction',
      properties: {
       EpochTime:{
       	property:'EpochTime',
        defaultValue:0
       },
       TransactionID:{
       	property:'is_item',
        defaultValue:0
       }
     }
    }

 
 }, {
    
    CONTAINS: {
      type: 'CONTAINS',
      orientation: 'UNDIRECTED'
    }
})
            """
            )
            print('database created.')
        except ClientError as ex:
            print(ex)


def main():
    create_db()


if __name__ == "__main__":
    main()

