#!/bin/sh
isql 3030 dba dba exec="select * from DB.DBA.load_list;"
