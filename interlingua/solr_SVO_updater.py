import argparse
import logging
import urllib2
class SolrSVOUpdater:

    def __init__(self, server_url='http://localhost:8983/solr/', svo_file='./svo_file'):

        file = open(svo_file, 'r')
        num_triples = sum(1 for line in file)
        logging.info("Total # of SVO triples: %d", num_triples)
        file.close()
        i = 0;
        file = open(svo_file, 'r')
        for line in file:
            sentence = line.strip().split("\t");
            if (len(sentence) > 4):
                logging.warn("Sentence is not a quad tuple %s", sentence)
            #data = {
                        #"s": sentence[0],
                        #"v": sentence[1],
                        #"id": str(i),
                        #"o": sentence[2],
                        #"w": float(sentence[3])/float(num_triples)
                    #}
            sentence[3] = float(sentence[3])/num_triples
            sentence[4] = i;
            logging.info("Adding triplet %s",  data)


            i += 1;
        file.close()
        logging.info("Added %d records to solr", i)


if __name__ == "__main__":
    parser = argparse.ArgumentParser();
    FORMAT = '%(levelname)s %(asctime)s %(name)s: %(message)s'
    parser.add_argument("-s", "--server",
            help="server url for solr. Default is http://localhost:8983/solr",
            default='http://localhost:8983/solr')
    parser.add_argument("-i", "--input_file",
            help="Path of input file",
            default='./svo.txt')
    args = parser.parse_args()
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    logging.info("Server Url: %s",  args.server)
    logging.info("SVO File %s",  args.input_file)
    SolrSVOUpdater(args.server, args.input_file)



