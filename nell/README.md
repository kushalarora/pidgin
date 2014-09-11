This directory contains the code related to NELL KB data.

Currently NELL is hosted in a mongodb server.

nell_tsv2json.py script converts default nell data into json format.
This can be run as

    python nell_tsv2json.py -i <path of nell_tsv_file> -o <path to nell_json_file>

This json file is then imported into mongodb server using following command

    mongoimport -v --journal --dbpath=<data path> --collection=nell --type=json --file=./nell1.json

MongoDb server can be simply run

    mongod --dbpath=<data path>

NELL relations are extracted from kb_relations by using following command:

    cat yago_and_NELL.txt freebase_and_NELL.txt kbp_and_NELL.txt | tr " " "\n"|tr "\t" "\n"|sort | uniq  | grep concept >./nell/nell_relations.txt


The command to construct Nell Relation Entity Pair Edge Graph and corresponding precusor to Noun Phrase Pair Verb and Entity Pair Noun Phrase Pair Edge

    python construct_graph.py -r ./nell_relations.txt -g <graph file> -n <temp np file for interlingua edge>
