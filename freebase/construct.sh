#!/bin/sh

lines=`cat $2 |wc -l`

split_size=`expr $lines / 8`
echo $split_size
split -l $split_size $2 /tmp/$2-s
i=0
for file in `ls /tmp/$2-s*`
do
    nohup python $1/freebase/construct_graph.py -r $file -s $3 -g "$4-$i" -n "$5-$i" > /mnt/logs/$2.log &
    i=`expr $i + 1`
done
