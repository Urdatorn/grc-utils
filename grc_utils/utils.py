'''
/utils.py
'''

import re
import unicodedata
from .macrons_map import macrons_map
from .vowels import vowel

# ============================
# Regexes
# ============================

base_alphabet = r'[ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρσςτυφχψω]' # 24 uppercase, 25 lowercase

# Miniscules with accents
acutes = r'[άέήίόύώΐΰἄἅἔἕἤἥἴἵὄὅὔὕὤὥᾄᾅᾴᾔᾕῄᾤᾥῴ]'
graves = r'[ὰὲὴὶὸὺὼῒῢἂἃἒἓἢἣἲἳὂὃὒὓὢὣᾂᾃᾲᾒᾓῂᾢᾣῲ]'
circumflexes = r'[ᾶῆῖῦῶῗῧἇἆἦἧἶἷὖὗὦὧἦἧἆἇὧὦᾆᾇᾷᾖᾗᾦᾧῷῇ]'
all_accents = f'[{acutes[1:-1]}{graves[1:-1]}{circumflexes[1:-1]}]' # sum of above 3

# Miniscules without accents
unaccented = r'[αεηιουωϊϋἀἁἐἑἠἡἰἱὀὁὐὑὠὡᾳᾀᾁῃᾐᾑῳᾠᾡ]' # 7 + 14 + 9

# All miniscules
all_vowels_lowercase = f'[{all_accents[1:-1]}{unaccented[1:-1]}]' # sum of above 2; NB: no iota adscript

# The simple macronizing diacritics (for all, see macrons_map.py)
longa_brevi = r'[ᾰᾸᾱᾹῐῘῑῙῠῨῡῩ]'

# ============================
# Utility Functions for Greek
# ============================

def no_macrons(string):
    """
    Replace characters in the input string based on the macrons_map dictionary.
    UPDATE 14/03: Handles both single characters and multi-character sequences.
    Christ, how could I have missed this?? Don't want to think about the bugs that might exist bc of this...
    """
    # Get all multi-character sequences from macrons_map
    multi_char_keys = sorted([k for k in macrons_map.keys() if len(k) > 1], key=len, reverse=True)
    
    # First replace all multi-character sequences
    result = string
    for key in multi_char_keys:
        result = result.replace(key, macrons_map[key])
    
    # Then handle single characters
    return ''.join(macrons_map.get(char, char) for char in result)

def base(char):
    '''
    Returns the base letter of a combined Unicode character by removing diacritics using NFD normalization.
    '''
    return unicodedata.normalize("NFD", char)[0]

def only_bases(word):
    '''
    E.g. ᾰ̓ᾱ́ᾰτᾰ returns ααατα.
    Dependencies: unicodedata and re
    '''
    return ''.join([base(char) for char in word if re.search(base_alphabet, base(char))])

# def open_syllable_simple(syllable):
#     '''
#     For most uses, see open_syllable_in_word.
#     '''
#     syllable = syllable.replace('_', '').replace('^', '')
#     base_form = only_bases(syllable)
#     if base_form and base_form[-1] in all_vowels_lowercase:
#         return True
#     else:
#         return False
    
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
    if base_form and base_form[-1] in all_vowels_lowercase:
        return True
    elif len(base_form) > 1: 
        if syllable == list_of_syllables[-1].replace('_', '').replace('^', '') and base_form[-2] in all_vowels_lowercase:
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

def contains_greek(text):
    """Check if a string contains at least one Greek Unicode character."""
    for char in str(text):
        if 'GREEK' in unicodedata.name(char, ''):
            return True
    return False

def oxia_to_tonos(string):
    mapping = {
        '\u1f71': '\u03AC',  # alpha
        '\u1f73': '\u03AD',  # epsilon
        '\u1f75': '\u03AE',  # eta
        '\u1f77': '\u03AF',  # iota
        '\u1f79': '\u03CC',  # omicron
        '\u1f7b': '\u03CD',  # upsilon
        '\u1f7d': '\u03CE'   # omega
    }
    return ''.join(mapping.get(char, char) for char in string)

def normalize_word(word):
    '''
    Tailors the unicodedata.normalize function for Ancient Greek
    by ensuring that Greek question marks are preserved and oxia accents are converted to tonos.
    '''
    normalized = unicodedata.normalize('NFC', word)

    # Greek question mark inadvertently normalizes to semicolon, so we need to explicitly restore it
    greek_question_mark = "\u037e"
    normalized = normalized.replace(";", greek_question_mark)

    tonos = oxia_to_tonos(normalized)
    return tonos