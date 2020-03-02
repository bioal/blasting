class TxtFile:
    # constructor
    def __init__(self, fp):
        self.fp = fp

    # downloads file 
    def write_line(self, text):
        self.fp.write(text)
        self.fp.write('\r\n')
