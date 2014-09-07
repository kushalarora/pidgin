class BaseGraphBuilder:
    KEY_VALUE_DELIMITER = "$$$"
    INTRA_VALUE_DELIMITER = "###"
    INTRA_ENTITY_PAIR_DELIMITER = "@@@"
    def __init__(self, kb_name, relation_list, entity_relation_filename, entity_label_filename):
        self.kb_name = kb_name
        self.relation_list = relation_list
        self.entity_relation_filename = entity_relation_filename
        self.entity_label_filename = entity_label_filename


    def _canonicalize(self, value):
        """ Takes the entity or relation uri and converts in kb::<entity or relation> format
        """
        raise NotImplementedError("Canonicalization should be overriden by the subclass")

    def _query_entity_pair(self, relation):
        """ Query relations for entities.
            Relation argument is in raw format as present in relation list
            Return list of canonicalized entity pairs(tuples (e1, e2)) for relation.
        """
        raise NotImplementedError("Subclass must override query_entity method")

    def _query_labels(self, entity):
        raise NotImplementedError("Subclass must ovverride query_label method")

    def build_graph(self):
        relation_file = open(self.entity_relation_filename, 'a+')
        label_file = open(self.entity_label_filename, 'a+')
        label_map = {}
        for relation in open(self.relation_list):
            relation = relation.strip()
            entity_pairs = self._query_entity_pair(relation)
            entity_pair_stringify = self.INTRA_VALUE_DELIMITER.join([self.INTRA_ENTITY_PAIR_DELIMITER.join(pair) for pair in entity_pairs])
            relation_file.write("%s\n" % self.KEY_VALUE_DELIMITER.join([relation, entity_pair_stringify]).encode('utf-8'))

            for entity_pair in entity_pairs:
                if entity_pair[0] not in label_map:
                    label_entity1 = self._query_labels(entity_pair[0])
                    label_map[entity_pair[0]] = label_entity1
                if entity_pair[1] not in label_map:
                    label_entity2 = self._query_labels(entity_pair[1])
                    label_map[entity_pair[1]] = label_entity2

        for entity in label_map:
            label_file.write("%s\n" % self.KEY_VALUE_DELIMITER.join([entity, self.INTRA_VALUE_DELIMITER.join(label_map[entity])]).encode('utf-8'))

        relation_file.close()
        label_file.close()




