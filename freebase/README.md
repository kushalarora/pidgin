Packages and Dataset needed:
    Freebase dataset can be downloaded from

        http://basekb.com/gold/ using bitTorrent Client.


    The dump can be converted in TDB format to be used with Jena fuseki server using instruction in following link .

        http://mail-archives.apache.org/mod_mbox/jena-users/201203.mbox/%3C4F58B60F.604@googlemail.com%3E

    Currently a copy of Freebase data converted in TDB format is available on dsr server at /data/d01/freebase

    Jena Fuseki can be downloaded from

        http://mirrors.koehn.com/apache//jena/binaries/jena-fuseki-1.0.1-distribution.tar.gz

    java

        sudo apt-get install default-jre

    python sparqlwrapper

        sudo apt-get install python-sparqlwrapper

To run Jena Fuseki endpoint, use following command

    ${JENA_DIR}/fuseki-server --loc=<freebase tdb data path> --port=<port number> /yago

Freebase relations are present in current directory and were provided with kb mapping.

To construct Relation Entity-Pair edges and generate "Noun-Phrase-Pair Entity-Pair KB" list

    Constructing graph is non trivial due to size constraints leading to out of memory error. Hence it is advisable to use construct.sh script which splits the data into multiple files.

    ./construct.sh <relative path to construct_graph.py> <relation file> <freebase url> <graph file> <temp np file for interlingua edge>

    If the memory is not a constraint use directly

    python construct_graph.py -r freebase_relations.txt -s <freebase url> -g <path for graph file> -n <temp np file for interlingua edges>
