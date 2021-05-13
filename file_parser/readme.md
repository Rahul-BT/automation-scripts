## File Name: file_parser.py

## Operations
### 1. Search for a keyword
The user can search a keyword in all the files in the current directory and also in its child directories. The file format for the search can be specified (deafult is 'txt') in the command line. The script will search the keyword in all files in the specified format. File and directory exceptions are allowed.

Example 
 1. `python file_parser.py --search "honey" --file_format txt`
 2. `python file_parser.py --search "honey" --file_format txt --target_dir <target_path>`
 3. `python file_parser.py --search "honey" --file_format txt --file_excep file_1 file_2 ... file_n --dir_excep dir_1 dir2 ... dir_n`
    
### 2. Rename files
The user can use this script to rename files in the current directory and also in its child directories. The supported rename operations are 'prefix', 'suffix' and 'subs(titute)'. The file format can be specified (default is 'txt'). File and directory exceptions are allowed.
    
Example
 1. `python file_parser.py --rename prefix Log_file --file_format txt`
 2. `python file_parser.py --rename suffix document --file_format txt --target_dir <target_path>`
 3. `python file_parser.py --rename subs log Log_file --file_excep file_1 file_2 ... file_n --dir_excep dir_1 dir2 ... dir_n`    

## Output
* file_parser.log -> A log file will be generated with the parameters used for the search/rename operation. The directories that were searched will 
also be shown in the log file.
* console ouput -> If a match is found then the results will be printed on the console.

Use `python file_parser.py --help` for more information on command line arguments