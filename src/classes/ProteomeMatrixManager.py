import time
import subprocess
import os

class MatrixManager:
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

    # make matrix
    def make_matrix(self):
        fp1 = open(self.output_folder + '/matrix1.txt', 'w')
        fp2 = open(self.output_folder + '/matrix2.txt', 'w')
        fp3 = open(self.output_folder + '/matrix3.txt', 'w')
        fp4 = open(self.output_folder + '/matrix4.txt', 'w')
        fp5 = open(self.output_folder + '/matrix5.txt', 'w')

        human_genome = self.genome_list[0]
        human_fp = open('proteins/1', 'r')
        for line in human_fp:
            print(line.strip())
            tokens = line.strip().split('\t')
            if len(tokens) >= 2:
                number = tokens[0]
                title = tokens[1]

                for genome in self.genome_list:
                    result = self.__search_from_human(title, genome)
                    fp1.write(result['number'] + '\t')
                    fp2.write(result['score'] + '\t')

                    if result['number'] == 'n/a':
                        result['score'] = 'n/a'
                    else:
                        result = self.__search_from_other(result['title'], genome, human_genome)

                    fp3.write(result['number'] + '\t')
                    fp4.write(result['score'] + '\t')
                    if result['number'] == 'n/a':
                        fp5.write('n/a' + '\t')
                    elif int(result['number']) == int(number):
                        fp5.write(result['number'] + '\t')
                    else:
                        fp5.write('NULL' + '\t')

                fp1.write('\n')
                fp2.write('\n')
                fp3.write('\n')
                fp4.write('\n')
                fp5.write('\n')

        human_fp.close()
        fp1.close()
        fp2.close()
        fp3.close()
        fp4.close()
        fp5.close()
       

    # search from human
    def __search_from_human(self, title, genome):
        result = {'number': 'n/a', 'score': 'n/a', 'title': 'n/a'}
        path = self.input_folder + '/1-' + genome['id']
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
        path = self.input_folder + '/' + genome['id'] + '-1'
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

    

