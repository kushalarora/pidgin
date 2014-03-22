import argparse

def generate_seed_file(relation_file_path, seed_file_path):
    """ Generate seed file for KB.
    Labels are same as shorthand labels.
    This just copies the label qualified name as label """
    r_file = open(relation_file_path, 'r')
    s_file = open(seed_file_path, 'w+')

    for line in r_file:
        relation = line.strip()
        s_file.write("%s\t%s\t1.0\n" %(relation, relation))
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



