"""
This python script is used to perform certain operations as listed below. 
This script will look at target directory (and its children), and performs the operation on the files.
The output will be displayed on the console and also, an output log will be created.

__author__  = "Rahul B Thomas"
__status__  = "Development"
__date__    = "06-Apr-2021"

CODE_STRUCTURE
Class: xFinder()
Class_Functions:
|___init__(parameters): Pass the parameters and init the class object.
|_print_parameters() -> Prints the keyword to be searched, file type and the working Directory
|_find_words(f_name) -> Search for the keyword in file 'f_name'
|_replace_word(f_name) -> Search and replace the keyword in file 'f_name'
|_rename_file(f_name) -> Rename file 'f_name' based on 'type' parameter
|_parse_dir() -> Function to start the required operation in the target directory

SUPPORTED_OPERATIONS:
1. search -> search for a key word in the mentioned file type
[CMD] python file_parser.py --search keyword --target_dir <target_dir> --file_format txt

2. replace -> Replace a keyword in a file with another word. Works with search operation.
[CMD] python file_parser.py --search keyword --replace_by value --target_dir <target_dir> --file_format txt

3. rename -> rename [postfix, suffix, subs(titude)] files based on file type.
[CMD] python file_parser.py --rename prefix Logs --target_dir <target_dir>
[CMD] python file_parser.py --rename suffix documentation --target_dir <target_dir>
[CMD] python file_parser.py --rename subs logs test_logs --target_files <file1 file2 ... file_n>

"""

import os, re, sys
import logging
import argparse

parameters = {
    'f_op': 'search',
    'f_type': 'txt',
    'search': {'val_1': 'val'},
    'replace': {'val_1': '', 'val_2':''},
    'rename': {'type':'', 'val_1':'', 'val_2':''},
    'target_dir': os.getcwd(),
    'target_files': [],
    'dir_exp': ['.git'],
    'file_exp': ['.gitignore'],
    'cmd-line': ''
}

