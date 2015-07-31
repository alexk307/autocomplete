import unittest
import string
from autocomplete import WeightedTrie


class WeightedTrieTests(unittest.TestCase):

    def test_basic(self):
        test_word = 'autocomplete'
        trie = WeightedTrie()
        passage = 'Hello this is a test of the autocomplete functionality'
        trie.train(passage)
        results = trie.get_words(test_word[:2])

        self.assertTrue(test_word in results,
                        'Expected %s to be suggested in '
                        'autocomplete results' % test_word)

    def test_passage(self):
        passage = 'The third thing that I need to tell you is that ' \
                  'this thing does not think thoroughly.'
        trie = WeightedTrie()
        trie.train(passage)
        result1 = trie.get_words('thi')
        self.assertEqual('thing', result1[0],
                         'Expected `thing` to be most likely autocomplete '
                         'candidate, but got %s' % result1[0])

        expected_results1 = ['thing', 'think', 'third', 'this']
        self.assertEqual(set(result1), set(expected_results1),
                         'Expected results did not match given results.')

        result2 = trie.get_words('nee')
        self.assertEqual('need', result2[0],
                         'Expected `need` to be most likely autocomplete '
                         'candidate, but got %s' % result2[0])
        self.assertEqual(len(result2), 1,
                         'Expected 1 result, but got %s' % len(result2))

        result3 = trie.get_words('th')
        expected_results3 = ['that', 'thing', 'think', 'this',
                             'third', 'the', 'thoroughly']
        self.assertEqual(set(result3), set(expected_results3),
                         'Expected results did not match given results.')

    def test_case_insensitive(self):
        test_word = 'tEsT'
        trie = WeightedTrie()
        passage = 'Test TEst TESt TEST TesTing Testers Testing Tested Tests'
        trie.train(passage)
        autocomplete_prefix = test_word[:2]
        results = trie.get_words(autocomplete_prefix.lower())

        self.assertFalse(autocomplete_prefix in results,
                         'Expected %s not to be in results' % test_word)

        self.assertFalse(test_word in results,
                         'Expected %s not to be in results' % test_word)

        self.assertTrue(test_word.lower() in results,
                        'Expected %s to be suggested in '
                        'autocomplete results' % test_word.lower())

    def test_punctuation(self):
        passage = 'Hello, this is a test. Just a test? Yes just a test! ' \
                  'One, two, test, test. Tessa, Tesla, Testing, testers, tes'
        trie = WeightedTrie()
        trie.train(passage)
        results = trie.get_words('tes')

        for punc in string.punctuation:
            for candidate in results:
                self.assertFalse(punc in candidate,
                                 'Expected no punctuation in '
                                 'autocomplete results but found %s' % punc)

    def test_no_results(self):
        passage = 'This is a passage about nothing. Some words will not be' \
                  'in this passage.'
        trie = WeightedTrie()
        trie.train(passage)
        results = trie.get_words('xyz')
        self.assertFalse(results, 'Expected no autocomplete results, but '
                                  'was returned %s' % results)

    def test_invalid_input(self):
        trie = WeightedTrie()
        trie.train(None)
        results = trie.get_words('word')
        self.assertFalse(results, 'Expected no autocomplete results with no '
                                  'data in the trie, but returned: '
                                  '%s' % results)

        trie.train('Sometimes a user will make a mistake and will '
                   'ask to auto get_words two words at once')
        results = trie.get_words('two words')
        self.assertFalse(results, 'Expected no autocomplete results when '
                                  'requesting two words at once, but was '
                                  'returned %s' % results)
        results = trie.get_words('wil')
        self.assertTrue(results, 'Expected autocomplete results when '
                                 'requesting a prefix contained in the '
                                 'passage, instead got no results.')

    def test_weights(self):
        trie = WeightedTrie()
        passage = 'test test testing tester test testing test ' \
                  'testing tea team tear tee tent term terse'

        trie.train(passage)
        results = trie.get_words('te')
        self.assertEqual('test', results[0],
                         'Expected `test` to be most likely, '
                         'but `%s` was returned as most likely' % results[0])


if __name__ == '__main__':
    unittest.main()
