Yago dataset is hosted as a Jena Fuseki based Sparql endpoint.
The choice of jena is made as Yago2 provides the data in TDB format for download
Otherwise too it provides convertor to convert Yago22 native format to TDB

Yago relations can be extracted from kb_mapping using
cat ../kb_mapping/yago_and_NELL.txt |tr " " "\n" | tr "\t" "\n"| grep yago | cut -d . -f 1 >../yago/yago_relations.txt

To construct Relation Entity-Pair edges and generate "Noun-Phrase-Pair Entity-Pair KB" list
python construct_graph.py -r yago_relations.txt -s http://localhost:3033/yago/query -g ../graph/graph -n ../interlingua/np_list
