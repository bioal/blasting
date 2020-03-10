class OptionParser:
    # constructor
    def __init__(self, argv):
        self.argv = argv

    # get option 
    def get_option(self, option):
        str = '-' + option
        flag = False
        value = None
        
        for arg in self.argv:
            if arg == str:
                flag = True
            else:
                if flag == True:
                    value = arg
                flag = False
        return value

