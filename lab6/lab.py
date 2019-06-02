# NO ADDITIONAL IMPORTS!
from text_tokenize import tokenize_sentences


class Trie:
    def __init__(self):
        self.value = None
        self.children = {}
        self.type = None

    def __setitem__(self, key, value):
        """
        Add a key with the given value to the trie, or reassign the associated
        value if it is already present in the trie.  Assume that key is an
        immutable ordered sequence.
        """
        # Helper function 
        # get(or create) new node for next key character
        def find_new_node(children, key):
            # global helper function 
            # separate str and tuple types
            k_ = set_key_(key) 
            # check if key in children
            if k_ in children: 
                new_node = children[k_]   
            else: # add new node
                children[k_] = Trie() 
                new_node = children[k_]
            return new_node
        
        def assign_type_and_recurse(self, this_type, key, value):
            self.type = this_type 
            new_node = find_new_node(self.children, key)
            new_node.__setitem__(key[1:], value)    
        # End helper function
        
        this_type = type(key)
        if len(key) == 0:  # base case
            self.value = value
            self.type = this_type
        
        if self.type is None: # pass by, only assign the type
            assign_type_and_recurse(self, this_type, key, value)
        
        elif len(key) != 0: # has already inserted before and not the end node
            if not isinstance(key, self.type): # check type
                raise TypeError
            assign_type_and_recurse(self, this_type, key, value)

    def __getitem__(self, key):
        """
        Return the value for the specified prefix.  If the given key is not in
        the trie, raise a KeyError.
        """
        if not isinstance(key, self.type): # check if key type matches
            raise TypeError
        if len(key) == 0:  # base case: end node
            if self.value is None: # check if has value
                raise KeyError
            else:
                return self.value
        # recurrance
        else: 
            k_ = set_key_(key)
            if k_ not in self.children: # check if correct key each time
                raise KeyError
            else:
                new_node = self.children[k_]
                return new_node.__getitem__(key[1:])
        
    def __delitem__(self, key):
        """
        Delete the given key from the trie if it exists.
        """
        self.__setitem__(key, None)

    def __contains__(self, key):
        """
        Is key a key in the trie? return True or False.
        """
        if len(key) == 0:
            if self.value is not None:
                return True
            else:
                return False
        else:
            k_ = set_key_(key)
            if k_ not in self.children:
                return False
            else:
                new_node = self.children[k_]
                return new_node.__contains__(key[1:])
    
    def __iter__(self):
        """
        Generator of (key, value) pairs for all keys/values in this trie and
        its children.  Must be a generator!
        """
        def helper(trie, prefix):
            if trie.value is not None:
                yield (prefix, trie.value)

            for k, child in trie.children.items():
                yield from helper(child, prefix+k)

        if self.type == str:    
            return helper(self, '')
        else:
            return helper(self, ())

# Helper function
def set_key_(key):
    if isinstance(key, str):
        return key[0]
    else:
        return key[0],
            
def count_freq(text):
    ans = {}
    for i in text:
        if i not in ans:
            ans[i] = 1
        else:
            ans[i] += 1
    return ans

def assign_trie(text):
    freq = count_freq(text)
    t = Trie()
    for i in freq:
        t[i] = freq[i]
    return t
# End helper function
    
def make_word_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    words in the text, and whose values are the number of times the associated
    word appears in the text
    """
    tok_text = tokenize_sentences(text)
    to_words = []
    # get list of words
    for sub_text in tok_text:
        to_words += sub_text.split(' ') 
    t = assign_trie(to_words)
    return t

def make_phrase_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    sentences in the text (as tuples of individual words) and whose values are
    the number of times the associated sentence appears in the text.
    """
    tok_text = tokenize_sentences(text)
    # get list of tuples(sentences)
    tup_text = [tuple(i.split(' ')) for i in tok_text]
    t = assign_trie(tup_text)
    return t

# Helper function
def getnode(Trie, key):
    if not isinstance(key, Trie.type):
        raise TypeError
    if len(key) == 0:  # base case: no key branch
        return Trie
    else: # recurrance
        k_ = set_key_(key)
        if k_ not in Trie.children: # check if correct key each time
            raise KeyError
        else:
            new_node = Trie.children[k_]
            return getnode(new_node, key[1:])

def get_all_match(trie, prefix):
    try:
        spe_node = getnode(trie, prefix)
    except KeyError: # if prefix not match
        return []
    # get all possibility of prefix
#    print([(prefix+k,v) for k, v in spe_node] )
    return [(prefix+k,v) for k, v in spe_node] 
# End helper function
    
