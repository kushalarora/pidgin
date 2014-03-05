This directory contains the code related to NELL KB data.

Currently NELL is hosted in a mongodb server.

nell_tsv2json.py script converts default nell data into json format.
This can be run as
        python nell_tsv2json.py -i <path of nell_tsv_file> -o <path to nell_json_file>
