from .utils import only_bases
from .vowels import vowel
from .vowels_long import long_set

def heavy(syllable):
    '''
    Input is considered in abstracto, and assuming no interplay with the following syllable.
    Final long dichrona must be followed by a "_" for the syllable to be considered heavy.
    >>> heavy("πὶς")
    True
    >>> heavy("πή")
    True
    >>> heavy("λε")
    False
    >>> heavy("α_")
    True
    >>> heavy("α")
    False
    '''
    
    syllable = syllable.replace('_', '').replace('^', '')
    base_form = only_bases(syllable)

    if not base_form:
        return False

    if vowel(base_form[-1]):
        return base_form[-1] in long_set | set('_')
    else:
        return True

def open_syllable_in_word(syllable, list_of_syllables):
    '''
    NOTE designed for words in abstracto:
    if applied word-by-word to words in synapheia like ἐλπὶς δὲ it will incorrely label -πὶς as open

    Designed to accomodate 
    - "True" for ultimae with single final consonant (i.e. open in abstracto and in hiatus), e.g. both syllables in ἰσχύς return True.
    - False for ultimae with any of the three double consonants 'ζ','ξ','ψ'.

    TODO problem with words where the ultima is identical to some earlier syllable
    '''
    syllable = syllable.replace('_', '').replace('^', '')
    base_form = only_bases(syllable)

    if base_form[-1] in {'ζ','ξ','ψ'}:
        return False
    if base_form and vowel(base_form[-1]):
        return True
    elif len(base_form) > 1: 
        if syllable == list_of_syllables[-1].replace('_', '').replace('^', '') and vowel(base_form[-2]):
            return True
    else:
        return False
    
def is_open_syllable_in_word_in_synapheia(syllable, list_of_syllables, next_word):
    '''
    Designed for words in verse synapheia, e.g. "ἐλπὶς ἀνθρώπου" = - u - - -
    
    >>> is_open_syllable_in_word_in_synapheia("πὶς", ["ἐλ", "πὶς"], "ἀνθρώπου"):
    >>> True

    '''
    syllable = syllable.replace('_', '').replace('^', '')
    final_syllable = list_of_syllables[-1].replace('_', '').replace('^', '')

    syll_base = only_bases(syllable)
    if not syll_base:
        return False

    if syll_base[-1] in {'ζ','ξ','ψ'}:
        return False
    
    if vowel(syll_base[-1]) or len(syll_base) == 1:
        return True

    # The only way a closed syll can be opened by synapheia
    # is if it's the ultima and the following word starts with a vowel:
    if syllable == final_syllable:
        if next_word and vowel(next_word[0]):
            return True
    else:
        return False