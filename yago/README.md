Packages and Dataset needed:
    Yago2core dataset can be downloaded from

    http://www.mpi-inf.mpg.de/yago-naga/yago1_yago2/download/yago2/YAGO2.3.0__yago2core_20120109/YAGO2.3.0__yago2core_20120109_jena.7z

    Jena Fuseki can be downloaded from

    http://mirrors.koehn.com/apache//jena/binaries/jena-fuseki-1.0.1-distribution.tar.gz

    java

    sudo apt-get install default-jre

    python sparqlwrapper

    sudo apt-get install python-sparqlwrapper

To run Jena Fuseki endpoint, use following command

    ${JENA_DIR}/fuseki-server --loc=${HOME}/yago_data/ --port=3030 /yago

where yago_data is the directory containing uncompressed yago2core data

Yago dataset is hosted as a Jena Fuseki based Sparql endpoint.
The choice of jena is made as Yago2 provides the data in TDB format for download
Otherwise too it provides convertor to convert Yago22 native format to TDB

Yago relations can be extracted from kb_mapping using

    cat ../kb_mapping/yago_and_NELL.txt |tr " " "\n" | tr "\t" "\n"| grep yago | cut -d . -f 1 >./yago/yago_relations.txt

To construct Relation Entity-Pair edges and generate "Noun-Phrase-Pair Entity-Pair KB" list

    python construct_graph.py -r yago_relations.txt -s <yago url> -g <path for graph file> -n <temp np file for interlingua edges>
