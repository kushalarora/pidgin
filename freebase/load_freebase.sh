#!/bin/sh
isql 3030 dba dba exec="ld_dir_all('/home/ubuntu/20140302/sieved', '*.gz', 'http://freebase.org');" &
isql 3030 dba dba exec="rdf_loader_run (log_enable=>3);" &
isql 3030 dba dba exec="rdf_loader_run (log_enable=>3);" &
isql 3030 dba dba exec="rdf_loader_run (log_enable=>3);" &
isql 3030 dba dba exec="rdf_loader_run (log_enable=>3);" &
isql 3030 dba dba exec="rdf_loader_run (log_enable=>3);" &
isql 3030 dba dba exec="rdf_loader_run (log_enable=>3);" &
isql 3030 dba dba exec="rdf_loader_run (log_enable=>3);" &
isql 3030 dba dba exec="rdf_loader_run (log_enable=>3);" &
