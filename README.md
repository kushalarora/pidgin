This source code is implementation of PIDGIN system from the paper PIDGIN: Ontology Alignment using WebText as Interlingua[http://dl.acm.org/citation.cfm?id=2505559].

The directory structure is given below. Each directory contains source code relating to running code in that directory.

PIDGIN:
    - freebase
        Contains source related to running freebase server and creating graph portion corresponding to Freebase entities, relations and noun phrases.

    - nell
        Contains source related to running nell server and creating nell portion of graph.

    - yago
        Contains source related to running yago server and creating nell portion graph.

    - kb_mapping
        Gold mapping for Yago to Nell, Freebase to Nell and KBP to Nell mapping

    - learn
        Contains configuration file for junto library which provides implementation of MAD algorithm (https://github.com/parthatalukdar/junto)

    - util
        Util functions/source. Currently contains a python script to create seeds for learning

    - interlingua
        Config to run SVO solr server and source to index the SVO data. SVO data is provided by Hazy group, CMU[ http://rtw.ml.cmu.edu/resources/svo/nell_hazy_svo_604m.gz]

    - graph
        Some rewrite of graph creation process to optimize and avoid code duplication. Still in progress.


Currently all datasets are present on dsr server under /data/d01.

Freebase
    Stored in TDB Format. Run using Jena Fuseki Server. Data present in /data/d01/freebase/data.

    Command to run server
        /data/d01/jena-fuseki/fuseki-server --loc=/data/d01/freebase/data --port=3031 /freebase

    Query url
        http://<server address:port>/freebase/query [example http://localhost:3031/freebase/query if running from dsr server]

Yago
    Stored in TDB Format. Run using Jena Fuseki Server. Data present in /data/d01/yago.

    Command to run server
        /data/d01/jena-fuseki/fuseki-server --loc=/data/d01/yago --port=3031 /yago

    Query url
        http://<server address:port>/yago/query [example http://localhost:3031/yago/query if running from dsr server]


Nell
    Nell data is stored in mongo db. The data is present on /data/d01/nell_data

    Command to run server
        /data/d01/mongodb/bin/mongod --dbpath=/data/d01/nell_data/

_
