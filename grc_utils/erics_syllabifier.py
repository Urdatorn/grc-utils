'''
divides the greek into syllables (adapted from DionysiusRecomposed)
all double consonants and mutae-cum-liquidae are treated as closed (made for tragedy), i.e.
>>syllabifier('πατρός')
>>['πατ', 'ρός']
>>syllabifier('ἄμμι')
>>['ἄμ', 'μι']
'''

import re

from .macrons_map import macrons_map

# ============================
# Prepare Character Patterns
# ============================

# Albin:
# NB1: there was a bug, an ᾶ in the subscr_i 
# NB2: requires corpus normalized to not include the oxia variants of άέήίόύώ, only tonos
# NB3: since wiktionary has macrons, I added vowels with macra and brevia from macrons_map.py

macronized_vowels = list(macrons_map.keys())
unmacronized_vowels = '|'.join(list('αεηιουωἀἁἐἑἠἡἰἱὀὁὐὑὠὡάὰέὲήὴόὸίὶὺύώὼ'
                                    'ἄἅἔἕὄὅὂὃἤἥἴἵὔὕὤὥἂἃἒἓἢἣἲἳὒὓὢὣ'
                                    'ᾶῆῖῦῶἇἆἦἧἶἷὖὗὦὧϋϊΐῒϋῢΰῗῧ'))
# Combine both parts into a full alternation group
all_vowels = '|'.join(re.escape(char) for char in macronized_vowels) + '|' + unmacronized_vowels

# A few relevant regex conventions:
# "Character classes" [...] match any one character from a list
# "Capture groups" (...) capture the match for later use; used for "alternation" (...|...) and combinations (...)(...)
#   - NB: regexes of several combining characters together like '\u03B1\u0306' and '\u0391\u0306' must use alternation, i.e. ( | )
patterns = {
    'diphth_y': r'(α|ε|η|ο)(ὐ|ὔ|υ|ὑ|ύ|ὖ|ῦ|ὕ|ὗ|ὺ|ὒ|ὓ)', # note () for alternation and combination
    'diphth_i': r'(α|ε|ο|υ)(ἰ|ί|ι|ῖ|ἴ|ἶ|ἵ|ἱ|ἷ|ὶ|ἲ|ἳ)', # -''-
    'adscr_i': r'(α|η|ω|ἀ|ἠ|ὠ|ἁ|ἡ|ὡ|ά|ή|ώ|ὰ|ὴ|ὼ|ᾶ|ῆ|ῶ|ὤ|ὥ|ὢ|ὣ|ἄ|ἅ|ἂ|ἃ|ἤ|ἥ|ἣ|ἢ|ἦ|ἧ|ἆ|ἇ|ὧ|ὦ)(ι)', # -''-
    'subscr_i': r'[ᾄᾂᾆᾀᾅᾃᾇᾁᾴᾲᾷᾳᾔᾒᾖᾐᾕᾓᾗᾑῄῂῃῇᾤᾢᾦᾠᾥᾣᾧᾡῴῲῷῳ]', # note [] for single chars. 36 chars
    'stops': r'[πκτβδγφχθ]',
    'liquids': r'[ρλῥ]',
    'nasals': r'[μν]',
    'double_cons': r'[ζξψ]',
    'sibilants': r'[σς]',
    'vowels': f'({all_vowels})'
}

# ============================
# Auxiliary Functions
# ============================

def preprocess_text(text):
    # Characters to be ignored
    ignore_chars = set('\n\'(),-.·;<>[]«»;;··†—‘’' + '×⏑⏓–')

    # Removing the ignored characters from the text, but keeping spaces
    cleaned_text = ''.join([char if char != ' ' else ' ' for char in text.lower() if char not in ignore_chars])
    return cleaned_text

def divide_into_elements(text):
    '''
    Draws on the patterns dictionary to divide the text into elements.
    Keeps markup characters (^ and _) with their preceding character.
    '''
    elements = []
    i = 0
    while i < len(text):
        matched = False
        for pattern in patterns.values():
            match = re.match(pattern, text[i:])
            if match:
                matched = True
                element = match.group()
                # Check for markup after the matched element
                if i + len(element) < len(text) and text[i + len(element)] in '^_':
                    element += text[i + len(element)]
                    i += 1  # Skip the markup character in next iteration
                elements.append(element)
                i += len(match.group())
                break

        if not matched:
            if text[i] == ' ':
                elements.append(text[i])
            elif text[i] in '^_':
                # If we somehow got a lone markup character, attach it to previous element
                if elements:
                    elements[-1] += text[i]
            else:
                elements.append(f"UNCLASSIFIED: {text[i]}")
                print(f'erics_syllabifier.divide_into_elements:')
                print(f"Warning: Unclassified element '{text[i]}' at position {i}")
            i += 1

    return elements

