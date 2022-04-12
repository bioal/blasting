import sys
import re

class SpeciesManager:
    def __init__(self, species_list):
        self.ids, self.taxids, self.species = {}, {}, {}
        fp = open(species_list, 'r')
        for line in fp:
            line = line.rstrip('\r\n')
            fields = line.split('\t')
            if len(fields) < 3:
                continue
            no = fields[0]
            taxid = fields[1]
            name = fields[2]
            if re.match(r'^[1-9][0-9]*$', no):
                self.ids[no] = line
                self.taxids[taxid] = no
                self.species[name] = no
        fp.close()
