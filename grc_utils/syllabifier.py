'''
divides the greek into syllables (adapted from DionysiusRecomposed)

1) all double consonants and mutae-cum-liquidae are treated as closed (made for tragedy), i.e.
>>syllabifier('πατρός')
>>['πατ', 'ρός']
>>syllabifier('ἄμμι')
>>['ἄμ', 'μι']

2) handles adscripts, e.g.
>>syllabifier('δεινῆι')
>>['δει', 'νῆι']

NOTE requires corpus normalized to not include the oxia variants of άέήίόύώ, only tonos
NOTE since wiktionary has macrons, I added vowels with macra and brevia from macrons_map.py

TODO Add option for comic homosyllabic mutae cum liquidae.
TODO 27/3 -25 I'm getting some shitty split diphthongs like: [(-4, 'δα'), (-3, 'ρε'), (-2, 'ῖ'), (-1, 'ος')]

BUG

Why does τοῖος· ἀλλ give ['τοῖ', 'ος· ', 'ἀλλ'] and not the correct ['τοῖ', 'ο', 'ς· ἀλλ']?
Note that "τοῖος ἀλλ" correctly gives ['τοῖ', 'ο', 'ς ἀλλ'],
while "τοῖος·ἀλλ" gives the error ['τοῖ', 'ος·', 'ἀλλ'],
so clearly the culprit is the MIDDLE DOT.

Debug output:
Normalized text: τοῖος· ἀλλ
Divided text: ['τ', 'ο', 'ῖ', 'ο', 'ς· ', 'ἀ', 'λ', 'λ']
Joined text: τ⋮ο⋮ῖ⋮ο⋮ς· ⋮ἀ⋮λ⋮λ
Syllabified text: ['τ', 'οῖ', 'ος· ', 'ἀλλ']
Reshuffled text: ['τ', 'οῖ', 'ος· ', 'ἀλλ']
Final reshuffled text: ['τ', 'οῖ', 'ος· ', 'ἀλλ']
['τοῖ', 'ος· ', 'ἀλλ']
'''

import re
import unicodedata

from .lower_grc import VOWELS_LOWER_TO_UPPER
from .macrons_map import macrons_map
from .utils import normalize_word
from .vowels import vowel

SHORT = '̆'
LONG = '̄'

# ============================
# Prepare Character Patterns
# ============================

macronized_vowels = list(macrons_map.keys())  # Contains both upper and lower case vowels with macrons
unmacronized_vowels = list('αεηιουωἀἁἐἑἠἡἰἱὀὁὐὑὠὡάὰέὲήὴόὸίὶὺύώὼ'
                          'ἄἅἔἕὄὅὂὃἤἥἴἵὔὕὤὥἂἃἒἓἢἣἲἳὒὓὢὣ'
                          'ᾶῆῖῦῶἇἆἦἧἶἷὖὗὦὧϋϊΐῒϋῢΰῗῧ')

# Combine initial vowel sets and expand with uppercase forms
initial_vowels = set(macronized_vowels + unmacronized_vowels)
all_vowels_expanded = set()
for char in initial_vowels:
    all_vowels_expanded.add(char)
    if char in VOWELS_LOWER_TO_UPPER:
        all_vowels_expanded.add(VOWELS_LOWER_TO_UPPER[char])
all_vowels = '(' + '|'.join(re.escape(char) for char in all_vowels_expanded) + ')' + f'[{SHORT}{LONG}]?'

