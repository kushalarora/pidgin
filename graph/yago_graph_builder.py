from SPARQLWrapper import SPARQLWrapper, JSON
from base_graph_builder import BaseGraphBuilder
import argparse
import logging
import json
import os
import re

class YagoGraphBuilder(BaseGraphBuilder):
    YAGO_BASE_URL = "http://yago-knowledge.org/resource/"
    def __init__(self, relations_file, sparql_endpoint, graph_file, noun_phrase_file):
        self.sparql_client = SPARQLWrapper(sparql_endpoint, returnFormat=JSON)
        self.relations_file = relations_file
        BaseGraphBuilder.__init__("YAGO", relation_file, graph_file, noun_phrase_file)


    def _canonicalize(self, value):
        return value.replace(YAGO_BASE_URL, "YAGO:")

    def _query_sparql(self,  query):
        response = None
        self.sparql_client.setQuery(query)
        try:
            response = json.loads(self.sparql_client.query().response.read())
        except:
            logging.error("Yago::Query Failed%s",query)
        return response


    def _query_entity_pair(self, relation):
        logging.info("Yago::Processing Relation '%s'" % relation)
        query = """
            PREFIX yago: <http://yago-knowledge.org/resource/>

        SELECT ?s ?o
        WHERE {
                ?s %s ?o .
        }
        """ % relation

        results = self._query_sparql(query)

        if not results:
            return
        entity_pairs = []
        for result in results["results"]["bindings"]:

            entity_pair = [self._canonicalize(result["s"]),
                                    self._canonicalize(result["o"])]
            # logging.info("Yago::Adding %s-(%s) edge" % (relation, entity_pair))
            entity_pairs.append(entity_pair)

        logging.info("Yago::Number Entity Pair: %d" % len(entity_pairs))
        return entity_pairs

    def _query_labels(self, entity):
        np_values = []
        query = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?o
            WHERE {
                     <%s> rdfs:label ?o .
            }
        """ % entity

        results = self._query_sparql(query)
        for result in results["results"]["bindings"]:
            np_values.append(result["o"]["value"])

        return np_values

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    FORMAT = '%(levelname)s %(asctime)s %(name)s: %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)

    parser.add_argument("-r", "--relations_file",
            type=str, help="File containing list of relation to be added to graph")

    parser.add_argument("-s", "--sparql",
            type=str, help="sparql url for data set")

    parser.add_argument("-g", "--graph_file",
            type=str, help="Graph file to write entity pair relation edge")

    parser.add_argument("-n", "--np_file",
            type=str, help="File to write noun phrase pair for entity pair")

    args = parser.parse_args()
    grapher = YagoGraphBuilder(
                args.relations_file,
                args.sparql,
                args.graph_file,
                args.np_file)
    import pdb;pdb.set_trace()
    logging.info("Yago::Adding Entity-Pair Relation Edge for Yago!")
    grapher.build_graph()
    logging.info("Yago::Exit!!")
