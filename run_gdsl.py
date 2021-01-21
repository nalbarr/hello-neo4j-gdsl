from neo4j import GraphDatabase
from neo4j.exceptions import ClientError
import os
from sklearn.manifold import TSNE
import numpy as np
import altair as alt
import pandas as pd

# NAA
# - https://neo4j.com/developer/graph-data-science/applied-graph-embeddings/

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

# NAA
# - https://github.com/neo4j/graph-data-science/releases
# - rename embeddingSize to embeddingDimension
def call_node2vec():
    print('*** call_node2vec().')
    with driver.session() as session:
        try:
            results = session.run(
               """
CALL gds.alpha.node2vec.stream({
  nodeProjection: "Place",
  relationshipProjection: {
    eroad: {
      type: "EROAD",
      orientation: "UNDIRECTED"
    }
  },
  embeddingDimension: 10,
  iterations: 10,
  walkLength: 10
})
YIELD nodeId, embedding
RETURN gds.util.asNode(nodeId).name AS place, embedding
LIMIT 5;
              """
            )
            place_list = [record["place"] for record in results]
            for i,place in enumerate(place_list):
                print('place[{}]: {}'.format(i, place))
            embed_list = [record["embedding"] for record in results]
            for i,embed in enumerate(embed_list):
                print('embedding[{}]: {}'.format(i, embed))
        except ClientError as ex:
            print(ex)

# NAA
# - https://github.com/neo4j/graph-data-science/releases
# - rename embeddingSize to embeddingDimension
def write_node2vec():
    print('*** write_node2vec().')
    with driver.session() as session:
        try:
            results = session.run(
"""
CALL gds.alpha.node2vec.write({
   nodeProjection: "Place",
   relationshipProjection: {
     eroad: {
       type: "EROAD",
       orientation: "UNDIRECTED"
    }
   },
   embeddingDimension: 10,
   iterations: 10,
   walkLength: 10,
   writeProperty: "embeddingNode2vec"
   });
"""
            )
            #embed_list = [record["embedding"] for record in results]
            #for i,embed in enumerate(embed_list):
            #    print('embedding[{}]: {}'.format(i, embed))
            for record in results:
                print('record: {0}: '.format(record))            
        except ClientError as ex:
            print(ex)


def get_node2vec_embeddings():
    print('*** get_node2vec_embeddings().')
    with driver.session(database="neo4j") as session:
        try:
            results = session.run(
"""
MATCH (p:Place)-[:IN_COUNTRY]->(country)
WHERE country.code IN $countries
RETURN p.name AS place, p.embeddingNode2vec AS embedding, country.code AS country
"""
        , {"countries": ["E", "GB", "F", "TR", "I", "D", "GR"]}
            )

            # embed_list = [record["embedding"] for record in results]
            # for i,embed in enumerate(embed_list):
            #    print('embedding[{}]: {}'.format(i, embed))

            X = pd.DataFrame([dict(record) for record in results])
            print('X.head(): {0}'.format(X.head()))
            return X
        except ClientError as ex:
            print(ex)

def graph_node2vec(X):
    print('*** graph_node2vec().')    
    
    # NAA
    # - n_components=2 means visualize in 2 dimensions
    X_embedded = TSNE(n_components=2, random_state=6).fit_transform(list(X.embedding))

    places = X.place
    df = pd.DataFrame(data = {
        "place": places,
        "country": X.country,
        "x": [value[0] for value in X_embedded],
        "y": [value[1] for value in X_embedded]
    })
    print(df.head)
    alt.Chart(df).mark_circle(size=60).encode(
        x='x',
        y='y',
        color='country',
        tooltip=['place', 'country']
    ).properties(width=700, height=400)


def main():
    check_apoc()
    check_gds()
    call_node2vec()
    write_node2vec()
    X = get_node2vec_embeddings()
    graph_node2vec(X)


if __name__ == "__main__":
    main()
