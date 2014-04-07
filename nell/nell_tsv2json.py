import json
import argparse
import logging
import re


def nell_tsv2json(nell_input, nell_output):
    """ Read input file of NELL and convert it to
        json format.
    """
    inp_file = open(nell_input, 'r')
    out_file = open(nell_output, 'w+')

    line = inp_file.readline()
    fields = line.split("\t")

    # canonicalize fields
    fields = [field.strip()
                   .lower()
                   .replace(" ", "_") \
                for field in fields]
    for line in inp_file:
        columns = line.split("\t")

        # Convert space seperated values to arrays

        # column[6] => entity_literalstrings
        columns[6] = [literal.replace('"', "")  for literal in re.findall('\".*?\"', columns[6])]

        # column[7] => value_literalstrings
        columns[7] = [literal.replace('"', "")  for literal in re.findall('\".*?\"', columns[7])]


        # column[10] => categories for entity
        columns[10] = [category for category in columns[10].split()]

        # column[11] => categories for entity
        columns[11] = [category for category in columns[11].split()]

        entry = {}
        try:
            for i in xrange(0, len(columns)):
                if (i == 3 or # Iteration of promotion
                        i == 5 or # source
                        i == 12 ): # Candidate source
                    continue

                entry[fields[i]] = columns[i]
        except:
            logging.info("Error at line number %d:: \n%s\n" % (i, line))


        out_file.write("%s\n" % json.dumps(entry))
    out_file.close()
    inp_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser();
    parser.add_argument("-i", "--input_file",
            help="Path of input file",
            default='./nell.txt')
    parser.add_argument("-o", "--output_file",
            help="Path of output file",
            default='./nell_output.txt')
    args = parser.parse_args()
    FORMAT = '%(levelname)s %(asctime)s %(name)s: %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    nell_tsv2json(args.input_file, args.output_file)
