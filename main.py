# for retrieving metadata
from tinytag import TinyTag as tags

from ClosestMatch import Trie

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

def get_dictionary():
    """Load dictionary from file"""
    dictionary = Trie()
    print('LOADING DICTIONARY from', dictionary_file)
    with open(dictionary_file) as input_file:
        for entry in input_file:
            dictionary.insert(entry.rstrip().lower())
        print(f'loaded {dictionary.entries} words\n')
    return dictionary
    
def dictionary_insert(name, dict):
    """Update dictionary both in file and in memory"""
    print('adding', name, 'to dictionary')
    dict.insert(name)
    dict_file = open(dictionary_file, "a")
    dict_file.write(f'\n{name}')
    dict_file.close()

def prompt_user(suggestions, ask_dict=True):
    """Display a list of suggestions and prompt the user to select one."""
    num_suggestions = len(suggestions)
    if ask_dict:
        print('0 run against dictionary')
    for i in range(1, num_suggestions):
        print(i, suggestions[i])
        
    correct_spelling = str()
    found = False
    while not correct_spelling:
        response = input('selection or correct spelling (blank to keep):')
        if not response:
            print('keep', suggestions[0])
            correct_spelling = suggestions[0][1]
            found = False
        elif response.isnumeric():
            value = int(response)
            if value == 0 and ask_dict:
                correct_spelling = 'check_against_dictionary'
            elif value < 1 or value > num_suggestions:
                print('invalid response. try again') 
            else:
                correct_spelling = suggestions[value][1]
                found = True
        else:
            correct_spelling = response
            dictionary_insert(response, dictionary)
    return correct_spelling, found

def check_against_dictionary(entry, dictionary):
    assembled = str()
    for token in entry.split(' '):
        if not dictionary.find_exact(token):
            if input(f'is {token} correct?') == 'yes':
                assembled += ' ' + token
                dictionary_insert(token, dictionary)
            else:
                suggestions = dictionary.find_nearest(token)
                suggestions.insert(0, (-1, token))
                response, dummy = prompt_user(suggestions, False)
                assembled += ' ' + response
        else:
            assembled += ' ' + token
    return assembled

def check_spelling(entry, known, dictionary):
    """Compare entry to elements from known Trie with dictionary as fallback"""
    found_spellings = [ 'unknown' ]
    assembled = ''
    found = False
    
    found_spellings = known.find_nearest(entry)
    if not found_spellings:
        assembled = check_against_dictionary(entry, dictionary)
    elif min(found_spellings)[0] == 0:
        found = True
        assembled = min(found_spellings)[1]
    else:
        found_spellings.insert(0, (0, entry))
        assembled, found = prompt_user(found_spellings)
        if assembled == 'check_against_dictionary':
            print('passing to dict')
            assembled = check_against_dictionary(entry, dictionary)
        
    if not found:
        assembled = assembled.strip()
        known.insert(assembled)
        
    return assembled

def check_attribute(attr, trie, dict):
    ret = check_spelling(attr, trie, dict)
    print('found', ret, 'for', attr)
    # todo write corrected tag?

if __name__ == '__main__':
    dir = 'files'
    format = "%-35s%-35s"

    dictionary = get_dictionary()
    forest = {'artist': Trie(), 'comp': Trie(), 'album': Trie(), 'title': Trie() }
    
    dir_list = os.listdir(dir)
    file_filters = get_accepted_file_types()
    for file in dir_list:
        if file_filter(file, file_filters):
            meta = tags.get(os.path.join(dir, file))
            
            artist = (meta.artist or '').lower()
            album = (meta.album or '').lower()
            composer = (meta.composer or '').lower()
            title = (meta.title or '').lower()
            
            print(format % (artist, album))
            print(format % (composer, title))
            
            if meta.artist:
                print('checking artist')
                check_attribute(artist, forest['artist'], dictionary)
            if meta.album:
                print('checking album')
                check_attribute(album, forest['album'], dictionary)
            if meta.composer:
                print('checking composer')
                check_attribute(composer, forest['comp'], dictionary)
            if meta.title:
                print('checking title')
                check_attribute(title, forest['title'], dictionary)
            
            print()
            