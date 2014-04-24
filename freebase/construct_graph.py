from SPARQLWrapper import SPARQLWrapper, JSON
import argparse
import logging
import json
import os
import re
import codecs

class FreebaseRelationGraph:
    QUERY = """
            PREFIX basekb: <http://rdf.basekb.com/ns/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            SELECT %s
            WHERE {
                %s
            }
            LIMIT 10
        """

    def __init__(self, relations_file, sparql_endpoint, graph_file, noun_phrase_file):
        self.sparql_client = SPARQLWrapper(sparql_endpoint, returnFormat=JSON)
        self.relations_filename = relations_file
        self.graph_filename = graph_file
        self.np_filename = noun_phrase_file
        self.relations_file = None
        self.graph_file = None
        self.np_file = None


    def preprocess_types(self, type):
        return "basekb:%s" % ".".join(type[1:].split("/"))

    def _load_relations(self):
        relations = {}
        for line in self.relations_file:
            values = line.strip().split("\t")
            relation = values[0].split(".")[0]

            relations[relation] = {}
            relations[relation]['arg1'] = [self.preprocess_types(type) for type in re.findall(r'[^-:]+', values[1])]
            relations[relation]['arg2'] = [self.preprocess_types(type) for type in re.findall(r'[^-:]+', values[2])]
            arg1_cvt = ".".join((relations[relation]['arg1'][0]).split(".")[:-1])
            arg2_cvt = ".".join((relations[relation]['arg2'][0]).split(".")[:-1])
            assert arg1_cvt == arg2_cvt
            relations[relation]['cvt'] = arg1_cvt
            if len(values) > 3:
                parts = re.findall(r'[^-:]+', values[3])
                filter = "%s:%s" % (parts[-2], parts[-1])
                parts = parts[:-2]
                parts.append(filter)
                relations[relation]['filter1'] = [self.preprocess_types(type) for type in parts]
            if len(values) > 4:
                parts = re.findall(r'[^-:]+', values[4])
                filter = "%s:%s" % (parts[-2], parts[-1])
                parts = parts[:-2]
                parts.append(filter)
                relations[relation]['filter2'] = [self.preprocess_types(type) for type in parts]
        return relations

    def is_name_query(self, type):
        return type.split(".")[-1] == 'name'

    def get_other_query(self, type, is_subject):
        query_obj = "?s" if is_subject else "?o"
        return ("\t".join(["?cvt", type , query_obj, "."]))

    def  get_literal(self, is_subject, is_cvt=False):
        (type, lit) = ("?s", "?sl") if is_subject else ("?cvt", "?cl") if is_cvt else ("?o", "?ol")
        return "\t".join([type, "rdfs:label", lit, "."])

    def get_cvt(self, type):
        return "\t".join(["?cvt", "a", type, "."])

    def get_filter_str(self, is_subject):
        query_obj = "?sl" if is_subject else "?ol"
        return "FILTER (lang(%s) = 'en')" % query_obj

    def get_query(self, mp):
        (cvt, subject, object, filter1, filter2 ) = (mp['cvt'], mp['arg1'], mp['arg2'], mp.get('filter1', None), mp.get('filter2', None))
        if len(subject) > 1 or len(object) > 1 or  filter1 or  filter2:
            return None
        q_arr = []
        subject_name_q = True
        object_name_q = True
        q_arr.append(self.get_cvt(cvt))
        if not self.is_name_query(subject[0]):
            subject_name_q = False
            q_arr.append(self.get_other_query(subject[0], True))
        if not self.is_name_query(object[0]):
            object_name_q = False
            q_arr.append(self.get_other_query(object[0], False))

        q_str = "\n".join(q_arr)

        q_arg = "*"

        results = self._query_sparql(self.QUERY %(q_arg, q_str))
        tup_arr = []
        for result in results["results"]["bindings"]:
            subject = result["s"] if not subject_name_q else result["cvt"]
            object = result["o"] if not object_name_q else result["cvt"]

            tup_arr.append((subject, object))
        return tup_arr


    def build_graph(self, offset = 0):
        self.relations_file = open(self.relations_filename, 'r')
        self.graph_file = codecs.open(self.graph_filename, "w+", encoding='utf-8')

        self.np_file = codecs.open(self.np_filename, 'w+', encoding='utf-8')

        relations = self._load_relations()
        if len(relations) == 0:
            assert "Freebase::Relations not found"

        for relation, mp in relations.iteritems():
            self._add_entity_relation_edge(relation, mp)

        self.relations_file.close()
        self.graph_file.close()
        self.np_file.close()

    def _add_entity_relation_edge(self, relation, mp):

        logging.info("Freebase::Processing Relation '%s'" % relation)
        results = self.get_query(mp)
        if not results:
            return

        for (subject, object) in results:
            entity_pair = "%s %s" % (self._minify_entity(subject),
                                        self._minify_entity(object))
            logging.info("Freebase::Adding %s-(%s) edge" % (relation, entity_pair))

            self.graph_file.write("%s\n" % "\t".join([relation, entity_pair, "1.0"]))
            self._add_noun_phrases(subject, object, entity_pair)

    def _query_sparql(self,  query):
        response = None
        self.sparql_client.setQuery(query)
        try:
            response = json.loads(self.sparql_client.query().response.read())
        except:
            logging.error("Freebase::Query Failed%s",query)
        return response


    def _minify_entity(self, entity):
        value = entity["value"]
        if entity["type"] == "uri":
            value = entity["value"].replace("http://rdf.basekb.com/ns/", "basekb:")
        return value



    def _add_noun_phrases(self, entity1, entity2, entity_pair):
        np_pairs = []
        if entity1["type"] == 'uri' and \
            entity2["type"] == 'uri':
            query = """
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                SELECT ?o1 ?o2
                WHERE {
                         <%s> rdfs:label ?o1 .
                         <%s> rdfs:label ?o2 .
                        FILTER (lang(?o1) = 'en')
                        FILTER (lang(?o2) = 'en')

                }
            """ % (entity1["value"], entity2["value"])

            results = self._query_sparql(query)

            if not results:
                return

            for result in results["results"]["bindings"]:
                np_pair =    (result["o1"]["value"],
                                            result["o2"]["value"])
                np_pairs.append(np_pair)

        elif entity1["type"] == 'uri' or \
            entity2["type"] == 'uri':

            entity = entity1["value"] if entity1["type"] == 'uri' else entity2["value"]

            query = """
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                SELECT ?o
                WHERE {
                         <%s> rdfs:label ?o .
                        FILTER (lang(?o) = 'en')
                }
            """ % entity

            results = self._query_sparql(query)

            if not results:
                return
            for result in results["results"]["bindings"]:
                np_pair =  (entity1["value"],
                                result["o"]["value"]) \
                                    if entity1["type"] != 'uri' else \
                                        (result['o']['value'],
                                            entity2['value'])

                np_pairs.append(np_pair)
        else:
            assert "Both Entities are literals %s %s" % (entity1, entity2)

        np_set = set([])
        for np_pair in np_pairs:
            np_set.add(self.preprocess_np_pair(np_pair))

        for np_pair in np_set:
            logging.info("      Freebase::%s" % np_pair)
            self.np_file.write("%s\n" % "\t".join([np_pair, entity_pair, "freebase"]))


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
