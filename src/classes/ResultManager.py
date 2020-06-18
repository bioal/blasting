import os
import sys
import re
import time
import subprocess

class ResultManager:
    def __init__(self, input_folder, output_folder, list_file):
        self.input_folder = input_folder
        self.output_folder = output_folder
        if not os.path.exists(output_folder):
            os.makedirs(output_folder) 
        self.genome_list = self.__get_list(list_file)

    def __get_list(self, list_file):
        fp = open(list_file, 'r')
        list = []
        for line in fp:
            tokens = line.strip().split('\t')
            if len(tokens) >= 2:
                list.append({'id':tokens[0], 'faa_file':tokens[1]})
        fp.close()
        return list

    def is_invalid_id(self, id):
        if re.search(':', id):
            return True
        else:
            return False

    def parse_line(self, line):
        if line.startswith('#'):
            return None
        fields = line.split('\t')
        if len(fields) != 12:
            return None
        query_name = fields[0]
        query_ids = query_name.split('|')
        if len(query_ids) != 3:
            return None
        query_gene = query_ids[1]
        target_gene = fields[1]
        if self.is_invalid_id(query_gene):
            return False
        if self.is_invalid_id(target_gene):
            return False
        score = fields[11]
        return query_gene, target_gene, score

    def calc_bbh(self):
        for genome in self.genome_list:
            if genome['id'] != '1':
                self.make_matrix('1', genome['id'])

    def make_matrix(self, human_id, other_id):
        output_fp = open(f'{self.output_folder}/{human_id}-{other_id}', 'w')
        error_fp = open(f'{self.output_folder}/{human_id}-{other_id}.err', 'w')

        hash = {}
        hash_rev = {}
        score_val = {}

        input_fp = open(f'{self.input_folder}/{human_id}-{other_id}')
        for line in input_fp:
            parsed_line = self.parse_line(line.strip())
            if parsed_line is None:
                continue
            if parsed_line is False:
                print('ERROR:', line.strip(), file=sys.stderr)
                continue
            query_gene, target_gene, score = parsed_line
            
            if hash.get(query_gene):
                continue
            hash[query_gene] = target_gene
            score_val[(query_gene, target_gene)] = score
        input_fp.close()

        input_fp = open(f'{self.input_folder}/{other_id}-{human_id}')
        for line in input_fp:
            parsed_line = self.parse_line(line.strip())
            if parsed_line is None:
                continue
            if parsed_line is False:
                print('ERROR:', line.strip(), file=sys.stderr)
                continue
            query_gene, target_gene, score = parsed_line
            
            if hash.get(query_gene):
                continue
            hash_rev[query_gene] = target_gene
            score_val[(query_gene, target_gene)] = score
        input_fp.close()

        for query in hash:
            if not hash.get(query):
                print(f'ERROR: no such query {query}', file=error_fp)
                continue
            target = hash[query]
            if not hash_rev.get(target):
                print(f'ERROR: no such target {target}', file=error_fp)
                continue
            rev = hash_rev[target]
            if query == rev:
                print(query, target, score_val[(query, target)], score_val[(target, query)], sep='\t', file=output_fp)
        
        # human_genome = self.genome_list[0]
        # print(human_genome['id'])
        # human_fp = open('proteins/1', 'r')
        # for line in human_fp:
        #     print(line.strip())
        #     tokens = line.strip().split('\t')
        #     if len(tokens) >= 2:
        #         number = tokens[0]
        #         title = tokens[1]

        #         for genome in self.genome_list:
        #             result = self.__search_from_human(title, genome)
        #             fp1.write(result['number'] + '\t')
        #             fp2.write(result['score'] + '\t')

        #             if result['number'] == 'n/a':
        #                 result['score'] = 'n/a'
        #             else:
        #                 result = self.__search_from_other(result['title'], genome, human_genome)

        #             fp3.write(result['number'] + '\t')
        #             fp4.write(result['score'] + '\t')
        #             if result['number'] == 'n/a':
        #                 fp5.write('n/a' + '\t')
        #             elif int(result['number']) == int(number):
        #                 fp5.write(result['number'] + '\t')
        #             else:
        #                 fp5.write('NULL' + '\t')

        #         fp1.write('\n')

        # human_fp.close()
        # fp1.close()
       

    # search from human
    def __search_from_human(self, title, genome):
        result = {'number': 'n/a', 'score': 'n/a', 'title': 'n/a'}
        path = self.input_folder + '/1-' + genome['id'] + '.txt'
        if os.path.exists(path):
            result_fp = open(path, 'r')
            score = -1 
            for line in result_fp:
                tokens = line.strip().split('\t')
                if len(tokens) >= 12:
                    qid = tokens[0]
                    did = tokens[1]
                    bscore = tokens[11]
                    current_score = float(bscore)

                    if title.find(qid) >= 0 and current_score >= score:
                        element = self.__search_list(genome, did)
                        result['number'] = element['number']
                        result['title'] = element['title']
                        result['score'] = bscore
                        score = current_score
            result_fp.close()
        else:
            print('File does not exist: ' + path)
        return result

    def __parse_blast_result(self, path):
        result_fp = open(path, 'r')
        for line in result_fp:
            fields = line.strip().split('\t')
            if len(fields) >= 12:
                query_seq = fields[0]
                db_seq = fields[1]
                score = fields[11]
                print(query_seq + '\t' + db_seq + '\t' + score)
        return

    # search from other 
    def __search_from_other(self, title, genome, human_genome):
        result = {'number': 'n/a', 'score': 'n/a', 'title': 'n/a'}
        path = self.input_folder + '/' + genome['id'] + '-1.txt'
        human_genome = self.genome_list[0]
        if os.path.exists(path):
            result_fp = open(path, 'r')
            score = -1
            for line in result_fp:
                tokens = line.strip().split('\t')
                if len(tokens) >= 12:
                    qid = tokens[0]
                    did = tokens[1]
                    bscore = tokens[11]
                    current_score = float(bscore)

                    if title.find(qid) >= 0 and current_score >= score:
                        element = self.__search_list(human_genome, did)
                        result['number'] = element['number']
                        result['title'] = element['title'] 
                        result['score'] = bscore
                        score = current_score
            result_fp.close()
        else:
            print('File does not exist: ' + path)
        return result 


    # searches number
    def __search_list(self, genome, did):
        result = {'number': 'n/a', 'title': 'n/a'}
        fp = open('proteins/' + genome['id'], 'r')
        for line in fp:
            tokens = line.strip().split('\t')
            if len(tokens) >= 2:
                if tokens[1].find(did) >= 0:
                    result['number'] = tokens[0]
                    result['title'] = tokens[1]
        fp.close()
        return result 

    

