import argparse
import re
def generate_seed_file(relation_file_path, seed_file_path, kb_type):
    """ Generate seed file for KB.
    Labels are same as shorthand labels.
    This just copies the label qualified name as label """
    r_file = open(relation_file_path, 'r')
    s_file = open(seed_file_path, 'w+')

    for line in r_file:
        relation = line.strip()
        #TODO:(Hack) Currently ignoring _concept relations
        # as they are not part of graph
        if kb_type == 'nell' and re.search('^_concept:', relation):
            continue

        s_file.write("%s\t%s\t1.0\n" %(relation, relation))
    r_file.close()
    s_file.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--relations_file",
            type=str, help="Relations file")
    parser.add_argument("-s", "--seed_file",
            type=str, help="Seed file")
    parser.add_argument("-k", "--kb",
            type=str, help="KB")

    args = parser.parse_args()
    generate_seed_file(
            args.relations_file,
            args.seed_file,
            args.kb)



