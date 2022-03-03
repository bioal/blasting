import sys

class SpeciesManager:
    def __init__(self, species_list):
        self.species_list = species_list

    def get_hash(self):
        id_hash, taxid_hash, species_hash = {}, {}, {}
        fp = open(self.species_list, 'r')
        for line in fp:
            line = line.rstrip('\r\n')
            fields = line.split('\t')
            if not fields[0].isdigit:
                # skip header line
                continue
            id_hash[fields[0]] = line
            if len(fields) >= 2:
                species_hash[fields[1]] = fields[0]
            if len(fields) >= 7:
                taxid_hash[fields[6]] = fields[0]
        fp.close()
        return id_hash, taxid_hash, species_hash
