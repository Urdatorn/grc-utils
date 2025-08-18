'''
Robust unicode functions for Ancient Greek numerals, accomodating
- upper and lower case
- numerals covering 1 to 999 000, meaning:
- all different apostrophes I am aware of, including the thousand one, and
- all the 8 non-standard letters, including both sets of koppa
'''

import re

apostrophes = "'’‘´΄`\u02bc͵" # the last one is for thousands

stigma_large = "\u03da" # Ϛ
stigma_small = "\u03db" # ϛ (not to be confused with ς)
koppa_large = "\u03de" # Ϟ
koppa_small = "\u03df" # ϟ
koppa_archaic_large = "\u03d8" # Ϙ
koppa_archaic_small = "\u03d9" # ϙ
sampi_large = "\u03e0" # Ϡ
sampi_small = "\u03e1" # ϡ

# Define Greek numerals from α' to ϡ' (1 - 900)
greek_power_zero = f"αβγδε{stigma_large}{stigma_small}ζηθ"
greek_power_one = f"ικλμνξοπ{koppa_large}{koppa_small}{koppa_archaic_large}{koppa_archaic_small}"
greek_power_two = f"ρστυφχψω{sampi_large}{sampi_small}"

greek_numeral = re.compile(rf"""(?:
    [{greek_power_zero}][{greek_power_one}]?[{greek_power_two}]?|
    [{greek_power_zero}][{greek_power_two}]?[{greek_power_one}]?|
    [{greek_power_one}][{greek_power_zero}]?[{greek_power_two}]?|
    [{greek_power_one}][{greek_power_two}]?[{greek_power_zero}]?|
    [{greek_power_two}][{greek_power_zero}]?[{greek_power_one}]?|
    [{greek_power_two}][{greek_power_one}]?[{greek_power_zero}]?
)[{apostrophes}]""", re.VERBOSE) # the flag allows for multiline regex (i.e. does not match newlines and spaces)

def is_greek_numeral(word):
    return bool(greek_numeral.fullmatch(word))

if __name__ == "__main__":
    print(greek_numeral.pattern)

    print(is_greek_numeral("α'"))  # True
    print(is_greek_numeral("ϡ`"))  # True
    print(is_greek_numeral("ϡϟϛ`"))  # True

