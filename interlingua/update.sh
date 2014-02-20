#!/usr/bin/sh
for file in `ls $2.*`
do
    curl $1'/solr/update?fieldnames=s,v,o,w,id&commitWithin=1200000&stream.file='$file'&stream.contentType=text/csv;charset=utf-8&separator=%09'
done
