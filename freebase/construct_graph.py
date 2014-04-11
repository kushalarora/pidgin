from SPARQLWrapper import SPARQLWrapper, JSON
import argparse
import logging
import json
import os
import re

class FreebaseRelationGraph:
    KEY_QUERY = """

                """
    def __init__(self, relations_file, sparql_endpoint, graph_file, noun_phrase_file):
        self.sparql_client = SPARQLWrapper(sparql_endpoint, returnFormat=JSON)
        self.relations_file = relations_file
        self.graph_file = graph_file
        self.np_file = noun_phrase_file
        self.key_mp = {}        # key to mid

    def get_key(self, entity):
        if

    def build_graph(self, offset = 0):
        relations_file = open(self.relations_file, 'r')
        relations = [relation.strip() for relation in relations_file]

        if len(relations) == 0:
            assert "Freebase::Relations not found"

        for i in xrange(0, len(relations)):
            self._add_entity_relation_edge(relations[i])

    def _query_sparql(self,  query):
        response = None
        self.sparql_client.setQuery(query)
        try:
            response = json.loads(self.sparql_client.query().response.read())
        except:
            logging.error("Freebase::Query Failed%s",query)
        return response

    def _add_entity_relation_edge(self, relation):
        graph_file = open(self.graph_file, "a+")

        logging.info("Freebase::Processing Relation '%s'" % relation)

        query = """
<<<<<<< HEAD
            PREFIX yago: <http://yago-knowledge.org/resource/>
=======
            PREFIX basekb: <http://rdf.basekb.com/ns/>
>>>>>>> 87350278a58fdbf12583a6e9fafbbd0a18f07b49

        SELECT ?s ?o
        WHERE {
                ?s %s ?o .
        }
        """ % relation

        results = self._query_sparql(query)

        if not results:
            return

        for result in results["results"]["bindings"]:

            (entity1, entity2) = (self._minify_entity(result["s"]),
                                    self._minify_entity(result["o"]))
            entity_pair = "%s %s" % (self._encode_utf8(entity1),

                                        self._encode_utf8(entity2))
            logging.info("Freebase::Adding %s-(%s) edge" % (relation, entity_pair))

            graph_file.write("%s\n" % "\t".join([relation, entity_pair, "1.0"]))
            self._add_noun_phrases(result["s"], result["o"], entity_pair)
        graph_file.close()

    def _minify_entity(self, entity):
        value = entity["value"]
        if entity["type"] == "uri":
            value = entity["value"].replace("http://yago-knowledge.org/resource/", "yago:")
        return value

    def _encode_utf8(self, entity):
        return entity.encode('utf-8')


    def _add_noun_phrases(self, entity1, entity2, entity_pair):
        np_file = open(self.np_file, 'a+')
        np_pairs = []
        if entity1["type"] == 'uri' and \
            entity2["type"] == 'uri':
            query = """
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                SELECT ?o1 ?o2
                WHERE {
                         <%s> rdfs:label ?o1 .
                         <%s> rdfs:label ?o2 .
                }
            """ % (entity1["value"], entity2["value"])

            results = self._query_sparql(query)

            if not results:
                return

            for result in results["results"]["bindings"]:
<<<<<<< HEAD
                np_pair =   "%s\t%s" % (result["o1"]["value"].encode('utf-8'),
                                            result["o2"]["value"].encode('utf-8'))
                logging.info("      Freebase::%s" % np_pair)
=======
                np_pair =    (result["o1"]["value"].encode('utf-8'),
                                            result["o2"]["value"].encode('utf-8'))
>>>>>>> 87350278a58fdbf12583a6e9fafbbd0a18f07b49
                np_pairs.append(np_pair)

        elif entity1["type"] == 'uri' or \
            entity2["type"] == 'uri':

            entity = entity1["value"] if entity1["type"] == 'uri' else entity2["value"]

            query = """
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                SELECT ?o
                WHERE {
                         <%s> rdfs:label ?o .
                }
            """ % entity

            results = self._query_sparql(query)

            if not results:
                return
            for result in results["results"]["bindings"]:
<<<<<<< HEAD
                np_tuple =  (entity1["value"].encode('utf-8'),
=======
                np_pair =  (entity1["value"].encode('utf-8'),
>>>>>>> 87350278a58fdbf12583a6e9fafbbd0a18f07b49
                                result["o"]["value"].encode('utf-8')) \
                                    if entity1["type"] != 'uri' else \
                                        (result['o']['value'].encode('utf-8'),
                                            entity2['value'].encode('utf-8'))

<<<<<<< HEAD
                np_pair = '%s\t%s' % np_tuple
                logging.info("      Freebase::%s" % np_pair)
=======
>>>>>>> 87350278a58fdbf12583a6e9fafbbd0a18f07b49
                np_pairs.append(np_pair)
        else:
            assert "Both Entities are literals %s %s" % (entity1, entity2)

<<<<<<< HEAD
        for np_pair in np_pairs:
            np_file.write("%s\n" % "\t".join([np_pair, entity_pair, "yago"]))
        np_file.close()

=======
        np_set = set([])
        for np_pair in np_pairs:
            np_set.add(self.preprocess_np_pair(np_pair))

        for np_pair in np_set:
            logging.info("      Freebase::%s" % np_pair)
            np_file.write("%s\n" % "\t".join([np_pair, entity_pair, "yago"]))
        np_file.close()

    def preprocess_np_pair(self, np_pair):
        """ Takes np tuple and returns a tab seperated value
        """
        return "%s\t%s" %(self.preprocess_np(np_pair[0]),
                            self.preprocess_np(np_pair[1]))
    def preprocess_np(self, np):
        """ Conditions np pairs for better match.
            Condition includes things like lowercasing, replacing "-" and "_" by " ", removing suffixes like "_(Film)"
        """
        match = re.match("(.*?)[_ ]\(.*?\)", np)
        if match:
            np = match.group(1)

        return np.lower().replace("_", " ").replace("-", " ")

>>>>>>> 87350278a58fdbf12583a6e9fafbbd0a18f07b49
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
    grapher = FreebaseRelationGraph(
                args.relations_file,
                args.sparql,
                args.graph_file,
                args.np_file)

    logging.info("Freebase::Adding Entity-Pair Relation Edge for Freebase!")
    grapher.build_graph()
    logging.info("Freebase::Exit!!")
