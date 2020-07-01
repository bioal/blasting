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
                continue
            species_id = fields[0]
            id_hash[species_id] = line
            if len(fields) >= 2:
                species = fields[1]
                species_hash[species] = species_id
            if len(fields) >= 7:
                taxid = fields[6]
                taxid_hash[taxid] = species_id
        fp.close()
        return id_hash, taxid_hash, species_hash
