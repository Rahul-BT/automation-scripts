"""
This python script is used to search keyword in many text/log files. The files can be in many directories in the home
directory. This script will go through each dir in the home, open the text/log files and search for the keyword.
If found, then the Filename and line will be printed.

__author__  = "Rahul B Thomas"
__status__  = "Development"
__date__    = "06-Apr-2021"

USAGE DETAILS:
Class: xFinder()
Functions:
|_define_keywords(keyword, file_type) -> Define the keyword and file format to search (txt, log)
|_print_parameters() -> Prints the keyword to be searched, file type and the working Directory
|_exceptions(dir_exceptions=[], file_exceptions=[]) -> Pass the dir/file names to be avoided (full path not required)
|_parse_dir(operation) -> Function to start the operation (search) in the current directory

SUPPORTED OPERATIONS:
* search -> search for a key work in the mentioned file types.

"""
import os, re, sys
import logging

# Dir/Files to be avoided in search operation
dir_exp = ['.git']
file_exp = ['.gitignore']

# Define the parameters
f_op = 'search'
key = 'honey'
f_type = 'txt'

class xFinder():
    
    def __init__(self, home_dir=os.getcwd()):
        # Init the logger module
        self.home_dir = home_dir
        os.chdir(self.home_dir)

        # Get the file name for logging purpose
        self.file_name = os.path.basename(__file__)
        self.log_name = "{}.log".format(self.file_name[:-3])
        logging.basicConfig(filename=self.log_name, filemode='w', format='%(asctime)s - %(message)s', \
            datefmt='%d-%b-%Y %H:%M:%S', level=logging.INFO)
        logging.info("Log for File: {}".format(self.file_name))
        
        # Declare the dir/file exceptions
        self.dir_exceptions=[]
        self.file_exceptions=[self.log_name] 

    def exceptions(self, dir_exceptions=[], file_exceptions=[]):
        # Directory and files to avoid checking
        self.dir_exceptions += dir_exceptions
        self.file_exceptions += file_exceptions

    # Function to define the keywords for search
    def define_keywords(self, keyword, file_type, f_operation):
        self.keyword = keyword
        self.file_type = file_type
        self.op = f_operation
        
        logging.info("OPERATION= {}\nKEYWORD=\"{}\"\nFILE_TYPE=\".{}\" \nHOME_DIR: {}".\
            format(str.upper(self.op), self.keyword, self.file_type, self.home_dir))

    # Function to print the search parameters
    def print_parameters(self):
        print("PARAMETERS\nOperation: {}\nKeyword: {}\nFile_Type: {}".format(str.upper(self.op),\
        self.keyword, self.file_type))
        print("Home_Dir: {}".format(self.home_dir))

    # Function to search the keyword in the files
    def find_words(self, f_name):
        f1 = open(f_name, 'r')
        # Pattern to find 3 words before and after the keyword
        patt = "((?:[\S]+\s+){1,3})"+self.keyword+"((?:\s+[\S]+){1,3})"
        l_no = 0
        for line in f1:
            l_no += 1 # For line numbers
            z = re.search(patt, line)
            if z:
                to_print = str(self.keyword).join( list(z.groups()) )
                print("File: {} -> MATCH FOUND for \"{}\" -> Line {}: {}".format(f_name, self.keyword, l_no, to_print))
                logging.info("{}\\{} -> MATCH FOUND for \"{}\" -> Line {}: {}".format(os.getcwd(), \
                    f_name, self.keyword, l_no, to_print))
        f1.close()

    # Function (recursive) to parse the directories and find files with the given format
    # Requires f_operation that defines the type of operation to be performed
    def parse_dir(self):
        elements = os.listdir()
        
        func_dict = {'search': self.find_words}
        try:
            func_to_exec = func_dict[self.op]
        except :
            print("[ERROR]: Operation \"{}\" is not valid".format(self.op))
            logging.info("[ERROR]: Operation \"{}\" is not valid".format(self.op))
            sys.exit()

        dir_ = [x for x in elements if (os.path.isdir(x) and x not in self.dir_exceptions)]
        file_ = [x for x in elements if (os.path.isfile(x) and x.endswith(self.file_type) \
            and x not in self.file_exceptions)]
        
        # Parse through the child dirs 
        if dir_:
            for i in dir_:
                os.chdir(i)
                logging.info("{}".format(os.getcwd()))
                self.parse_dir()
                os.chdir('../')
        # If files are found, execute the required function
        if file_:
            for i in file_:
                logging.info("{}\\{}".format(os.getcwd(), i))    
                func_to_exec(i)
            return 1
        return 1

test = xFinder()
test.define_keywords(key, f_type, f_op)
test.exceptions(dir_exp, file_exp)
test.print_parameters()
test.parse_dir()
