from ClosestMatch import Trie
import time

test_trie = Trie()

print('LOADING TRIE')
with open('testing_insert_large') as input_file:
    start = time.time()
    for entry in input_file:
        test_trie.insert(entry.rstrip())
    end = time.time()
    print(f'loaded {test_trie.entries} words in {end - start:.4f}s')
print('\n')

print('EXECUTING QUERIES - find exact')
with open('testing_find') as input_file:
    for query in input_file:
        query = query.rstrip()
        start = time.time()
        ans = test_trie.find_exact(query)
        end = time.time()
        print(f'\'{query}\' was{"" if ans else " NOT"} found in {end - start:.4f}s')
print('\n')

print('EXECUTING QUERIES - find nearest')
with open('testing_find') as input_file:
    for query in input_file:
        query = query.rstrip()
        print(f'looking for \'{ query }\'')
        start = time.time()
        ans = test_trie.find_nearest(query)
        end = time.time()
        if ans:
            print(f'found {min(ans)} in {end - start:.4f}s')
        else:
            print(f'no matches found in {end - start:.4f}s')

