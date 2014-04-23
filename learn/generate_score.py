import argparse
import logging
def generate_score(kb1_relation_file, kb2_relation_file,
                    kb1_label_file, kb2_label_file,
                    top_k, kb_mapping_file, out_file):
    kb1_relations = open(kb1_relation_file)
    kb2_relations = open(kb2_relation_file)
    kb_gold = open(kb_mapping_file)
    kb1_labels = open(kb1_label_file)
    kb2_labels = open(kb2_label_file)
    output = open(out_file, 'w+')

    kb1_arr = []
    kb2_arr = []
    kb_mapping = {}
    kb_gold_map = {}

    # Mapping for gold standards for evaluation
    # Only using equivaleence relation.
    # Format relation => [mapped relations]
    for line in kb_gold:
        values = line.strip().split("\t")
        # In supplied kb mapping file the relations are in <relation>.tsv format.
        # Removing .tsv from name
        relation = values[0].split(".")[0]
        # Relation may map to muultiple relations.
        kb_gold_map[relation] = values[1].split()

    # KB1 Relations list
    for line in kb1_relations:
        kb1_arr.append(line.strip())

    #KB2 relations list
    for line in kb2_relations:
        kb2_arr.append(line.strip())

    # Calculates Y(r1, r2) = A(r1, l_r2) * A(r2, l_r1)
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
                        kb_mapping[tup] = 100000

                    kb_mapping[tup] *= float(tmp_arr[i + 1])
                    if kb_mapping[tup] > 0:
                        logging.info("Updating alignment score for (%s %s): %.10f" % (tup[0], tup[1], kb_mapping[tup]))

    # Convert Y(r1,r2) tuples into ranked list for r1 and r2
    mapping = {}
    for key, value in kb_mapping.iteritems():
        if key[0] not in mapping:
            mapping[key[0]] = []
        mapping[key[0]].append((key[1], value))
        if key[1] not in mapping:
            mapping[key[1]] = []
        mapping[key[1]].append((key[0], value))

    # srt the list for ranking
    for key, value in mapping.iteritems():
        mapping[key] = sorted(value, key=lambda x:x[1], reverse=True)

    relavent_document = 0
    returned_document = 0
    total_documents = 0

    # Calculate relavent document, returned documents and total documents
    for key, value in mapping.iteritems():
        if key in kb_gold_map:
            returned_document += 1
            for (relation, prob) in value[:int(top_k)]:
                if relation in kb_gold_map[key]:
                    logging.info("Gold Standard matched: %s %s" % (key, relation))
                    relavent_document += 1
                    break
            output.write("%s\t%s\n" %(key, "\t".join([ "%s %f" % tup for tup in value[0:int(top_k)] ])))
        total_documents += 1

    print "Precision: %f" % (float(relavent_document)/float(returned_document))
    print "Recall: %f" % (float(relavent_document)/len(kb_gold_map))


    kb_gold.close()
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
    parser.add_argument("-k","--top_k",
            type=str, help="top k value")
    parser.add_argument("--gold",
            type=str, help="Output file")
    args = parser.parse_args()
    generate_score(
            args.kb1_relations,
            args.kb2_relations,
            args.kb1_labels,
            args.kb2_labels,
            args.top_k,
            args.gold,
            args.out)