#   - NB: regexes of several combining characters together like '\u03B1\u0306' and '\u0391\u0306' must use alternation, i.e. ( | )
patterns = {
    'diphth_y': r'(α|ε|η|ο|Α|Ε|Η|Ο)(ὐ|ὔ|υ|ὑ|ύ|ὖ|ῦ|ὕ|ὗ|ὺ|ὒ|ὓ)',
    'diphth_i': r'(α|ε|υ|ο|Α|Ε|Υ|Ο)(ἰ|ί|ι|ῖ|ἴ|ἶ|ἵ|ἱ|ἷ|ὶ|ἲ|ἳ)',
    'adscr_i': r'(α_|η|ω|ἀ|ἠ|ὠ|ἁ|ἡ|ὡ|ά|ή|ώ|ὰ|ὴ|ὼ|ᾶ|ῆ|ῶ|ὤ|ὥ|ὢ|ὣ|ἄ|ἅ|ἂ|ἃ|ἤ|ἥ|ἣ|ἢ|ἦ|ἧ|ἆ|ἇ|ὧ|ὦ)(ι)', # 'αι' can be dipth or adscr. since diph is commoner, we default to that
    'subscr_i': r'[ᾄᾂᾆᾀᾅᾃᾇᾁᾴᾲᾷᾳᾔᾒᾖᾐᾕᾓᾗᾑῄῂῃῇᾤᾢᾦᾠᾥᾣᾧᾡῴῲῷῳ]', # note [] for single chars. 36 chars
    'stops': r'[ϝβγδθκπτφχϜΒΓΔΘΚΠΤΦΧ]',
    'liquids': r'[λρῤῥΛῬ]',
    'nasals': r'[μνΜΝ]',
    'double_cons': r'[ζξψΖΞΨ]',
    'sibilants': r'[σςΣ]',
    'vowels': all_vowels
}

# ============================
# Auxiliary Functions
# ============================

def divide_into_elements(text):
    '''
    Draws on the patterns dictionary to divide the text into elements.
    Keeps markup characters (^ and _) with their preceding character.
    Also keeps combining diacritics with their base characters.
    Attaches any Greek punctuation at the very start of the string
    to the first syllable instead of storing it separately.
    '''
    # First decompose the text to handle combining diacritics properly
    decomposed = unicodedata.normalize('NFD', text)
    
    elements = []
    i = 0
    greek_punctuation = r"""[‘’'\u0387\u037e\u00b7.,!?;:"()\[\]\{\}<>\-—…\n«»†×⏑⏓–]"""

    # --- NEW: capture all leading punctuation and hold it in a buffer
    leading_punct = ""
    while i < len(decomposed) and re.match(greek_punctuation, decomposed[i]):
        leading_punct += decomposed[i]
        i += 1

    while i < len(decomposed):
        # If we're at a base character, collect all its combining marks
        if unicodedata.category(decomposed[i]).startswith('L'):
            # Get the base character
            base_char = decomposed[i]
            i += 1
            # Collect all combining marks
            combining_marks = ''
            while i < len(decomposed) and unicodedata.category(decomposed[i]).startswith('M'):
                combining_marks += decomposed[i]
                i += 1
            
            # Try to match the recomposed character (base + combining marks)
            recomposed = unicodedata.normalize('NFC', base_char + combining_marks)
            matched = False
            for pattern in patterns.values():
                match = re.match(pattern, recomposed)
                if match:
                    matched = True
                    element = recomposed
                    # Attach any buffered leading punctuation to this *first* element
                    if leading_punct:
                        element = leading_punct + element
                        leading_punct = ""  # clear buffer
                    
                    # Check for markup after the matched element
                    if i < len(decomposed) and decomposed[i] in '^_ ':
                        element += decomposed[i]
                        i += 1
                    elements.append(element)
                    break
            
            if not matched:
                element = recomposed
                if leading_punct:
                    element = leading_punct + element
                    leading_punct = ""
                elements.append(element)
        
        # Check for Greek punctuation
        elif re.match(greek_punctuation, decomposed[i]):
            # If we have punctuation, attach to previous element
            if elements:
                elements[-1] += decomposed[i]
            else:
                # If no element yet, keep buffering as "leading"
                leading_punct += decomposed[i]
            i += 1
        
        # Handle spaces or markup characters
        elif decomposed[i] in '^_ ':
            if elements:
                elements[-1] += decomposed[i]
            else:
                # Still no element, attach to leading_punct
                leading_punct += decomposed[i]
            i += 1
        else:
            if not unicodedata.category(decomposed[i]).startswith('M'):
                element = decomposed[i]
                if leading_punct:
                    element = leading_punct + element
                    leading_punct = ""
                elements.append(element)
            i += 1

    return elements

