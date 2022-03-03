import sys
import re

class SpeciesManager:
    def __init__(self, species_list):
        # [0] no
        # [1] taxid
        # [2] name
        self.ids, self.taxids, self.species = {}, {}, {}
        fp = open(species_list, 'r')
        for line in fp:
            line = line.rstrip('\r\n')
            fields = line.split('\t')
            # skip header line
            if re.match(r'^[1-9][0-9]*$', fields[0]):
                self.ids[fields[0]] = line
                if len(fields) > 2:
                    self.species[fields[2]] = fields[0]
                if len(fields) > 1:
                    self.taxids[fields[1]] = fields[0]
        fp.close()
