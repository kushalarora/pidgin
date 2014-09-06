from pymongo import MongoClient
import argparse
import logging
from base_graph_builder import BaseGraphBuilder
import re

class NellGraphBuilder(BaseGraphBuilder):
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

    def __init__(self, relations_file, mongo_url, mongo_port, db_name, entity_relation_file, label_file):
        client = MongoClient(mongo_url, mongo_port)
        self.db = client[db_name]
        self.db.nell.ensure_index("relation")
        # Entity to label strings
        self.entity_to_label_map = {}

        super("NELL", relations_file, entity_relation_file, label_file)


    def _canonicalize(value):
        return "NELL::%s" % value

    def _query_entity_pair(relation):
        logging.info("NELL::Processing Relation '%s'" % relation)

        self.entity_to_label_map = {}
        query = {
                'relation': self.canonicalizeRelation(relation)
                }

        entity_pairs = []
        for entries in self.db.nell.find(query):
            entity, entity_literals, value, value_literals = (self._canonicalize(entries["entity"]),
                    entries["entity_literalstrings"], self._canonicalize(entries["value"]), entries["value_literalstrings"])

            self.entity_to_label_map[entity] = entity_literals
            self.entity_to_label_map[value] = value_literals

            entities = (entity, value) if self._isAReverseConcept(relation) else (value, entity)
            entity_pairs.append(entities)

        return entity_pairs

    def _query_labels(entity):
        return self.entity_to_label_map[entity]

    def _isAReverseConcept(self, entity):
        """ Relation given for NELL are in two forms:
                concept:<Relation> => This indicates forward relation(normal relation)
                _concept:<Relation> => This indicates reverse relation i.e.
                    value _concept:<Relation> entity == entity concept:<Relation> value
        """
        return re.match('_concept:', entity)

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
    parser.add_argument("--db", default='nell',
            type=str, help="Database name")
    parser.add_argument("-g", "--graph_file",
            type=str, help="Graph file to write entity pair relation edge")
    parser.add_argument("-n", "--np_file",
            type=str, help="File to write noun phrase pair for entity pair")

    args = parser.parse_args()
    import pdb;pdb.set_trace()
    grapher =   NellGraphBuilder(
                args.relations_file,    # relation file
                args.mongo_url,         # url to mongo server(optional)
                args.mongo_port,        # port mongo running on(optional)
                args.db,                # db name
                args.graph_file,        # file to write Relation Entity Pair
                args.np_file)           # file to write Noun Phraes and corresponding Entity Pair
    logging.info("NELL::Adding Entity-Pair Relation Edge forNelll!")
    grapher.build_graph()
    logging.info("NELL::Exit!!")
