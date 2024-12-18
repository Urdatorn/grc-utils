'''
/utils/filter_dichrona.py

Filter for tokens which
    - contain at least one DICHRONON the length of which is not given by the accentuation rules:
        - the two halfs of the σωτῆρᾰ-rule (for properispomena and paroxytones respectively)
        - the short ultima of proparoxytones (a corollary of sorts, if you wish, of the Law of Limitation)

THe DICHRONA set (viz. dichrona.py) already only contains true "dichronic" vowels, i.e. letters that may hide quantity.
The following α, ι and υ are excluded: 
- capitals without spiritus (can't appear in AG!)
- iota-subscriptum forms (always long)
- all macronized forms (after all, they are already disambiguated!)
- circumflexes (always long)

Note concerning the logical relationship between the five accentuation word classes and dichrona:
    OXYTONE implies nothing without context (cf. Ἀλκμάν, -ᾶνος)
    PAROXYTONE with ≥3 syllables still does NOT imply long vowel in ultima, because not all accents are recessive (cf. pf. ppc. λελῠμένος)
    However paroxytone + long penultima implies short ultima (as per the σωτῆρα-rule)
    PROPAROXYTONE implies that the vowel in the ultima is short, except for the πόλις declination's εως, which however has no DICHRONA.
    PERISPOMENON implies that the vowel in the ultima is long (as all vowels with circumf.)
    PROPERISPOMENON implies that the vowel in the ultima is short (as per the σωτῆρα-rule) and that the vowel in the penultima is long (as all vowels with circumf.)
'''
import re
import unicodedata

from .utils import oxia_to_tonos, open_syllable
from .dichrona import DICHRONA
from .erics_syllabifier import patterns, syllabifier
from .longa import longa_set

# ============================
# Syllable Positions 
# ============================

# ultima
# penultima

def ultima(word):
    '''
    >> ultima('ποτιδέρκομαι')
    >> μαι
    '''
    list_of_syllables = syllabifier(word)
    ultima = list_of_syllables[-1]

    return ultima

def penultima(word):
    '''
    >> penultima('ποτιδέρκομαι')
    >> κο
    '''
    list_of_syllables = syllabifier(word)
    penultima = list_of_syllables[-2]

    return penultima

# ============================
# Accent Word Classes
# ============================

# properispomenon
# paroxytone
# proparoxytone

def properispomenon(word):
    '''
    >> properispomenon('ὗσον')
    >> True
    '''
    list_of_syllables = syllabifier(word)
    if len(list_of_syllables) >= 2: 
        penultima = list_of_syllables[-2]
        circumflexes = r'[ᾶῆῖῦῶἇἆἦἧἶἷὖὗὦὧἦἧἆἇὧὦᾆᾇᾷᾖᾗᾦᾧῷῇ]'
        
        if re.search(circumflexes, penultima):
            return True
        else:
            return False
    else:
        return False
    
def paroxytone(word):
    '''
    >> paroxytone('λελῠμένος')
    >> True
    '''
    list_of_syllables = syllabifier(word)
    if len(list_of_syllables) >= 2: 
        penultima = list_of_syllables[-2]
        acutes = r'[άέήίύώἄἅἔἕὄὅἤἥἴἵὔὕὤὥΐΰᾄᾅᾴᾔᾕῄᾤᾥῴ]'
        
        if re.search(acutes, penultima):
            return True
        else:
            return False
    else:
        return False

def proparoxytone(word):
    '''
    >> proparoxytone('ποτιδέρκομαι')
    >> True
    '''
    list_of_syllables = syllabifier(word)
    if len(list_of_syllables) >= 3: 
        antepenultima = list_of_syllables[-3]
        acutes = r'[άέήόίύώἄἅἔἕὄὅἤἥἴἵὔὕὤὥΐΰᾄᾅᾴᾔᾕῄᾤᾥῴ]'
        
        if re.search(acutes, antepenultima):
            return True
        else:
            return False
    else:
        return False

# ============================================================
# Basic Properties Related to Syllable Weight and Vowel Length
# ============================================================

#   is_diphthong
#   has_iota_subscriptum
#   has_iota_adscriptum
#   word_with_real_dichrona
#   long_acute
#   short_vowel
#   make_only_greek

def is_diphthong(chars):
    ''' Expects two characters '''
    # Check if the input matches either of the diphthong patterns
    for pattern in ['diphth_y', 'diphth_i']:
        if re.match(patterns[pattern], chars):
            return True
    return False

