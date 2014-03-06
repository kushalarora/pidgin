Yago dataset is hosted as a Jena Fuseki based Sparql endpoint.
The choice of jena is made as Yago2 provides the data in TDB format for download
Otherwise too it provides convertor to convert Yago22 native format to TDB

Yago relations can be extracted from kb_mapping using
cat yago_and_NELL.txt |tr " " "\n" | tr "\t" "\n"| grep yago | cut -d . -f 1 >../yago/yago_relations.txt