def is_vowel(element):
    return any(re.match(patterns[vowel_type], element) for vowel_type in ['vowels', 'diphth_y', 'diphth_i', 'adscr_i', 'subscr_i'])

def is_consonant(element):
    return any(re.match(patterns[consonant_type], element) for consonant_type in ['stops', 'liquids', 'nasals', 'double_cons', 'sibilants'])

def syllabify(divided_text):
    elements = divided_text.split()
    syllables = []
    current_syllable = ''

    for element in elements:
        if is_vowel(element):
            # If there's already content in the current syllable, add it as a complete syllable
            if current_syllable:
                syllables.append(current_syllable)
                current_syllable = ''

            # Add the vowel to the current (now empty) syllable
            current_syllable = element
        else:
            # Add non-vowel elements to the current syllable
            current_syllable += element

    # Add the final syllable if it exists
    if current_syllable:
        syllables.append(current_syllable)
    return syllables

def reshuffle_consonants(syllables):
    reshuffled_syllables = []
    carry_over = ''

    for i in range(len(syllables)):
        syllable = syllables[i]

        # Handle start of line cases
        if i == 0 and not is_vowel(syllable[0]):
            vowel_index = next((index for index, char in enumerate(syllable) if is_vowel(char)), len(syllable))
            reshuffled_syllables.append(syllable[:vowel_index])
            carry_over = syllable[vowel_index:]
            continue

        # Prepend carry_over if present
        syllable = carry_over + syllable
        carry_over = ''

        # Simple and Complex case handling
        if i < len(syllables) - 1 and is_consonant(syllable[-1]):
            next_syllable = syllables[i + 1]
            if is_vowel(next_syllable[0]):
                # Move last consonant to next syllable (Simple case)
                carry_over = syllable[-1]
                syllable = syllable[:-1]
            else:
                # Complex case
                consonant_cluster = ''.join(filter(is_consonant, syllable))
                if len(consonant_cluster) > 1:
                    carry_over = consonant_cluster[1:]
                    syllable = syllable.replace(consonant_cluster, consonant_cluster[0], 1)

        reshuffled_syllables.append(syllable)

    # Add any remaining carry over to the last syllable
    if carry_over:
        reshuffled_syllables[-1] += carry_over

    return reshuffled_syllables

def final_reshuffle(reshuffled_syllables):
    final_syllables = []
    
    for i, syllable in enumerate(reshuffled_syllables):
        # Check for the end of the syllable having multiple consonants
        if syllable and i < len(reshuffled_syllables) - 1 and is_consonant(syllable[-1]):
            next_syllable = reshuffled_syllables[i + 1]
            # Count how many consonants are at the end
            consonant_count = 0
            while consonant_count < len(syllable) and is_consonant(syllable[-(consonant_count + 1)]):
                consonant_count += 1
            
            if consonant_count > 1:
                # Leave one consonant at the end of the current syllable, push the rest to the next
                split_index = consonant_count - 1
                final_syllables.append(syllable[:-split_index])
                reshuffled_syllables[i + 1] = syllable[-split_index:] + next_syllable
            else:
                final_syllables.append(syllable)
        else:
            final_syllables.append(syllable)

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

def syllabifier(string):
    '''
    all double consonants and mutae-cum-liquidae are treated as closed, i.e.
    >>syllabifier('πατρός')
    >>['πατ', 'ρός']

    string -> list
    '''
    cleaned_text = preprocess_text(string)
    divided_text = divide_into_elements(cleaned_text)
    joined_text = ' '.join(divided_text)
    syllabified_text = syllabify(joined_text)
    reshuffled_text = reshuffle_consonants(syllabified_text)
    final_reshuffled_text = final_reshuffle(reshuffled_text)
    definitive_text = definitive_syllables(final_reshuffled_text)

    return definitive_text
