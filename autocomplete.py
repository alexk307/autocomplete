from Queue import LifoQueue
import string


class WeightedTrie:
    def __init__(self):
        self.children = {}
        self.weight = 0
        self.path = LifoQueue()
        self._autocomplete = {}

    def _get_prefix(self, prefix):
        """
        Traverse to the sub-trie from a given prefix
        :param prefix: a string of a prefix
        :return: a dict of letters to WeightedTrie objects
        """
        curr_node = self
        for letter in prefix:
            if letter in curr_node.children:
                curr_node = curr_node.children[letter]
            else:
                return {}
        return curr_node.children

    def _walk_prefix(self, prefix):
        """
        Recursively walk to trie from a given prefix and record possible
        candidate words for auto-completion
        :param prefix: a dict of letters to WeightedTrie objects
        """
        for child in prefix:

            # Push each child node
            self.path.put(child)

            # If the weight is greater than 0, we're at a leaf and the
            # path we took to get here forms an auto-complete candidate
            if prefix[child].weight > 0:
                self._autocomplete["".join(self.path.queue)] = \
                    prefix[child].weight

            # Recursively call this method on the children of this node
            self._walk_prefix(prefix[child].children)

            # Pop the stack after recursively visiting children
            if not self.path.empty():
                self.path.get()

    def _insert(self, word):
        """
        Inserts a word into the Trie
        :param word: The word to be inserted into the Trie
        """
        curr_node = self
        letter_count = 0

        for letter in word:
            letter_count += 1

            # Case-insensitive
            letter = letter.lower()

            if letter not in curr_node.children:
                curr_node.children[letter] = WeightedTrie()

            if letter_count == len(word):
                curr_node.children[letter].weight += 1
            else:
                curr_node = curr_node.children[letter]

    @staticmethod
    def _strip_punctuation(passage):
        """
        Removes punctuation from a blob of text
        :param passage: The passage to remove punctuation from
        :return: The same passage but without any punctuation
        """
        for punc in string.punctuation:
            if punc in passage:
                passage = passage.replace(punc, '')
        return passage

    def get_words(self, prefix):
        """
        Interface to auto-complete a prefix based on previous trained history
        :param prefix: The prefix to auto-complete
        :return: A dict of suffixes and their weight
        """
        prefix_trie = self._get_prefix(prefix)
        self._walk_prefix(prefix_trie)
        results = {}
        candidate_count = float(sum(self._autocomplete.values()))
        for candidate in self._autocomplete:
            results[prefix + candidate] = \
                self._autocomplete[candidate] / candidate_count
        results = sorted(results.items(), key=lambda x: x[1], reverse=True)

        # Reset variables used to store autocomplete data
        self.path.empty()
        self._autocomplete = {}

        # Only return the words in sorted order, not their weights
        return [result[0] for result in results]

    def train(self, passage):
        """
        Trains the algorithm on a passage
        :param passage: The passage to train the algorithm with
        """
        if passage:
            passage = WeightedTrie._strip_punctuation(passage)
            for word in passage.split(' '):
                self._insert(word)
