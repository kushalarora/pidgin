from SPARQLWrapper import SPARQLWrapper, JSON
import pysolr
import argparse
import logging


class ConstructGraph:
    def __init__(self, dataset, sparql_endpoint, svo_endpoint, graph_file, limit = 10000, backup_point="./backup"):
        self.sparql_client = SPARQLWrapper(sparql_endpoint, returnFormat=JSON)
        self.solr_client = pysolr.Solr(svo_endpoint)
        self.limit = limit;
        self.backup_file = backup_point
        self.graph_filename = graph_file
        self.dataset = dataset


    def query(self, offset = 0):
        try:
            backup_point = open(self.backup_file, "r")
            offset_str = backup_point.read()
            offset = 0 if not offset_str else int(offset_str)
            backup_point.close()
        except IOError:
            offset = 0

        query = """
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX rdf: <http://yago-knowledge.org/resource>
                    SELECT ?s ?v ?o
                    WHERE {
                        ?s ?v ?o
                        FILTER NOT EXISTS { ?s rdf:type ?o }
                    }
                    LIMIT %s
                    OFFSET %s
                """
        self.sparql_client.setQuery(query % (self.limit, offset))

        results = self.sparql_client.query().convert()

        for result in results["results"]["bindings"]:
            logging.info("%s: %s" % (self.dataset, result))

        backup_point = open(self.backup_file, "w")
        backup_point.write(str(offset + self.limit))
        backup_point.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    FORMAT = '%(levelname)s %(asctime)s %(name)s: %(message)s'
    parser.add_argument("-d", "--dataset", type=str,
            help="name of dataset for graph construction")
    parser.add_argument("--sparql", type=str,
            help="sparql url for data set")
    parser.add_argument("--svo", type=str,
            help="solr end point for svo triplets",
            default="http://localhost:3031/solr")
    parser.add_argument("-b", "--batch_size", type=int,
            help="how many records to process in one go",
            default=100)

    logging.basicConfig(format=FORMAT, level=logging.INFO)
    args = parser.parse_args()
    import pdb;pdb.set_trace()
    grapher = ConstructGraph(
                args.dataset,
                args.sparql,
                args.svo,
                "./hello.txt",
                args.batch_size)

    grapher.query()
