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
|___init__(target_dir): Init the Target directory and log file.
|_define_keywords(keyword, file_type, f_operation) -> Define the keyword, file format(txt, log) and opertion to be implemented
|_print_parameters() -> Prints the keyword to be searched, file type and the working Directory
|_exceptions(dir_exceptions=[], file_exceptions=[]) -> Pass the dir/file names to be avoided (full path not required)
|_parse_dir() -> Function to start the required operation in the target directory

SUPPORTED OPERATIONS:
* search -> search for a key work in the mentioned file types.

"""

import os, re, sys
import logging
import argparse

# Dir/Files to be avoided in search operation
dir_exp = ['.git']
file_exp = ['.gitignore']

# Define the parameters (default)
f_op = 'search'
key = 'honey bee'
f_type = 'txt'
target_dir=os.getcwd()
log_dest=''

class xFinder():
    
    def __init__(self, target_dir):
        
        self.target_dir = target_dir

        # Get the file name for logging purpose
        self.file_name = os.path.basename(__file__)
        self.log_name = "{}.log".format(self.file_name[:-3])
        logging.basicConfig(filename=self.log_name, filemode='w', format='%(asctime)s - %(message)s', \
            datefmt='%d-%b-%Y %H:%M:%S', level=logging.INFO)
        logging.info("Log for File: {}".format(self.file_name))
        global log_dest
        log_dest = "{}\\{}".format(os.getcwd(), self.log_name)

        os.chdir(self.target_dir)

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
        
        logging.info("OPERATION= {}\nKEYWORD=\"{}\"\nFILE_TYPE=\".{}\" \nTARGET_DIRECTORY: {}".\
            format(str.upper(self.op), self.keyword, self.file_type, self.target_dir))

    # Function to print the search parameters
    def print_parameters(self):
        print("PARAMETERS\nOperation: {}\nKeyword: {}\nFile_Type: {}".format(str.upper(self.op),\
        self.keyword, self.file_type))
        print("Target_Directory: {}\n".format(self.target_dir))

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
                print("{}\\{} -> MATCH FOUND for \"{}\" -> Line {}: {}".format(os.getcwd().replace(self.target_dir,'.'), \
                    f_name, self.keyword, l_no, to_print))
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


# Add support for command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--keyword", dest='keyword', help="Keyword to search")
parser.add_argument("--format", dest='f_format', help="File format to be searched")
parser.add_argument("--op", dest='f_operation', help="Operation to be performed", choices=['search', 'rename'])
parser.add_argument("--file_excep", dest='file_exc', help="Files to be exempted.\
    Usage: [file1, file2, file3]")
parser.add_argument("--dir_excep", dest='dir_exc', help="Directories to be exempted\
    Usage: [dir1, dir2, dir3]")
parser.add_argument("--target_dir", dest='target_dir', help="Directory to perform the operation")

args = parser.parse_args()

# Update the paramters to the variables
key = args.keyword if args.keyword else key
f_type = args.f_format if args.f_format else f_type
f_op = args.f_operation if args.f_operation else 'search'
dir_exp = dir_exp+ list(args.dir_exc.split()) if args.dir_exc else dir_exp
file_exp = file_exp+ list(args.file_exc.split()) if args.file_exc else file_exp
target_dir = args.target_dir if args.target_dir else target_dir


test = xFinder(target_dir)
test.define_keywords(key, f_type, f_op)
test.exceptions(dir_exp, file_exp)
test.print_parameters()
test.parse_dir()
print("\nLOG AT: {}".format(log_dest))