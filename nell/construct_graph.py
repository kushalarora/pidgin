from pymongo import MongoClient
import argparse
import logging
import os
import re

DONE_TILL_FILE = "./done_till_relation"
class NellRelationGraph:
    def __init__(self, relations_file, mongo_url, mongo_port, db_name,  graph_file, noun_phrase_file):
        client = MongoClient(mongo_url, mongo_port)
        self.db = client[db_name]
        self.relations_file = relations_file
        self.graph_file = graph_file
        self.np_file = noun_phrase_file
        self.db.nell.ensure_index("relation")

    def _queryDB(self, query):
        return self.db.nell.find(query)

    def build_graph(self, offset = 0):
        relations_file = open(self.relations_file, 'r')
        relations = [relation.strip() for relation in relations_file]

        if len(relations) == 0:
            assert "NELL::Relations not found"

        try:
            done_till_relation_file = open(DONE_TILL_FILE, "r")
            done_till_relation_index = int(done_till_relation_file.read())
            done_till_relation_file.close()
        except IOError:
            done_till_relation_index = -1

        for i in xrange(done_till_relation_index + 1, len(relations)):
            self._add_entity_relation_edge(relations[i])
            done_till_relation_file = open(DONE_TILL_FILE, 'w+')
            done_till_relation_file.write(str(i))
            done_till_relation_file.close()
        os.remove(DONE_TILL_FILE)

    def _isAConcept(entity):
        return re.match('concept:', entity)

    def _add_entity_relation_edge(self, relation):
        graph_file = open(self.graph_file, "a+")
        logging.info("NELL::Processing Relation '%s'" % relation)

        query = {
                'relation': relation
                }
        for entries in self._queryDB(query):

            entity_pair = "%s %s" % (entries["entity"], entries["value"])
            graph_file.write("%s\n" % "\t".join([relation, entity_pair.encode('utf-8'), "1.0"]))
            self._add_noun_phrases(entries["entity_literalstrings"],
                                    entries["value_literalstrings"] , entity_pair)
        graph_file.close()

    def _add_noun_phrases(self, entity_literals, value_literals, entity_pair):
        np_file = open(self.np_file, 'a+')

        for e_literal in entity_literals:
            for v_literal in value_literals:
                np_pair = "'%s' '%s'" % (e_literal, v_literal)
                logging.info("      NELL::%s" % np_pair)
                np_file.write("%s\n" % "\t".join([np_pair.encode('utf-8'), entity_pair.encode('utf-8'), "nell"]))
        np_file.close()

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
                args.relations_file,
                args.mongo_url,
                args.mongo_port,
                args.db,
                args.graph_file,
                args.np_file)
    logging.info("NELL::Adding Entity-Pair Relation Edge forNelll!")
    grapher.build_graph()
    logging.info("NELL::Exit!!")