class xFinder():
    
    def __init__(self, parameters):
        """Init class object with the parameters

        Args:
            parameters (dict): A dict having all the parameters required for the operation (search/rename)
        """
        self.hits = 0
        self.target_dir = parameters['target_dir']
        self.target_files = parameters['target_files']
        self.op = parameters['f_op']

        # Get the file name for logging purpose
        self.file_name = os.path.basename(__file__)
        self.log_name = "{}.log".format(self.file_name[:-3])
        logging.basicConfig(filename=self.log_name, filemode='w', format='%(asctime)s - %(message)s', \
            datefmt='%d-%b-%Y %H:%M:%S', level=logging.DEBUG)
        #logging.info('\n')
        logging.info("Log for File: {}".format(self.file_name))
        logging.info("[CMD] {}".format(parameters['cmd-line']))
        global log_dest
        log_dest = "{}\\{}".format(os.getcwd(), self.log_name)

        os.chdir(self.target_dir)

        # Declare the dir/file exceptions
        self.dir_exceptions = parameters['dir_exp']
        self.file_exceptions = parameters['file_exp'] + [self.log_name]

        self.file_type = parameters['f_type']

        logging.info("OPERATION= " + str.upper(self.op))

        if self.op == 'search':
            self.keyword = parameters[parameters['f_op']]['val_1']
            logging.info("KEYWORD=\"{}\"".format(self.keyword))
            
        elif self.op == 'replace':
            self.keyword = parameters[parameters['f_op']]['val_1']
            self.replace_value = parameters[parameters['f_op']]['val_2']
            logging.info("KEYWORD=\"{}\"\nREPLACE_WITH: \"{}\"".format(self.keyword, self.replace_value))
        
        elif self.op == 'rename':
            self.rename = parameters[parameters['f_op']]
            if self.rename['type'] == 'subs':
                logging.info("Type=\"substitute old={} with new={}\"".format(self.rename['type'],self.rename['val_1'],self.rename['val_2']))
            else:
                logging.info("Type=\"{} using {}\"".format(self.rename['type'],self.rename['val_1'],self.rename['val_2']))
        
        logging.info("FILE_TYPE=\".{}\"".format(self.file_type))
        logging.info("TARGET_DIRECTORY= {}".format(self.target_dir))
        if self.target_files:
            logging.info("TARGET_FILES: {}".format(', '.join([x for x in self.target_files])))

    def print_parameters(self):
        """ Function to print the parameters """
        if self.op == 'search':
            print("PARAMETERS\nOPERATION: {}\nKEYWORD: \"{}\"\nFILE_TYPE: .{}".format(str.upper(self.op),\
                self.keyword, self.file_type))
        
        elif self.op == 'replace':
            print("PARAMETERS\nOPERATION: {}\nKEYWORD: \"{}\"\nREPLACE BY: \"{}\"\nFILE_TYPE: .{}".format(str.upper(self.op),\
                self.keyword, self.replace_value, self.file_type))
        
        elif self.op == 'rename':
            if self.rename['type'] in ['prefix', 'suffix']:
                print("PARAMETERS\nOPERATION: {}\nTYPE: {}\nSTRING: {}\nFILE_TYPE: .{}".format(str.upper(self.op),\
                    self.rename['type'], self.rename['val_1'], self.file_type))
            elif self.rename['type'] == 'subs':
                print("PARAMETERS\nOPERATION: {}\nTYPE: {}\nSTRING: {} \nREPLACE BY: {}\nFILE_TYPE: .{}".\
                    format(str.upper(self.op), self.rename['type'], self.rename['val_1'], self.rename['val_2'], self.file_type))
        print("Target_Directory: {}\n".format(self.target_dir))

    def find_words(self, f_name):
        """Function to search keyword in file. Substrings are also included

        Args:
            f_name (file name): File name passed for searching keyword
        
        Returns:
            hits [int]: No. of times the keyword is found
        """
        f1 = open(f_name, 'r')
        # Pattern to find 3 words before and after the keyword
        patt = r"((?:[\S]+\s+|[\w]+){0,3})"+self.keyword+ r"((?:[\w]+|\s+[\S]+){0,3})"
        l_no=0
        hits=0
        for line in f1:
            l_no += 1 # For line numbers
            z = re.search(patt, line)
            if z:
                to_print = str(self.keyword).join( list(z.groups()) )
                print("{}\\{} -> MATCH FOUND for \"{}\" -> Line {}: {}".format(os.getcwd().replace(self.target_dir,'.'), \
                    f_name, self.keyword, l_no, to_print))
                logging.info("{}\\{} -> MATCH FOUND for \"{}\" -> Line {}: {}".format(os.getcwd(), \
                    f_name, self.keyword, l_no, to_print))
                hits += 1
        f1.close()
        return hits
    
    def replace_word(self, f_name):
        """Function to replace keyword with a new word in files

        Args:
            f_name (file name): File name passed for searching keyword

        Returns:
            hits [int]: No. of times the keyword gets replaced
        """
        f1 = open(f_name, 'r')
        split_fname = re.search('(.*)(\.[\w]*)$', f_name).groups()
        temp_file = "{}_{}_{}{}".format( split_fname[0], 'replaced', self.replace_value, split_fname[1])
        f2 = open(temp_file,'w')
        l_no=0
        line_list=[]
        hits=0
        for line in f1:
            l_no += 1
            patt = r"\b{}\b".format(self.keyword)
            if re.search(patt, line):
                #line_to_write = line.replace(self.keyword, self.replace_value)
                line_to_write = re.sub(patt, self.replace_value, line)
                f2.write(line_to_write)
                line_list.append(l_no)
                hits += 1
            else:
                f2.write(line)
        
        f1.close()
        f2.close()
        
        if line_list:
            print("{}\\{} -> CREATED {}\nREPLACED \"{}\" with \"{}\" in LINES: {}".format(os.getcwd().replace(self.target_dir,'.'), \
                f_name, temp_file,self.keyword, self.replace_value, ' '.join([str(x) for x in line_list])))
            logging.info("{}\\{} -> CREATED {}\nREPLACED \"{}\" with \"{}\" in LINES: {}".format(os.getcwd(), f_name, \
                temp_file, self.keyword, self.replace_value, ' '.join([str(x) for x in line_list])))
            self.file_exceptions.append(temp_file)
        else:
            os.remove(temp_file)
        
        return hits

    def rename_file(self, f_name):
        """Function to rename file

        Args:
            f_name (file name): File to be renamed (prefix, suffix, subs(titute))

        Returns:
            [int]: 1 if file is renamed, else 0
        """
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
            return 1
        return 0

    def parse_dir(self):
        """ Function (recursive) to parse the directories and find files with the given format. 
            Requires f_operation that defines the type of operation to be performed """
        elements = os.listdir()
        
        func_dict = {'search': self.find_words,
                    'replace': self.replace_word,
                    'rename': self.rename_file}
        try:
            func_to_exec = func_dict[self.op]
        except :
            print("[ERROR]: Operation \"{}\" is not valid".format(self.op))
            logging.info("[ERROR]: Operation \"{}\" is not valid".format(self.op))
            sys.exit(1)

        dir_ = [x for x in elements if (os.path.isdir(x) and x not in self.dir_exceptions)]
        file_ = [x for x in elements if (os.path.isfile(x) and x.endswith(self.file_type))]
        
        # Check if the files in the current dir matches the target files (if any)
        if self.target_files:
            file_ = [x for x in file_ if x in self.target_files]

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
                if i not in self.file_exceptions:
                    logging.info("{}\\{}".format(os.getcwd(), i))    
                    self.hits += func_to_exec(i)
        if os.getcwd() == self.target_dir:
            logging.info("Total no. of hits: {}\n\n".format(str(self.hits)))
        return self.hits


