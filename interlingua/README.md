This readme deals with uploading SVO data to solr.
The directory contains the following

    solr_conf
        |
        |-- solrconfig.xml
        |-- schema.xml

    solr_splitter.py
    svo.txt
    solr_upload_svo.sh

solr conf directory contains two file required to get solr up and running.
    1. schema.xml: This defines the basic schema for indexing
    2. solrconfig.xml: This defines basic query handler and updater configuration.

These two files need to be copied to conf directory of solr.

Installation Instructions:
    1. Install apache solr from this link http://lucene.apache.org/solr/features.html. We are using version 4.6.1.
        Make sure you install the binary version not from the source.
    2. Ensure that Java is installed.
    3. We need example folder inside solr. Either copy it outside or ensure you run solr from inside the example folder.
        Lets call this SOLR_HOME.
    4. Copy files inside solr_conf directory to SOLR_HOME/solr/collection1/conf/
    5. Inside SOLR_HOME directory you will find start.jar. Now from this directory run
        java -jar start.jar
    6. To run solr on specific port use
        java -Djetty.port=<port no> -jar start.jar

Indexing SVO triples:
    To index SVO first we split the input file into multiple file containing <split size> quad tuples each
    Then we use solr bulk csv loader to upload these triples.

    To index SVO triples simply run python update
        ./solr_upload_svo.sh <ip:port of solr> <svo triples location> <split size>

