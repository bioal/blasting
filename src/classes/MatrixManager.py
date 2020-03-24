import time
import subprocess
import os

class MatrixManager:
    # constructor
    def __init__(self, output_folder, list_file, input_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder) 
        self.output_folder = output_folder
        self.genome_list = self.__get_list(list_file)
        self.input_folder = input_folder

    # get list
    def __get_list(self, list_file):
        fp = open(list_file, 'r')
        list = []
        for line in fp:
            tokens = line.strip().split('\t')
            if len(tokens) >= 6:
                id = tokens[0]
                gene_id = tokens[1]
                species = tokens[2]
                faa_file = tokens[3]
                list_file = tokens[4]
                database = tokens[5]
                
                genome = {'id':id, 'gene_id':gene_id, 'species':species, 'faa_file':faa_file, 'list_file': list_file, 'database': database}
                list.append(genome)
        fp.close()
        return list

    # make matrix
    def make_matrix(self):
        fp1 = open(self.output_folder + '/matrix1.txt', 'w')
        fp2 = open(self.output_folder + '/matrix2.txt', 'w')
        fp3 = open(self.output_folder + '/matrix3.txt', 'w')
        fp4 = open(self.output_folder + '/matrix4.txt', 'w')

        human_genome = self.genome_list[0]
        human_fp = open(human_genome['list_file'], 'r')
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
                fp1.write('\n')
                fp2.write('\n')
                fp3.write('\n')
                fp4.write('\n')

        human_fp.close()
        fp1.close()
        fp2.close()
        fp3.close()
        fp4.close()

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
        fp = open(genome['list_file'], 'r')
        for line in fp:
            tokens = line.strip().split('\t')
            if len(tokens) >= 2:
                if tokens[1].find(did) >= 0:
                    result['number'] = tokens[0]
                    result['title'] = tokens[1]
        fp.close()
        return result 

    

