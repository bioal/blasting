class FASTA:
    def __init__(self, fasta_file):
        self.fasta_file = fasta_file

    def preprocess(self):
        fp = open(self.fasta_file, 'r')
        for line in fp:
            if line.startswith('>'):
                line = line[1:].strip()
                print(str(count) + '\t' + line)
                count = count + 1;
        fp.close()
