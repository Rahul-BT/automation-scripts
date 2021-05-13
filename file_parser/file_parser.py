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

parameters = {
    'f_op': 'search',
    'f_type': 'txt',
    'search': {'val_1': ''},
    'rename': {'type':'', 'val_1':'', 'val_2':''},
    'target_dir': os.getcwd(),
    'dir_exp': ['.git'],
    'file_exp': ['.gitignore'],
    'cmd-line': ''
}

class xFinder():
    
    def __init__(self, parameters):

        self.target_dir = parameters['target_dir']
        self.op = parameters['f_op']
        self.target_dir = parameters['target_dir']

        # Get the file name for logging purpose
        self.file_name = os.path.basename(__file__)
        self.log_name = "{}.log".format(self.file_name[:-3])
        logging.basicConfig(filename=self.log_name, filemode='a', format='%(asctime)s - %(message)s', \
            datefmt='%d-%b-%Y %H:%M:%S', level=logging.INFO)
        logging.info("\n\n\nLog for File: {}".format(self.file_name))
        logging.info("[CMD] {}".format(parameters['cmd-line']))
        global log_dest
        log_dest = "{}\\{}".format(os.getcwd(), self.log_name)

        os.chdir(self.target_dir)

        # Declare the dir/file exceptions
        self.dir_exceptions = parameters['dir_exp']
        self.file_exceptions = parameters['file_exp'] + [self.log_name]

        self.file_type = parameters['f_type']

        if self.op == 'search':
            self.keyword = parameters[parameters['f_op']]['val_1']
            logging.info("OPERATION= {}\nKEYWORD=\"{}\"\nFILE_TYPE=\".{}\" \nTARGET_DIRECTORY: {}".\
            format(str.upper(self.op), self.keyword, self.file_type, self.target_dir))
            
        elif self.op == 'rename':
            self.rename = parameters[parameters['f_op']]
            logging.info("OPERATION= {}\nType=\"{} {} {}\"\nFILE_TYPE=\".{}\" \nTARGET_DIRECTORY: {}".\
            format(str.upper(self.op), self.rename['type'],self.rename['val_1'], self.rename['val_2'], \
                self.file_type, self.target_dir))
    # TODO:
    # Fix the print parametrs function, especially the rename part
    def print_parameters(self):
        """ Function to print the parameters """
        if self.op == 'search':
            print("PARAMETERS\nOPERATION: {}\nKEYWORD: \"{}\"\nFILE_TYPE: .{}".format(str.upper(self.op),\
                self.keyword, self.file_type))
        elif self.op == 'rename':
            if self.rename['type'] in ['prefix', 'suffix']:
                print("PARAMETERS\nOPERATION: {}\nTYPE: {}\nSTRING: {}\nFILE_TYPE: .{}".format(str.upper(self.op),\
                    self.rename['type'], self.rename['val_1'], self.file_type))
            elif self.rename['type'] == 'subs':
                print("PARAMETERS\nOPERATION: {}\nTYPE: {}\nSTRING: {} \nREPLACE BY: {}\nFILE_TYPE: .{}".\
                    format(str.upper(self.op), self.rename['type'], self.rename['val_1'], self.rename['val_2'], self.file_type))
        print("Target_Directory: {}\n".format(self.target_dir))
        #print("PARAMETERS\n{}".format(self.parameters))

    def find_words(self, f_name):
        """ Function to search the keyword in the files """
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
    
    def rename_file(self, f_name):
        split_fname = re.search('(.*)(\.[\w]*)$', f_name).groups()
        new_name = {
            'prefix': "{}_{}".format(self.rename['val_1'], f_name),
            'suffix': "{}_{}{}".format( split_fname[0], self.rename['val_1'], split_fname[1]),
            'subs': f_name.replace(self.rename['val_1'], self.rename['val_2'])
        }
        if f_name != new_name[self.rename['type']]:
            os.rename(f_name, new_name[self.rename['type']])
            logging.info("{}\\{} -> {}".format(os.getcwd(), f_name, new_name[self.rename['type']]))
            print("{}\\{} -> {}".format(os.getcwd(), f_name, new_name[self.rename['type']]))

    def parse_dir(self):
        """ Function (recursive) to parse the directories and find files with the given format. 
            Requires f_operation that defines the type of operation to be performed """
        elements = os.listdir()
        
        func_dict = {'search': self.find_words,
                    'rename': self.rename_file}
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
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--search", dest='search', \
    help="Keyword to search in files. \nUsage: --search \"keyword\"")
parser.add_argument("--rename", dest='rename', nargs='*', \
    help="Rename files flag. Usage:\
        \n1. --rename prefix str_1 -> Prefix all file names in target. \
        \n2. --rename suffix str_1 -> Suffix str_1 at the end of the filename. \
        \n3. --rename subs old_str new_str\' -> Substitue a part of the file name.")
parser.add_argument("--file_format", dest='f_format', help="File format to be use in operation")
parser.add_argument("--file_excep", dest='file_exc', help="Files to be exempted from operation.\
    Usage: [file1, file2, file3]")
parser.add_argument("--dir_excep", dest='dir_exc', help="Directories to be exempted from operation\
    Usage: [dir1, dir2, dir3]")
parser.add_argument("--target_dir", dest='target_dir', help="Directory to perform the operation")

args = parser.parse_args()

# Update the paramters to the variables
parameters['cmd-line'] = ' '.join(sys.argv)
parameters['f_type'] = args.f_format if args.f_format else parameters['f_type']

parameters['dir_exp'] = parameters['dir_exp']+ list(args.dir_exc.split()) \
    if args.dir_exc else parameters['dir_exp']

parameters['file_exp'] = parameters['file_exp']+ list(args.file_exc.split()) \
    if args.file_exc else parameters['file_exp']

parameters['target_dir'] = args.target_dir if args.target_dir else parameters['target_dir']

if args.search:
    parameters['f_op'] = 'search'
    parameters['search']['val_1'] = args.search
elif args.rename:
    parameters['f_op'] = 'rename'
    if args.rename[0] in ['prefix', 'suffix', 'subs']:
        parameters['rename']['type'] = args.rename[0]
        parameters['rename']['val_1'] = args.rename[1]
        parameters['rename']['val_2'] = args.rename[2] if len(args.rename)>2 else ''
    else:
        print("[ERROR]: RENAME TYPE \"{}\" NOT PERMITTED".format(args.rename[0]))
        sys.exit(1)

test = xFinder(parameters)

test.print_parameters()
test.parse_dir()
print("\nLOG AT: {}".format(log_dest))