def autocomplete(trie, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring words that start with
    prefix.  Include only the top max_count elements if max_count is specified,
    otherwise return all.
    """
    all_match = get_all_match(trie, prefix)
    
    # not specify max_count or max_count is larger than output
    if max_count is None or max_count >= len(all_match):
        return get_keys(all_match)
    else:
        # sort all_match by freq
        sort_match = sort_by_value(all_match)
        return get_keys(sort_match[:max_count])

# Helper function
def get_edited(t, prefix):
    a_z = [chr(i) for i in range(ord('a'), ord('z')+1)]
    # edit 1: add one letter 
    possi = set()
    for le in a_z:
        for i in range(len(prefix)+1):
            possi.add(prefix[:i]+le+prefix[i:])
    # edit 2: remove one letter
    for i in range(len(prefix)):
        possi.add(prefix[:i] + prefix[i+1:])
    # edit 3: replace one letter
    for le in a_z:
        for i in range(len(prefix)):
            possi.add(prefix[:i]+le+prefix[i+1:])
    # edit 4: change two
    for i in range(len(prefix)-1):
        for j in range(i+1,len(prefix)):
            a = prefix
            possi.add(a[:i] + a[j]+ a[i+1:j]+a[i] + a[j+1:])
    valid_keys = set()
    for key in possi:
        if key in t:
            valid_keys.add(key)
    valid_edit = [] 
    for key in valid_keys:
        for k, v in t:
            if key == k:      
                valid_edit.append((k,v))
    return valid_edit

def sort_by_value(L):
    return sorted(L, key=lambda x: x[1], reverse=True)

def get_keys(L):
    return [k for k, v in L]

def get_distinct(L):
    set_ = set(L)
    ans = list(set_)
    return ans
# End helper function

def autocorrect(trie, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.
    """
    # do normal autocompltetion
    all_keys = autocomplete(trie, prefix, None)
    # already get enough guesses
    if max_count is not None and len(all_keys) >= max_count: 
        return autocomplete(trie, prefix, max_count)
    # do auto correction
    else:
        # get valid keys, frequency pairs
        valid_edit = get_edited(trie, prefix)
        # return all
        if max_count is None: 
            return get_distinct(all_keys + get_keys(valid_edit))
        # not enough guesses, need valid editions as compelement
        else: 
            # sort by frequency
            sorted_edit = sort_by_value(valid_edit)
            needed = max_count - len(all_keys)
            return get_distinct(all_keys + get_keys(sorted_edit[:needed]))

def word_filter(trie, pattern):
    """
    Return list of (word, freq) for all words in trie that match pattern.
    pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """
    def helper(trie, prefix, pattern):
        # base case
        if pattern == '*':
            if trie.value is not None:
#                print('final yield: ',prefix)
                yield (prefix, trie.value)
            
        if len(pattern) == 0 or trie.children == {}:
            
            if trie.value is not None:
#                print('final yield: ',prefix)
                yield (prefix, trie.value)
        # recurance
        if pattern[0] == '*':
            if len(pattern)==1:
                for le, c in trie.children.items():
                    print(le)
                    yield from helper(c, prefix+le, pattern)
            elif pattern[1] != '*':
                if pattern[1] in trie.children:
                    yield from helper(c, prefix+le, pattern)          
        elif pattern[0] == '?':
            for le, c in trie.children.items():
                yield from helper(c, prefix+le, pattern[1:])
        elif pattern[0] in trie.children:
            c = trie.children[pattern[0]]
            yield from helper(c, prefix+pattern[0], pattern[1:])
        else:
            yield ()
    print('helper: ',list(helper(trie, '', pattern)))
    return list(set([i for i in helper(trie, '', pattern) if i !=()]))
    
# you can include test cases of your own in the block below.
if __name__ == '__main__':
    pass
#    t = make_word_trie("bat bat bark bar")
#    res = autocorrect(t, "bar", 3)
#    print(res)
#    with open(os.path.join(TEST_DIRECTORY, 'testing_data', 'frankenstein.txt'), encoding='utf-8') as f:
#            text = f.read()
#    w = make_word_trie(text)
#    possi = get_edited(w, 'mon')
#    print(possi)
#    edit_match = []
#    for key in possi:  ### ????!!!!!
##        print(len(edit_match))
#        one = get_all_match(w, key)
#        bad = 'one' in [k for k, v in one]
#        print('-------')
#        print('key to try: ',key)
#        print('one' in [k for k, v in one])
#        print(one)
#        
#        if bad:
#            break
#        edit_match += get_all_match(w, key)
#    sorted_edit = sort_by_value(edit_match)
#    print(sorted_edit[:3])
    

#    print(get_all_match(w, 'mon'))