# Add support for command line arguments
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("--search", dest='search', \
    help="Keyword to search in files. Returns substring matches.\
        \nUsage: --search \"keyword\"")

parser.add_argument("--replace_by", dest='replace',\
    help="Value to replace the keyword with in the files. This will not replace substrings.\
        \nUasge: --replace \"value\"")

parser.add_argument("--rename", dest='rename', nargs='*', \
    help="Rename files flag. Usage:\
        \n1. --rename prefix str_1 -> Prefix all file names in target. \
        \n2. --rename suffix str_1 -> Suffix str_1 at the end of the filename. \
        \n3. --rename subs old_str new_str\' -> Substitue a part of the file name.")
parser.add_argument("--file_format", dest='f_format', help="File format to be use in operation")
parser.add_argument("--file_excep", dest='file_excep', help="Files to be exempted from operation.\
    \nUsage: --file_excep file_1 file_2 ... file_n", nargs='*')
parser.add_argument("--dir_excep", dest='dir_excep', help="Directories to be exempted from operation\
    \nUsage: --dir_excep dir_1 dir_2 ... dir_n", nargs='*')
parser.add_argument("--target_dir", dest='target_dir', help="Directory to perform the operation")
parser.add_argument("--target_files", dest='target_files', nargs='*', \
    help="Directory to perform the operation")

args = parser.parse_args()

# Update the paramters to the variables
parameters['cmd-line'] = ' '.join(sys.argv)
parameters['f_type'] = args.f_format if args.f_format else parameters['f_type']

parameters['dir_exp'] = parameters['dir_exp'] + args.dir_excep \
    if args.dir_excep else parameters['dir_exp']

parameters['file_exp'] = parameters['file_exp'] + args.file_excep \
    if args.file_excep else parameters['file_exp']

parameters['target_dir'] = args.target_dir if args.target_dir else parameters['target_dir']
parameters['target_files'] = parameters['target_files'] + args.target_files \
    if args.target_files else parameters['target_files']

print("")
if args.search:
    if args.replace:
        parameters['f_op'] = 'replace'
        parameters['replace']['val_1'] = args.search
        parameters['replace']['val_2'] = args.replace
    else:
        parameters['f_op'] = 'search'
        parameters['search']['val_1'] = args.search
elif args.replace:
    print("[ERROR]: REPLACE NOT PERMITTED SINCE SEARCH KEYWORD IS NOT PROVIDED")
    sys.exit(1)
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
hits = test.parse_dir()

print("\nTotal no. of hits: "+ str(hits))
print("LOG AT: {}".format(log_dest))
