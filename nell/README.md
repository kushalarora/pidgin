This directory contains the code related to NELL KB data.

Packages and Dependencies:
    1. MongoDB
        sudo apt-get install mongodb
    2. pymongo
        sudo apt-get install python-pymongo

    3. NELL dataset
        http://rtw.ml.cmu.edu/resources/results/08m/NELL.08m.825.esv.csv.gz
Currently NELL is hosted in a mongodb server.

nell_tsv2json.py script converts default nell data into json format.
This can be run as
        python nell_tsv2json.py -i <path of nell_tsv_file> -o <path to nell_json_file>

NELL relations are extracted from kb_relations by using following command:
    cat yago_and_NELL.txt freebase_and_NELL.txt kbp_and_NELL.txt | tr " " "\n"|tr "\t" "\n"|sort | uniq  | grep concept >../nell/nell_relations.txt


The command to construct Nell Relation Entity Pair Edge Graph and corresponding precusor to Noun Phrase Pair Verb and Entity Pair Noun Phrase Pair Edge

    python construct_graph.py -r ./nell_relations.txt -g ~/graph/nell_graph -n ~/np_list/nell_np_list
