import argparse
import logging
import operator
def generate_score(kb1_relation_file, kb2_relation_file,
                    kb1_label_file, kb2_label_file, out_file):
    kb1_relations = open(kb1_relation_file)
    kb2_relations = open(kb2_relation_file)
    kb1_labels = open(kb1_label_file)
    kb2_labels = open(kb2_label_file)
    output = open(out_file, 'w+')

    kb1_arr = []
    kb2_arr = []

    kb_mapping = {}
    for line in kb1_relations:
        kb1_arr.append(line.strip())

    for line in kb2_relations:
        kb2_arr.append(line.strip())
    for arr, labels in [(kb2_arr, kb1_labels), (kb1_arr, kb2_labels)]:
        for line in labels:
            values = line.strip().split('\t')
            value = values[0]
            if value in arr:
                tmp_arr = values[3].strip().split(" ")
                for i in xrange(0, len(tmp_arr), 2):
                    if tmp_arr[i] == '__DUMMY__':
                        continue
                    tup = tuple(sorted([value, tmp_arr[i]], reverse=True))
                    if tup not in kb_mapping:
                        logging.info("Adding relation alignment score for (%s %s)" % tup)
                        kb_mapping[tup] = 100000000

                    kb_mapping[tup] *= float(tmp_arr[i + 1])

    mapping = {}

    for key, value in kb_mapping.iteritems():
        if key[0] not in mapping:
            mapping[key[0]] = []
        mapping[key[0]].append((key[1], value))
    import pdb;pdb.set_trace()
    for key,value in mapping.iteritems():
        output.write("%s\t%s\n" %(key, "\t".join([
                                            "%s %f" % tup
                                            for tup in sorted(value, key=lambda x:x[1], reverse=True)[0:20]
                                                ])))


    kb1_relations.close()
    kb2_relations.close()
    kb1_labels.close()
    kb2_labels.close()
    output.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    FORMAT = '%(levelname)s %(asctime)s %(name)s: %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    parser.add_argument("--kb1_relations",
            type=str, help="KB1 relations file")
    parser.add_argument("--kb2_relations",
            type=str, help="KB2 relations file")
    parser.add_argument("--kb1_labels",
            type=str, help="Output labels for KB1")
    parser.add_argument("--kb2_labels",
            type=str, help="Output labels for KB2")
    parser.add_argument("--out",
            type=str, help="Output file")
    args = parser.parse_args()
    generate_score(
            args.kb1_relations,
            args.kb2_relations,
            args.kb1_labels,
            args.kb2_labels,
            args.out)
