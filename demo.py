from autocomplete import WeightedTrie


def main():
    trie = WeightedTrie()
    try:
        while True:
            print '[1]: Train algorithm'
            print '[2] Auto-complete word'

            selection = raw_input()
            if selection == '1':
                print 'Enter passage. Press `return` when done training.'
                training_passage = raw_input()
                trie.train(training_passage)
            elif selection == '2':
                print 'Enter auto-complete candidate.' \
                      ' Press `return` when finished.'
                fragment = raw_input()
                results = trie.get_words(fragment)
                if len(results):
                    print 'Possible words to complete `%s` ' \
                          '(in order of confidence) are: %s' % \
                          (fragment, ", ".join(results))
                else:
                    print 'No previously seen words to complete `%s`' \
                          % fragment
            else:
                print 'Please select an option from the menu.'
    except KeyboardInterrupt:
        print 'Thanks for looking!'

if __name__ == '__main__':
    main()