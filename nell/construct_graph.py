from pymongo import MongoClient
import argparse
import logging
import re

class NellRelationGraph:
    """ Builds Nell's Relation Entity Pair Edge and precursor to Noun Phrase Pair Entity Pair Edges graphs.
        Relation Entity Pair Edge aare  written to graph file.
        The structure of Relation Entity Pair Edge is
            <Relation> TAB <Entity Pair> TAB 1.0 (The default weight is 1.0 for Relation Entity Pair Edge)

        Noun Phrase Entity Pair file is written to noun_phrase file
        The structure of Noun Phrase Pair Entity Pair is
            <Entity Pair> TAB <Noun Phrase Pair>

        Note Noun Phrase Entity Pair file doesn''t contain Noun Phrase Entity Pair Edge.
        They are build in later stage as it needs a verb connection or same Noun Phrase Pair
        must be in otheer KBs.
    """

    def __init__(self, relations_file, mongo_url, mongo_port, db_name,  graph_file, noun_phrase_file):
        client = MongoClient(mongo_url, mongo_port)
        self.db = client[db_name]
        self.relations_file = relations_file
        self.graph_file = graph_file
        self.np_file = noun_phrase_file
        self.db.nell.ensure_index("relation")

    def _queryDB(self, query):
        """ Query interface to mongoDB.
            Query must be constructed outside.
        """
        return self.db.nell.find(query)

    def build_graph(self, offset = 0):
        """ Main method.
            Reads relations and calls method to add edges
        """
        relations_file = open(self.relations_file, 'r')
        relations = [relation.strip() for relation in relations_file]

        if len(relations) == 0:
            assert "NELL::Relations not found"

        for relation in relations:
            self._add_entity_relation_edge(relation)

    def _isAReverseConcept(self, entity):
        """ Relation given for NELL are in two forms:
                concept:<Relation> => This indicates forward relation(normal relation)
                _concept:<Relation> => This indicates reverse relation i.e.
                    value _concept:<Relation> entity == entity concept:<Relation> value
        """
        return re.match('_concept:', entity)

    def canonicalizeRelation(self, relation):
        """ For query purpose _concept has to be transformed to concept.
            Reversal of relation is treated in calling function.
        """
        return relation if not self._isAReverseConcept(relation) else relation[1:]

    def _add_entity_relation_edge(self, relation):
        """ Write Relation Entity Pair Edge to graph file.
            Also calls method method to write Noun Phrase Entity Pair to noun phrase file.
            Also handles reversing entity value placement to reverse relations.
        """
        logging.info("NELL::Processing Relation '%s'" % relation)
        graph_file = open(self.graph_file, "a+")

        is_reverse_relations = self._isAReverseConcept(relation)

        query = {
                'relation': self.canonicalizeRelation(relation)
                }

        for entries in self._queryDB(query):
            entity, entity_literals = (entries["entity"], entries["entity_literalstrings"]) if not is_reverse_relations \
                                            else (entries["value"], entries["value_literalstrings"])

            value, value_literals = (entries["value"], entries["value_literalstrings"]) if not is_reverse_relations \
                                            else (entries["entity"], entries["entity_literalstrings"])

            entity_pair = "%s %s" % (entity, value)
            graph_file.write("%s\n" % "\t".join([relation, entity_pair.encode('utf-8'), "1.0"]))
            self._add_noun_phrases(entity_literals, value_literals, entity_pair)

        graph_file.close()

    def _add_noun_phrases(self, entity_literals, value_literals, entity_pair):
        """ Write noun phrase entity pair to file.
            Must handling encoding as python by default treaats string to ascii.
        """
        np_file = open(self.np_file, 'a+')
        nps = set([])
        for e_literal in entity_literals:
            for v_literal in value_literals:
                tup = (self.preprocess_np(e_literal),
                                            self.preprocess_np(v_literal))
                logging.info("      NELL::%s %s" % tup)
                nps.add(tup)
        for (e_literal, v_literal) in nps:
            np_file.write("%s\n" % "\t".join([e_literal.encode('utf-8'),
                                                v_literal.encode('utf-8'),
                                                entity_pair.encode('utf-8'), "nell"]))
        np_file.close()

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
    parser.add_argument("-u", "--mongo_url", default='localhost',
            type=str, help="mongo url for data set")
    parser.add_argument("-p", "--mongo_port", default=27017,
            type=int, help="port of mongo data set")
    parser.add_argument("--db", default='test',
            type=str, help="Database name")
    parser.add_argument("-g", "--graph_file",
            type=str, help="Graph file to write entity pair relation edge")
    parser.add_argument("-n", "--np_file",
            type=str, help="File to write noun phrase pair for entity pair")

    args = parser.parse_args()
    grapher =   NellRelationGraph(
                args.relations_file,    # relation file
                args.mongo_url,         # url to mongo server(optional)
                args.mongo_port,        # port mongo running on(optional)
                args.db,                # db name
                args.graph_file,        # file to write Relation Entity Pair
                args.np_file)           # file to write Noun Phraes and corresponding Entity Pair
    logging.info("NELL::Adding Entity-Pair Relation Edge forNelll!")
    grapher.build_graph()
    logging.info("NELL::Exit!!")
