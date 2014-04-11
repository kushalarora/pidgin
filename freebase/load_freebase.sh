#!/bin/sh
echo "Are you sure you want to run loader"
read response
if [ "$response" = "y" ];
then
	isql 3030 dba dba exec="ld_dir_all('/home/vagrant/f', '*.gz', 'http://freebase.org');" &
	isql 3030 dba dba exec="rdf_loader_run (log_enable=>3);" &
	isql 3030 dba dba exec="rdf_loader_run (log_enable=>3);" &
	isql 3030 dba dba exec="rdf_loader_run (log_enable=>3);" &
	isql 3030 dba dba exec="rdf_loader_run (log_enable=>3);" &
	isql 3030 dba dba exec="rdf_loader_run (log_enable=>3);" &
	isql 3030 dba dba exec="rdf_loader_run (log_enable=>3);" &
	isql 3030 dba dba exec="rdf_loader_run (log_enable=>3);" &
	isql 3030 dba dba exec="rdf_loader_run (log_enable=>3);" &
	isql 3030 dba dba exec="rdf_loader_run (log_enable=>3);" &
	isql 3030 dba dba exec="rdf_loader_run (log_enable=>3);" &
	isql 3030 dba dba exec="rdf_loader_run (log_enable=>3);" &
	isql 3030 dba dba exec="rdf_loader_run (log_enable=>3);" &
	isql 3030 dba dba exec="rdf_loader_run (log_enable=>3);" &
	isql 3030 dba dba exec="rdf_loader_run (log_enable=>3);" &
	isql 3030 dba dba exec="rdf_loader_run (log_enable=>3);" &
	isql 3030 dba dba exec="rdf_loader_run (log_enable=>3);" &
    	wait
    	isql 3030 dba dba exec="checkpoint;"
fi