def has_iota_subscriptum(char):
    ''' Expects one character '''
    subscr_i_pattern = re.compile(patterns['subscr_i'])
    # Check if the character matches the subscript iota pattern
    if subscr_i_pattern.match(char):
        return True
    return False

def has_iota_adscriptum(chars):
    ''' Expects two characters '''
    adscr_i_pattern = re.compile(patterns['adscr_i'])
    # Check if the two-character string matches the adscript iota pattern
    if adscr_i_pattern.match(chars):
        return True
    return False

def word_with_real_dichrona(string):
    """
    Determines if a given string contains at least one character from the DICHRONA set that 
        i) does not form a diphthong with its neighboring character (ι and υ can be both first and second elements, α only first), 
        ii) neither has nor is an iota adscriptum.
    These two conditions are checked in the same way, since iota adscripta are just long diphthongs. 
    (NB: DICHRONA already excludes circumflexes and iota subscripta.)

    Iterating through the input string, we hence check, for each char found in the DICHRONA set, 
    whether it forms a diphthong with its preceding or succeeding char.

    Returns:
    - bool: True if the string contains a real DICHRONA character; 
            False otherwise.
    """
    for i, char in enumerate(string):
        if char in DICHRONA:

            prev_pair = string[i-1:i+1] if i > 0 else ''
            next_pair = string[i:i+2] if i < len(string) - 1 else ''

            if (prev_pair and (is_diphthong(prev_pair) or has_iota_adscriptum(prev_pair))) or \
               (next_pair and (is_diphthong(next_pair) or has_iota_adscriptum(next_pair))):
                continue 

            return True

    return False

non_dichrona_long_acutes = r'[ήώἤἥὤὥᾄᾅᾴᾔᾕῄᾤᾥῴ]'

dichrona_long_acutes = {
    '\u1FB1\u0301' # macronized alpha with combining acute
    '\u1FD1\u0301' # macronized iota with combining acute
    '\u1FE1\u0301' # macronized ypsilon with combining acute
    "\u1f0c\u0304",  # Ἄ̄ Greek Capital Letter Alpha with Psili and Macron
    "\u1f3c\u0304",  # Ἴ̄ Greek Capital Letter Iota with Psili and Macron
    "\u1f0d\u0304",  # Ἅ̄ Greek Capital Letter Alpha with Dasia and Macron
    "\u1f3d\u0304",  # Ἵ̄ Greek Capital Letter Iota with Dasia and Macron
    "\u1f5d\u0304",  # Ὕ̄ Greek Capital Letter Upsilon with Dasia and Macron
    "\u03ac\u0304",  # ά̄ Greek Small Letter Alpha with Tonos and Macron
    "\u03af\u0304",  # ί̄ Greek Small Letter Iota with Tonos and Macron
    "\u03cd\u0304",  # ύ̄ Greek Small Letter Upsilon with Tonos and Macron
    "\u1f04\u0304",  # ἄ̄ Greek Small Letter Alpha with Psili and Macron
    "\u1f34\u0304",  # ἴ̄ Greek Small Letter Iota with Psili and Macron
    "\u1f54\u0304",  # ὔ̄ Greek Small Letter Upsilon with Psili and Macron
    "\u1f05\u0304",  # ἅ̄ Greek Small Letter Alpha with Dasia and Macron
    "\u1f35\u0304",  # ἵ̄ Greek Small Letter Iota with Dasia and Macron
    "\u1f55\u0304",  # ὕ̄ Greek Small Letter Upsilon with Dasia and Macron
    "\u0390\u0304",  # ΐ̄ Greek Small Letter Iota with Dialytika and Macron
    "\u03b0\u0304"   # ΰ̄ Greek Small Letter Upsilon with Dialytika and Macron
}

long_acutes = r'(' + '|'.join(re.escape(char) for char in dichrona_long_acutes) + r'|' + non_dichrona_long_acutes + r')'

def long_acute(syllable):
    '''
    Function needed to compute the paroxytone versiom of the σωτῆρα-rule.
    '''
    return bool(re.search(long_acutes, syllable))

def short_vowel(syllable):
    """
    Determines if a syllable is a short vowel.

    A syllable is considered short if it is not in the set of long vowels.

    Args:
        syllable (str): The syllable to check.

    Returns:
        bool: True if the syllable is short, False otherwise.
    """
    long_vowels_pattern = re.compile('|'.join(re.escape(v) for v in longa_set | {'η', 'ω'}))
    return not bool(long_vowels_pattern.search(syllable))

