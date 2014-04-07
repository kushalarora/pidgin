import argparse
import logging
import pysolr

class NPEntityVerbEdge:
    def __init__(self, solr_url, np_files, graph_file):
        self.np_files = np_files
        self.graph_file = graph_file
        self.solr = pysolr.Solr(solr_url, timeout=10)
        self.mp = {
                }

    def add_np_entity_and_verb_edge(self):
        graph_file = open(self.graph_file, 'a+')
        for np_pair, lists in self.mp.iteritems():

            (np1, np2) = np_pair.split("\t")
            docs = []
            try:
                results = self.solr.search('s:"%s" AND o:"%s"' % (np1, np2))
                docs = results.docs
            except:
                pass
                #   logging.info("query failed for np pair %s\t%s"  % (np1, np2))

            if docs:
                logging.info("NP_Entity_Verb::Returned %d results for np_pair: %s\t%s" % (len(docs), np1, np2))

            if len(lists[0]) > 1 or len(docs) > 0:
                np_pair = "%s %s" % (np1, np2)
                for entity_pair in lists[1]:
                    triple =  "\t".join([np_pair,
                                            entity_pair,
                                            '1.0'])
                    logging.info("NP_Entity_Verb::Adding NP_Entity Edge %s" % triple)
                    graph_file.write("%s\n" % triple)

                for doc in docs:
                    triple = "\t".join([np_pair, doc["v"], str(doc["w"])])
                    logging.info("NP_Entity_Verb::Adding NP_Verb Edge %s" % triple)
                    graph_file.write("%s\n" % triple)
        graph_file.close()

    def preprocess_np_files(self):

        for file_name in self.np_files:
            self.mp = {}
            file = open(file_name, 'r')
            for line in file:
                values = [value.strip() for value in line.split('\t')]

                np1 = values[0]
                np2 = values[1]

                np_pair = "%s\t%s" % (np1, np2)
                if np_pair not in self.mp:
                    self.mp[np_pair] = [set([]), set([])]   # list of lists, [[kbs], [entity_pairs]]

                self.mp[np_pair][0].add(values[3])   # kb for np_pair
                self.mp[np_pair][1].add(values[2])   # entity_pair for np_pair
            self.add_np_entity_and_verb_edge()
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
