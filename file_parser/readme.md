## File Name: file_parser.py

### Usage
1. search
A user can search a keyword in all the files in the current directory. The file format for the search should be input in the script.
The script will search through all the files in the specified format in the parent directory as well as in the child directory.

**Example:** file_parser.py --keyword "honey" --format txt
The script will search all the files with '.txt' extension and print the results in terminal. It will also log the results in a file.

### Output
* file_parser.log -> A log file will be generated with the parameters used for the search. The directories that were searched will 
also be shown in the log file.
* console ouput -> If a match is found then the results will be printed on the console. The file name and the line number will also be
printed.
