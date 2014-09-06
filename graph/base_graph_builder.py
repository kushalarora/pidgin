class BaseGraphBuilder:
    KEY_VALUE_DELIMITER = "$$$"
    INTRA_VALUE_DELIMITER = "###"
    INTRA_ENTITY_PAIR_DELIMITER = "@@@"
    def __init__(kb_name, relation_list, entity_relation_filename, entity_label_filename):
        self.kb_name = kb_name
        self.relation_list = relation_list
        self.entity_relation_filename = entity_relation_filename
        self.entity_label_filename = entity_label_filename


    def _canonicalize(value):
        """ Takes the entity or relation uri and converts in kb::<entity or relation> format
        """
        raise NotImplementedError("Canonicalization should be overriden by the subclass")

    def _query_entity_pair(relation):
        """ Query relations for entities.
            Relation argument is in raw format as present in relation list
            Return list of canonicalized entity pairs(tuples (e1, e2)) for relation.
        """
        raise NotImplementedError("Subclass must override query_entity method")

    def _query_labels(entity):
        raise NotImplementedError("Subclass must ovverride query_label method")

    def build_graph():
        relation_file = open(self.entity_relation_filename, 'a+')
        label_file = open(self.entity_label_filename, 'a+')
        for relation in relation_list:
            entity_pairs = self._query_entity_pair(relation)
            entity_pair_stringify = INTRA_VALUE_DELIMITER.join(entity_pairs)
            relation_file.write(KEY_VALUE_DELIMITER.join([relation, entity_pair_string]))

            for entity_pair in entity_pairs:
                labels_entity1 = self._query_labels(entity_pair[0])
                label_file.write(KEY_VALUE_DELIMITER.join([entity_pair[0], [INTRA_ENTITY_PAIR_DELIMITER.join(labels_entity1)]]))

                labels_entity2 = self._query_labels(entity_pair[1])
                label_file.write(KEY_VALUE_DELIMITER.join([entity_pair[1], labels_entity2]))

        relation_file.close()
        label_file.close()




