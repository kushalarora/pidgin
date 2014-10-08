import argparse
import logging
import pysolr

class NPEntityVerbEdge:
    INTRA_ENTITY_DELIMITER = "###"
    INTRA_VALUE_DELIMITER = "@@@"
    KEY_VALUE_DELIMITER = "$$$"

    def __init__(self, solr_url, np_files, graph_file):
        self.np_files = np_files
        self.graph_file = graph_file
        self.solr = pysolr.Solr(solr_url, timeout=10)
        self.mp = {
                }

    def add_np_entity_and_verb_edge(self):
        graph_file = open(self.graph_file, 'a+')
        for np_pair, list in self.mp.iteritems():
            try:
                (np1, np2) = np_pair.split(self.INTRA_ENTITY_DELIMITER)
            except:
                print np_pair
                continue
            docs = []
            try:
                results = self.solr.search('s:"%s" AND o:"%s"' % (np1.lower(), np2.lower()))
                docs = results.docs
            except Exception as e:
                print e
                pass
                #   logging.info("query failed for np pair %s\t%s"  % (np1, np2))

            if docs:
                logging.info("NP_Entity_Verb::Returned %d results for np_pair: %s\t%s" % (len(docs), np1, np2))

            if len(list) > 1 or len(docs) > 0:
                for entity_pair in list[1]:
                    triple =  self.KEY_VALUE_DELIMITER.join([np_pair,
                                            entity_pair,
                                            '1.0'])
                    if len(docs) > 0:
                        logging.info("NP_Entity_Verb::Adding NP_Entity Edge %s" % triple)
                    graph_file.write("%s\n" % triple)

                for doc in docs:
                    triple = self.KEY_VALUE_DELIMITER.join([np_pair, doc["v"], str(doc["w"])])
                    logging.info("NP_Entity_Verb::Adding NP_Verb Edge %s" % triple)
                    graph_file.write("%s\n" % triple)
        graph_file.close()

    def preprocess_np_files(self):
        for file_name in self.np_files:
            self.mp = {}
            file = open(file_name, 'r')
            for line in file:
                try:
                    (entity_pair, np_value_pairs) = line.strip().split(self.KEY_VALUE_DELIMITER)
                except:
                    print line
                    continue
                np_pairs = np_value_pairs.split(self.INTRA_VALUE_DELIMITER)

                for np_pair in np_pairs:
                    if np_pair not in self.mp:
                        #print np_pair
                        self.mp[np_pair] = []
                    self.mp[np_pair].append(entity_pair)
            file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    FORMAT = '%(levelname)s %(asctime)s %(name)s: %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    logging.getLogger(pysolr.__name__).setLevel(logging.WARNING)

    parser.add_argument("-s", "--solr_url",
            type=str, help="Url of solr endpoint")

    parser.add_argument("-f", "--np_files", nargs='+',
            type=str, help="File containing list of relation to be added to graph")

    parser.add_argument("-g", "--graph_file",
            type=str, help="Graph file to write entity pair relation edge")

    args = parser.parse_args()
    grapher = NPEntityVerbEdge(
                args.solr_url,
                args.np_files,
                args.graph_file)

    logging.info("NP_Entity_Verb::Adding NP-Pair and NP-Verb Edge!")
    grapher.preprocess_np_files()
    grapher.add_np_entity_and_verb_edge();
    logging.info("NP_Entity_Verb::Exit!!")
