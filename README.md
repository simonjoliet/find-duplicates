# find_duplicates

The "find_duplicates.py" script is a command-line utility that takes a directory path as an argument and finds duplicate files within that directory and its subdirectories. The script uses SHA256 hashing to detect duplicate files and writes the results to a CSV file named "duplicates.csv".

*Requirements*
Python 3.6 or higher
The hashlib and csv modules.

*How to use*
To use this script, you need to provide the path to the directory you want to search for duplicates.
Usage: python find_duplicates.py <directory>

*How it works*
The script recursively traverses the provided directory and subdirectories and uses the SHA256 hash of the file contents to identify duplicate files. If the hash of a file matches a hash that has already been seen, the file is considered a duplicate.

If the size of the existing file is larger than 10KB, the script will write the details of the new and existing files to a CSV file named "duplicates.csv". The script also sorts the duplicates in the CSV file by file size, from largest to smallest.

The script prints a message indicating the location of the CSV file with the list of duplicate files.

*Disclaimer*
The script doesn't actually delete the duplicate files, it just writes the details of the files to the CSV file. It's up to the user to decide what to do with the duplicate files.
