This directory contains gold-standard mapping between these KBs: 

(1) Freebase, 
(2) KBP, 
(3) YAGO 

and NELL in these files: 

(1) freebase_and_NELL.txt, 
(2) kbp_and_NELL.txt, and 
(3) yago_and_NELL.txt respectively

The format of each of this file is: 
<KB_relation> tab \
<space separated NELL relations that map to KB_relation> tab \
<space separated NELL relations that SUBSUMES KB_relation>

In freebase_and_NELL.txt, freebase relations (the first column of this file) 
are given generic names: freebase:relation_[0-9]+.tsv. 
The definition of these generic names is in the file freebase_relations.txt.

The format of freebase_relations.txt is:
<freebase:relation_[0-9]+.tsv> tab \
<freebase path for arg1 of this relation> tab \
<freebase path for arg2 of this relation> tab \
<filter for arg1> tab <filter for arg2>

Freebase path for argument is a sequence of column lookups. The sequence is 
separated by a colon (:) if the column to be looked up is in a table that is
different from the table of the previous column in the sequence, and 
is separated by a dash (-) if the columns are in the same table.
