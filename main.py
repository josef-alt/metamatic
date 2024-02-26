# for retrieving metadata
from tinytag import TinyTag as tags

# for testing on random samples of larger directories
from random import sample

# for path operations and listdir
import os

extensions_file = 'files/extensions'
dictionary_file = 'files/dictionary'

def get_accepted_file_types():
    """Load accepted file extensions from file"""
    exts = []
    with open(extensions_file) as input_file:
        for extension in input_file:
            exts.append(extension.strip())
    return exts

def file_filter(file, accepted):
    """Determine whether or not to use selected file according to filters"""
    name, ext = os.path.splitext(file)
    return ext in accepted

def print_directory(dir, filters=[]):
    """Print out filtered directory contents for debugging purposes"""  
    dir_list = os.listdir(dir)
    for file in dir_list:
        if not filters or file_filter(file, filters):
            print(file)

if __name__ == '__main__':
    dir = '.'
	
    print('unfiltered')
    print_directory(dir)
    accepted_extensions = get_accepted_file_types()

    print('\nfiltered')
    print_directory(dir, accepted_extensions)