def is_vowel(element):
    # Strip markup characters for pattern matching
    clean_element = element.replace('^', '').replace('_', '')
    return any(re.match(patterns[vowel_type], clean_element) for vowel_type in ['vowels', 'diphth_y', 'diphth_i', 'adscr_i', 'subscr_i'])

def is_consonant(element):
    # Strip markup characters for pattern matching
    clean_element = element.replace('^', '').replace('_', '')
    return any(re.match(patterns[consonant_type], clean_element) for consonant_type in ['stops', 'liquids', 'nasals', 'double_cons', 'sibilants'])

def syllabify(divided_text):
    '''
    This version looks ahead and if there is a vowel in the next element,
    it checks if it can form a diphthong with the current element that matches any of the four patterns.
    Thus we can syllabify e.g. 'Δα', 'ρεῖ', 'ος'.
    '''
    elements = divided_text.split('⋮')
    syllables = []
    current_syllable = ''
    i = 0
    while i < len(elements):
        element = elements[i]
        if is_vowel(element):
            # Check if this vowel can form a diphthong with the next element
            if i + 1 < len(elements) and is_vowel(elements[i + 1]):
                potential_diphthong = element + elements[i + 1]
                # Strip markup characters for pattern matching but preserve them in the result
                clean_element = element.replace('^', '').replace('_', '')
                clean_next = elements[i + 1].replace('^', '').replace('_', '')
                clean_diphthong = clean_element + clean_next
                
                if (re.match(patterns['diphth_y'], clean_diphthong) or 
                    re.match(patterns['diphth_i'], clean_diphthong) or
                    re.match(patterns['adscr_i'], clean_diphthong)):
                    # Combine into a diphthong
                    if current_syllable:
                        syllables.append(current_syllable)
                        current_syllable = ''
                    current_syllable = potential_diphthong
                    i += 2  # Skip the next element since it's part of the diphthong
                    continue
            # If no diphthong, treat as a standalone vowel
            if current_syllable:
                syllables.append(current_syllable)
                current_syllable = ''
            current_syllable = element
            i += 1
        else:
            # Add non-vowel elements to the current syllable
            current_syllable += element
            i += 1
    if current_syllable:
        syllables.append(current_syllable)

    syllables = [syl for syl in syllables if syl]  # UPDATE: Remove if not a real syllable (had errors here from Pindar)
    #syllables = [syl for syl in syllables if any(is_vowel(char) for char in syl)]  # UPDATE: Remove if not a real syllable (had errors here from Pindar)
    return syllables

def reshuffle_consonants(syllables):
    '''
    Reshuffles consonants between syllables.
    Now properly handles spaces and punctuation at syllable boundaries.
    '''
    reshuffled_syllables = []
    carry_over = ''

    for i in range(len(syllables)):
        syllable = syllables[i]

        # Separate any trailing whitespace or punctuation
        trailing_chars = ''
        while syllable and (syllable[-1].isspace() or syllable[-1] in r"""['''\u0387\u037e\u00b7.,!?;:"()\[\]\{\}<>\-—…\n«»†×⏑⏓–]"""):
            trailing_chars = syllable[-1] + trailing_chars
            syllable = syllable[:-1]

        # Handle start of line cases
        if i == 0 and not is_vowel(syllable[0]):
            vowel_index = next((index for index, char in enumerate(syllable) if is_vowel(char)), len(syllable))
            reshuffled_syllables.append(syllable[:vowel_index] + trailing_chars)
            carry_over = syllable[vowel_index:]
            continue

        # Prepend carry_over if present
        syllable = carry_over + syllable
        carry_over = ''

        # Handle syllable ending
        if i < len(syllables) - 1 and is_consonant(syllable[-1]):
            next_syllable = syllables[i + 1].rstrip()  # ignore trailing space in peek
            if is_vowel(next_syllable[0]):
                # Check if the last character is a double consonant
                if re.match(patterns['double_cons'], syllable[-1]):
                    carry_over = ''
                else:
                    carry_over = syllable[-1] + trailing_chars  # Move trailing chars with the consonant
                    trailing_chars = ''  # Clear trailing chars since they've been added to carry_over
                    syllable = syllable[:-1]
            else:
                # Complex case: multiple consonants at end
                consonant_cluster = ''.join(filter(is_consonant, syllable))
                if len(consonant_cluster) > 1:
                    carry_over = consonant_cluster[1:] + trailing_chars
                    trailing_chars = ''  # Clear trailing chars
                    syllable = syllable.replace(consonant_cluster, consonant_cluster[0], 1)

        reshuffled_syllables.append(syllable + trailing_chars)

    # Add any remaining carry_over to the last syllable
    if carry_over:
        reshuffled_syllables[-1] = reshuffled_syllables[-1] + carry_over

    return reshuffled_syllables

