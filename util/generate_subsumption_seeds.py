import argparse

def generate_seed_file(kb_mapping, seed_file):
    """ Generate seed file for KB.
    Labels are same as shorthand labels.
    This just copies the label qualified name as label """
    r_file = open(kb_mapping, 'r')
    s_file = open(seed_file, 'w+')

    for line in r_file:
        values = line.strip().split("\t")
        relations = values[1].split(" ")
        subsumptions = values[2].split(" ")
        for subsumption in subsumptions:
            if subsumption == "concept:relatedto":
                continue
            for relation in relations:
                s_file.write("%s\t%s\t1.0\n" %(relation, subsumption))

    r_file.close()
    s_file.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--relations_file",
            type=str, help="Relations file")
    parser.add_argument("-s", "--seed_file",
            type=str, help="Seed file")

    args = parser.parse_args()
    generate_seed_file(
            args.relations_file,
            args.seed_file)



