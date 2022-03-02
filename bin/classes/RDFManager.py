import subprocess
import os

class RDFManager:
    def __init__(self, genome_file_list):
        self.summary_file = genome_file_list

    def rdfize_genome(self):
        file_obtained = {}
        fp = open(self.summary_file, 'r', encoding='UTF-8')
        line = fp.readline()
        while line:
            line = line.strip()
            tokens = line.split('\t')
            if not line.startswith('#') and len(tokens) >= 8:
                gcf_id = tokens[0]
                taxid = tokens[5]
                species_taxid = tokens[6]
                species = tokens[7]
                url = tokens[19]
                print(f'genome:{gcf_id} mbgd:inTaxon taxid:{taxid} ;')
                print(f'    rdfs:label "{species}" .')
                # id = self.species_hash.get(species) or \
                #      self.taxid_hash.get(taxid) or \
                #      self.taxid_hash.get(species_taxid)
                # # if id is not None and file_obtained.get(id) is None:
                #     gcf_file = self.__download_gcf_file(url, debug)
                #     file_obtained[id] = gcf_file
            line = fp.readline()
        fp.close()

        # result_fp = open(self.downloaded_genomes, 'w')
        # for id in self.id_hash:
        #     if file_obtained.get(id) is None:
        #         print('Genome not obtained for: ' + self.id_hash[id])
        #     else:
        #         result_fp.write(id + '\t' + file_obtained[id] + '\n');
        # result_fp.close()

    def rdfize_proteome(self):
        print('@prefix dct: <http://purl.org/dc/terms/> .')
        print('@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .')
        print('@prefix proteome: <http://purl.uniprot.org/proteomes/> .')
        print('@prefix up: <http://purl.uniprot.org/core/> .')
        print('')
        file_obtained = {}
        fp = open(self.summary_file, 'r', encoding='UTF-8')
        line = fp.readline()
        while line:
            line = line.strip()
            tokens = line.split('\t')
            if line.startswith('UP000') and len(tokens) >= 8:
                gcf_id = tokens[0]
                taxid = tokens[1]
                oscode = tokens[2]
                proteins = tokens[4]
                isoforms = tokens[5]
                species = tokens[7]
                # print(f'proteome:{gcf_id} mbgd:inTaxon taxid:{taxid} ;')
                print(f'proteome:{gcf_id}')
                print(f'    dct:identifier "{gcf_id}" ;')
                print(f'    rdfs:label "{species}" ;')
                print(f'    up:oscode "{oscode}" ;')
                print(f'    up:proteins {proteins} ;')
                print(f'    up:isoforms {isoforms} .')
                print('')
                # url = 'ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Eukaryota/' + gcf_id + '_' + taxid + '.fasta.gz'
                # id = self.species_hash.get(species) or \
                #      self.taxid_hash.get(taxid) or \
                #      self.taxid_hash.get(species_taxid)
                # if id is not None and file_obtained.get(id) is None:
                #     gcf_file = self.__download_gcf_file(url, debug)
                #     file_obtained[id] = gcf_file
            line = fp.readline()
        fp.close()