def make_only_greek(string):
    """
    Extracts only valid Greek substrings using defined patterns.
    NB: Removes space and punctuation!
    'ἱππιᾱτρῐκός hippiātrikós' -> 'ἱππιᾱτρῐκός'
    'δῆμος' -> 'δῆμος'
    '12345' -> ''
    'ἀγορά' -> 'ἀγορά'
    'Hello, world!' -> ''
    'ἔσπερος * & ^ %$#@!' -> 'ἔσπερος'
    'ᾄλφα βήτα' -> 'ᾄλφαβήτα'
    'αἰέν ἀριστεύειν!' -> 'αἰένἀριστεύειν'
    'μῆνιν ἄειδε θεά' -> 'μῆνινἄειδεθεά'
    """
    valid_pattern = re.compile('|'.join(patterns.values()))
    
    # Use re.finditer() for substring extraction
    greek_string = ''.join(match.group() for match in valid_pattern.finditer(string))
    return greek_string

# ===============================================================
# Advanced Properties Related to Syllable Weight and Vowel Length
# ===============================================================

#   paroxytone_short_ultima_with_dichronon_only_in_penultima
#   paroxytone_long_penultima_with_dichronon_only_in_ultima
#   properispomenon_with_dichronon_only_in_ultima
#   proparoxytone_with_dichronon_only_in_ultima

def paroxytone_short_ultima_with_dichronon_only_in_penultima(string):
    '''
    Is a word disambiguated by the σωτῆρᾰ-rule for penultimae?

    τὸ ἴον implies ῐ by the σωτῆρᾰ-rule, whereas τοῦ ἴου does not.
    '''
    if not word_with_real_dichrona(string):
        return False
    
    if not paroxytone(string):
        return False
    
    ultima_str = ultima(string)
    penultima_str = penultima(string)

    if not short_vowel(ultima_str):
        return False
    
    if not word_with_real_dichrona(penultima_str):
        return False
    
    pre_penultima = string[:-len(penultima_str)]

    if pre_penultima and word_with_real_dichrona(pre_penultima) or word_with_real_dichrona(ultima_str):
        return False
    
    return True


def paroxytone_long_penultima_with_dichronon_only_in_ultima(string):
    """
    Is a word disambiguated by the first half of the σωτῆρᾰ-rule for ultimae?

    Determines if a given string satisfies the following criteria:
    - The entire string is recognized by `word_with_real_dichrona`.
    - The accent type of the string is classified as paroxytone.
    - The penultima is long.
    - The ultima of the string is recognized by `word_with_real_dichrona`.
    - The part of the string before the ultima is NOT recognized by `word_with_real_dichrona`.
    """
    if not word_with_real_dichrona(string):
        return False
    
    if not paroxytone(string):
        return False
    
    ultima_str = ultima(string)
    penultima_str = penultima(string)
    
    if not long_acute(penultima_str):
        return False

    if not word_with_real_dichrona(ultima_str):
        return False

    pre_ultima = string[:-len(ultima_str)]

    if pre_ultima and word_with_real_dichrona(pre_ultima):
        return False

    return True

def properispomenon_with_dichronon_only_in_ultima(string):
    """
    Is a word disambiguated by the second half of the σωτῆρᾰ-rule for ultimae?

    Determines if a given string satisfies the following criteria:
    - The entire string is recognized by `word_with_real_dichrona`.
    - The accent type of the string is classified as properispomenon.
    - The ultima of the string is recognized by `word_with_real_dichrona`.
    - The part of the string before the ultima is NOT recognized by `word_with_real_dichrona`.
    
    The design importantly returns a word such as αὖθις.
    """
    # Check if the entire string is a word_with_real_dichrona
    if not word_with_real_dichrona(string):
        return False
    
    # Check if the accent type of the string is properispomenon
    if not properispomenon(string):
        return False
    
    # Extract the ultima of the string
    ultima_str = ultima(string)

    # Ensure the ultima itself is recognized by `word_with_real_dichrona`
    if not word_with_real_dichrona(ultima_str):
        return False

    # Determine the part of the string before the ultima
    pre_ultima = string[:-len(ultima_str)]

    # Ensure the part before the ultima is not recognized by `word_with_real_dichrona`
    # The pre_ultima conjunct checks whether the string is non-empty
    if pre_ultima and word_with_real_dichrona(pre_ultima):
        return False

    return True

