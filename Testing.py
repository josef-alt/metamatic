from ClosestMatch import Trie

test_trie = Trie()
print('loading trie')
with open('testing_insert') as input_file:
	for entry in input_file:
		print('inserting', entry, end='')
		test_trie.insert(entry)
print('\n')

print('executing queries')
with open('testing_find_exact') as input_file:
	for query in input_file:
		if test_trie.find_exact(query):
			print('found', query, end='')
		else:
			print('did not find', query, end='')