def final_reshuffle(reshuffled_syllables):
    final_syllables = []
    
    for i, syllable in enumerate(reshuffled_syllables):
        # Separate any trailing whitespace or punctuation
        trailing_chars = ''
        original_syllable = syllable
        while syllable and (syllable[-1].isspace() or syllable[-1] in r"""['''\u0387\u037e\u00b7.,!?;:"()\[\]\{\}<>\-—…\n«»†×⏑⏓–]"""):
            trailing_chars = syllable[-1] + trailing_chars
            syllable = syllable[:-1]
            
        # Check for multiple consonants at the end
        if syllable and i < len(reshuffled_syllables) - 1 and is_consonant(syllable[-1]):
            next_syllable = reshuffled_syllables[i + 1]
            # Count how many consonants are at the end
            consonant_count = 0
            while consonant_count < len(syllable) and is_consonant(syllable[-(consonant_count + 1)]):
                consonant_count += 1
            
            if consonant_count > 1:
                # Leave one consonant at end of current syllable, push the rest to next
                split_index = consonant_count - 1
                final_syllables.append(syllable[:-split_index] + trailing_chars)
                reshuffled_syllables[i + 1] = syllable[-split_index:] + next_syllable
            else:
                final_syllables.append(original_syllable)
        else:
            final_syllables.append(original_syllable)

    return final_syllables

def definitive_syllables(reshuffled_syllables):
    if not reshuffled_syllables:
        return reshuffled_syllables
    
    # If the first syllable is all consonants, join it with the second syllable
    if reshuffled_syllables[0] and not is_vowel(reshuffled_syllables[0][0]):
        if len(reshuffled_syllables) > 1:
            reshuffled_syllables[0] += reshuffled_syllables[1]
            reshuffled_syllables.pop(1)
    return reshuffled_syllables

# ============================
# Syllabifier
# ============================

def syllabifier(string, debug=False):
    '''
    all double consonants and mutae-cum-liquidae are treated as closed, i.e.
    >>syllabifier('πατρός')
    >>['πατ', 'ρός']

    string -> list
    '''
    if not string:
        return None

    normalized_text = normalize_word(string)
    if debug:
        print(f"Normalized text: {normalized_text}")
    divided_text = divide_into_elements(normalized_text)
    if debug:
        print(f"Divided text: {divided_text}")
    joined_text = '⋮'.join(divided_text)
    if debug:
        print(f"Joined text: {joined_text}")
    syllabified_text = syllabify(joined_text)
    if debug:
        print(f"Syllabified text: {syllabified_text}")
    reshuffled_text = reshuffle_consonants(syllabified_text)
    if debug:
        print(f"Reshuffled text: {reshuffled_text}")
    final_reshuffled_text = final_reshuffle(reshuffled_text)
    if debug:
        print(f"Final reshuffled text: {final_reshuffled_text}")
    definitive_text = definitive_syllables(final_reshuffled_text)

    return definitive_text