import sys

class SpeciesManager:
    def __init__(self, species_list):
        # [0] no
        # [1] species
        # [6] taxid
        self.ids, self.taxids, self.species = {}, {}, {}
        fp = open(species_list, 'r')
        for line in fp:
            line = line.rstrip('\r\n')
            fields = line.split('\t')
            if not fields[0].isdigit:
                # skip header line
                continue
            self.ids[fields[0]] = line
            if len(fields) >= 2:
                self.species[fields[1]] = fields[0]
            if len(fields) >= 7:
                self.taxids[fields[6]] = fields[0]
        fp.close()
