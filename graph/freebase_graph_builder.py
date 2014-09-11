from SPARQLWrapper import SPARQLWrapper, JSON
from base_graph_builder import BaseGraphBuilder
import argparse
import logging
import json
import os
import re
import codecs

class FreebaseGraphBuilder(BaseGraphBuilder):
    QUERY = """
            PREFIX basekb: <http://rdf.basekb.com/ns/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            SELECT %s
            WHERE {
                %s
            }
        """

    #  Used with findall. Returns entities splitted on - and :
    RELATION_ARG_IDENTIFIER = r'[^-:]+'


    def __init__(self, relations_file, sparql_endpoint, graph_file, noun_phrase_file):
        self.sparql_client = SPARQLWrapper(sparql_endpoint, returnFormat=JSON)
        BaseGraphBuilder.__init__(self, "freebase", relations_file, graph_file, noun_phrase_file)


    def _canonicalize(self, value):
        value.replace("http://rdf.basekb.com/ns/", "basekb:")
        return value

    def _query_sparql(self,  query):
        response = None
        self.sparql_client.setQuery(query)
        try:
            response = json.loads(self.sparql_client.query().response.read())
        except:
            logging.error("Freebase::Query Failed%s",query)
        return response

    def _relation_name(self, relation_line):
        values = relation_line.strip().split("\t")
        (relation_name, ext) = values[0].split(".")
        return relation_name


    def _load_relations(self, relation_line):
        values = relation_line.strip().split("\t")
        (relation_name, ext) = values[0].split(".")
        subjects = [self.preprocess_types(type) for type in re.findall(self.RELATION_ARG_IDENTIFIER, values[1])]
        objects = [self.preprocess_types(type) for type in re.findall(self.RELATION_ARG_IDENTIFIER, values[2])]

        cvt = ".".join((subjects[0]).split(".")[:-1])

        relation = {
                'name': relation_name,
                'subjects': subjects,
                'objects': objects,
                'cvt': cvt,
                }

        if len(values) > 3:
            parts = re.findall(self.RELATION_ARG_IDENTIFIER, values[3])
            relation['filter1'] = [self.preprocess_types(type) for type in parts]
        if len(values) > 4:
            parts = re.findall(self.RELATION_ARG_IDENTIFIER, values[4])
            relation['filter2'] = [self.preprocess_types(type) for type in parts]
        return relation

    def _query_entity_pair(self, relation):
        relation_map = self._load_relations(relation)
        (cvt, subjects, objects, filters1, filters2) = (relation_map['cvt'],
                relation_map['subjects'],
                relation_map['objects'],
                relation_map.get('filter1', None),
                relation_map.get('filter2', None))

        q_arr = []
        subject_name_q = True
        object_name_q = True

        # add cvt clause to query
        q_arr.append(self.get_cvt_clause(cvt))

        # Get subject clause and add
        (subject_name_q, subject_arr) = self.create_non_cvt_clauses(subjects, filters1, True)
        q_arr.extend(subject_arr)

        # Get object clause and add
        (object_name_q, object_arr) = self.create_non_cvt_clauses(objects, filters2, False)
        q_arr.extend(object_arr)

        q_arg = "*"
        q_str = "\n".join(q_arr)

        logging.info("Query String:\n%s" % q_str)

        results = self._query_sparql(self.QUERY %(q_arg, q_str))
        tup_arr = []
        for result in results["results"]["bindings"]:
            subject = result["s"] if not subject_name_q else result["cvt"]
            object = result["o"] if not object_name_q else result["cvt"]

            tup_arr.append((subject, object))

        logging.info("      Freebase::Adding %s-(%s) edge" % (relation_map['name'], entity_pair))
        return tup_arr


    def _query_labels(self, entity):
        np_pairs = []
        query = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?o1
            WHERE {
                     <%s> rdfs:label ?o1 .
                    FILTER (lang(?o1) = 'en')

            }
        """
        % entity1.replace("basekb:", "http://rdf.basekb.com/ns/")

        results = self._query_sparql(query)

        np_values = []
        if results:
            for result in results["results"]["bindings"]:
                np_value.append(result["o1"]["value"])

        return np_values

    def preprocess_types(self, type):
        return "basekb:%s" % ".".join(type[1:].split("/"))


    def canonicalize_query(self, type):
        """ Removes name at the end as it is implict in sparql data and hence it is not present
        """
        parts = type.split(".")
        if parts[-1] == 'name':
            parts = parts[:-1]
        return ".".join(parts)

    def is_name_query(self, type):
        return type.split(".")[-1] == 'name'

    def get_cvt_clause(self, type):
        return "\t".join(["?cvt", "a", type, "."])

    def create_non_cvt_clauses(self, clauses, filters, is_subject):
        """ clauses are either subjects or object clauses
        """
        o_p = "?s" if is_subject else "?o"
        s = "?cvt"
        use_cvt = True
        q_arr = []

        for i in xrange(len(clauses)):
            # clauses with id just refer to the object. Can be ignored.
            if clauses[i].endswith("id"):
                continue

            if self.is_name_query(clauses[i]):
                q_arr.append("\t".join([s, "a", self.canonicalize_query(clauses[i]), "."]))
            else:
                o = o_p + str(i)
                if i == len(clauses) - 1 or (i == len(clauses) - 2 and self.is_name_query(clauses[i + 1])):
                    o = o_p
                    use_cvt = False
                q_arr.append("\t".join([s, self.canonicalize_query(clauses[i]) , o, "."]))
                s = o

        f_p = "?f"
        s = "?cvt"
        if filters:
            for i in xrange(len(filters) - 1):
                if filters[i].endswith("id"):
                    continue
                if self.is_name_query(filters[i]):
                    q_arr.append("\t".join([s, "a", self.canonicalize_query(filters[i]), "."]))
                else:
                    o = f_p + str(i)
                    q_arr.append("\t".join([s, self.canonicalize_query(filters[i]) , o, "."]))
                    s = o
            if filters[i + 1].find("NOTNULL") > -1:
                q_arr[-1] = "FILTER EXISTS {%s %s %s}" % (f_p + str(i - 1), filters[i], f_p + str (i))
            else:
                q_arr.append("FILTER (%s = %s)" % (s, filters[i + 1]))
        return (use_cvt, q_arr)


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
    grapher = FreebaseGraphBuilder(
                args.relations_file,
                args.sparql,
                args.graph_file,
                args.np_file)

    logging.info("Freebase::Adding Entity-Pair Relation Edge for Freebase!")
    grapher.build_graph()
    logging.info("Freebase::Exit!!")
