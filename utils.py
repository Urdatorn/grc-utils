'''
/utils.py
'''

import re
import unicodedata
from utils.macrons_map import macrons_map

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

    Args:
        string (str): The input string to process.

    Returns:
        str: The string with substitutions applied.
    """
    # Use a list comprehension to replace each character if it exists in macrons_map
    return ''.join(macrons_map.get(char, char) for char in string)

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

def open_syllable(syllable):
    '''
    Boolean!
    '''
    base_form = only_bases(syllable)
    if base_form and base_form[-1] in all_vowels_lowercase:
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