def proparoxytone_with_dichronon_only_in_ultima(string):
    """
    Determines if a given string satisfies the following criteria:
    - The entire string is recognized by `word_with_real_dichrona` as containing a real dichrona.
    - The accent type of the string is classified as proparoxytone.
    - The ultima of the string is recognized by `word_with_real_dichrona`.
    - The part of the string before the ultima is not recognized by `word_with_real_dichrona`.

    Parameters:
    - string (str): The input string to be evaluated.

    Returns:
    - bool: True if the string satisfies all specified conditions; otherwise, False.
    """
    # Check if the entire string is a word_with_real_dichrona
    if not word_with_real_dichrona(string):
        return False
    
    # Check if the accent type of the string is PROPAROXYTONE
    if not proparoxytone(string):
        return False
    
    # Extract the ultima of the string
    ultima_str = ultima(string)

    # Ensure the ultima itself is recognized by `word_with_real_dichrona`
    if not word_with_real_dichrona(ultima_str):
        return False

    # Determine the part of the string before the ultima
    pre_ultima = string[:-len(ultima_str)]

    # Ensure the part before the ultima is not recognized by `word_with_real_dichrona`
    if pre_ultima and word_with_real_dichrona(pre_ultima):
        return False

    return True

# ============================
# The Actual Filter Functions
# ============================

# has_ambiguous_dichrona
# has_ambiguous_dichrona_in_open_syllables

def has_ambiguous_dichrona(string):
    """
    Identifies strings with *truly ambiguous dichrona*. Five criteria must be met:
        - identified by `word_with_real_dichrona` as containing a real dichronon.
        - not be identified by `paroxytone_short_ultima_with_dichronon_only_in_penultima`.
        - not be identified by `paroxytone_long_penultima_with_dichronon_only_in_ultima`.
        - not be identified by `properispomenon_with_dichronon_only_in_ultima`.
        - not be identified by `proparoxytone_with_dichronon_only_in_ultima`.
    """
    if string:
        # Cleanse the string
        string = make_only_greek(string)

        if not string:
            return False  # No valid characters left

        # Normalize the string and process
        tonos = oxia_to_tonos(string)
        token = unicodedata.normalize('NFC', tonos)

        # Checks
        word_check = word_with_real_dichrona(token)
        paroxytone_penultima_check = paroxytone_short_ultima_with_dichronon_only_in_penultima(token)
        paroxytone_ultima_check = paroxytone_long_penultima_with_dichronon_only_in_ultima(token)
        properispomenon_check = properispomenon_with_dichronon_only_in_ultima(token)
        proparoxytone_check = proparoxytone_with_dichronon_only_in_ultima(token)

        # Return True only if all criteria are met
        return word_check and not (paroxytone_penultima_check or paroxytone_ultima_check or properispomenon_check or proparoxytone_check)

    return False

def has_ambiguous_dichrona_in_open_syllables(string):
    '''
    Finds strings that have at least one syllable that is both open and has an ambiguous dichronon.

    The possibility that a word has several dichrona, one of which is open and determined by the accentuation rules
    and one of which is ambiguous and closed, precipitates a more complex logic.
    An example: Ᾰ̓́ργεῐ̈ (epic dative sing. of Ᾰ̓́ργος) has an open but decided dichronic ultima, and a closed earlier dichronon.
    Such a case should not be considered ambiguous.
    '''
    if not string:
        return False

    greek = make_only_greek(string)
    tonos = oxia_to_tonos(greek)
    normal = unicodedata.normalize('NFC', tonos)

    if not has_ambiguous_dichrona(normal):
        return False

    list_of_syllables = syllabifier(normal)
    total_syllables = len(list_of_syllables)

    dichronic_open_syllable_positions = [
        (-(total_syllables - i), syllable)  # Position from the end
        for i, syllable in enumerate(list_of_syllables)
        if word_with_real_dichrona(syllable) and open_syllable(syllable)
    ]

    if not dichronic_open_syllable_positions:
        return False
    
    if total_syllables < 2:
        return True
    
    ultima = list_of_syllables[-1]
    penultima = list_of_syllables[-2]

    for position, syllable in dichronic_open_syllable_positions:
        if position == -2 and paroxytone(normal) and short_vowel(ultima):
            continue  # Penultima disambiguated
        if position == -1:
            if paroxytone(normal) and long_acute(penultima):
                continue  # Ultima disambiguated
            if properispomenon(normal) or proparoxytone(normal):
                continue  # Ultima disambiguated
        return True

    return False
