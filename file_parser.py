"""
This python script is used to search keyword in many text/log files. The files can be in many directories in the home
directory. This script will go through each dir in the home, open the text/log files and search for the keyword.
If found, then the Filename and line will be printed.

__author__  = "Rahul B Thomas"
__email__   = "rahulbthomas@gmail.com"
__status__  = "Development"
__date__    = "06-Apr-2021"

"""
import os, re, sys
import logging

# Get the file name for logging purpose
file_name = os.path.basename(__file__)
# Log file name, DO NOT CHANGE
log_file = 'find_auto_logger.log'

# Placeholder for keyword and file format type
keyword = 'honey bee'
file_type = 'txt'
home_dir = 'C:\\Users\\rahul\\Scripts\\automation_scripts'

# Change dir to home and create log file
os.chdir(home_dir)
logging.basicConfig(filename=log_file, filemode='w', format='%(asctime)s - %(message)s', \
    datefmt='%d-%b-%Y %H:%M:%S', level=logging.INFO)

# Directory and files to avoid checking
dir_exceptions = []
file_exceptions = [] 
file_exceptions.append(log_file)
dir_exceptions.append('.git')

logging.info("File name: {}".format(file_name))
logging.info("Keyword=\"{}\" \t File_type=\".{}\"".format(keyword, file_type))

# Function to search the keyword in the files
def find_words(f_name, val):
    f1 = open(f_name, 'r')
    # Pattern to find 3 words before and after the keyword
    patt = "((?:[\S]+\s+){1,3})"+val+"((?:\s+[\S]+){1,3})"
    l_no = 0
    for line in f1:
        l_no += 1 # For line numbers
        z = re.search(patt, line)
        if z:
            to_p = str(val).join( list(z.groups()) )
            print("File: {} -> \"{}\" MATCH FOUND -> Line {}: {}".format(f_name, val, l_no, to_p))
            logging.info("{}\\{} -> MATCH FOUND -> Line {}: {}".format(os.getcwd(), f_name, l_no, to_p))
    f1.close()

# Function (recursive) to parse the directories and find files with the given format
def parse_dir(val, func_to_exec, f_type='txt'):
    elements = os.listdir()
    
    dir_ = [x for x in elements if (os.path.isdir(x) and x not in dir_exceptions)]
    file_ = [x for x in elements if (os.path.isfile(x) and x.endswith(f_type) \
        and x not in file_exceptions)]
    
    # Parse through the child dirs 
    if dir_:
        for i in dir_:
            os.chdir(i)
            logging.info("{}".format(os.getcwd()))
            parse_dir(val, func_to_exec, f_type)
            os.chdir('../')
    if file_:
        for i in file_:
            logging.info("{}\\{}".format(os.getcwd(), i))    
            func_to_exec(i, val)
        return 1
    return 1


func = find_words
parse_dir(keyword, func, file_type)