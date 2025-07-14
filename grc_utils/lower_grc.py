'''
Python's built in .lower() and .upper() work terribly bad for polytonic Greek.
Accents, breathings and iota subscripta vanish into the aether.
"If you need something done, you have to do it yourself."

ἰδού: lower_grc(str) and upper.grc(str)
'''

CONSONANTS_UPPER_TO_LOWER = {
    "\u0392": "\u03b2",  # Β → β (Beta)
    "\u0393": "\u03b3",  # Γ → γ (Gamma)
    "\u0394": "\u03b4",  # Δ → δ (Delta)
    "\u03dc": "\u03dd",  # Ϝ → ϝ (Digamma)
    "\u0376": "\u0377",  # Ͷ → ͷ (Pamphylian Digamma)
    "\u0396": "\u03b6",  # Ζ → ζ (Zeta)
    "\u0398": "\u03b8",  # Θ → θ (Theta)
    "\u039a": "\u03ba",  # Κ → κ (Kappa)
    "\u03d8": "\u03d9",  # Ϙ → ϙ (Archaic Koppa)
    "\u03de": "\u03df",  # Ϟ → ϟ (Koppa)
    "\u039b": "\u03bb",  # Λ → λ (Lambda)
    "\u039c": "\u03bc",  # Μ → μ (Mu)
    "\u039d": "\u03bd",  # Ν → ν (Nu)
    "\u039e": "\u03be",  # Ξ → ξ (Xi)
    "\u03a0": "\u03c0",  # Π → π (Pi)
    "\u1fec": "\u1fe5",  # Ῥ → ῤ (Rough Rho) # Only rough rho can appear in capitalization (except hypothetically in Aeolic)
    "\u03a3": "\u03c3",  # Σ → σ (Sigma)
    "\u03da": "\u03db",  # Ϛ → ϛ (Stigma)
    "\u03e0": "\u03e1",  # Ϡ → ϡ (Sampi)
    "\u0372": "\u0373",  # Ͳ → ͳ (Archaic Sampi)
    "\u03f6": "\u03fb",  # Ϻ → ϻ (San)
    "\u03f7": "\u03f8",  # Ϸ → ϸ (Sho)
    "\u03a4": "\u03c4",  # Τ → τ (Tau)
    "\u03a6": "\u03c6",  # Φ → φ (Phi)
    "\u03a7": "\u03c7",  # Χ → χ (Chi)
    "\u03a8": "\u03c8",  # Ψ → ψ (Psi)
}

CONSONANTS_LOWER_TO_UPPER = {CONSONANTS_UPPER_TO_LOWER[key]: key for key in CONSONANTS_UPPER_TO_LOWER}

UPPER_SMOOTH = [  #
    "\u1f08",  # Ἀ Greek Capital Letter Alpha with Psili
    "\u1f18",  # Ἐ Greek Capital Letter Epsilon with Psili
    "\u1f28",  # Ἠ Greek Capital Letter Eta with Psili
    "\u1f38",  # Ἰ Greek Capital Letter Iota with Psili
    "\u1f48",  # Ὀ Greek Capital Letter Omicron with Psili
    "\u1f68",  # Ὠ Greek Capital Letter Omega with Psili
    "\u1f88",  # ᾈ Greek Capital Letter Alpha with Psili and Prosgegrammeni
    "\u1f98",  # ᾘ Greek Capital Letter Eta with Psili and Prosgegrammeni
    "\u1fa8",  # ᾨ Greek Capital Letter Omega with Psili and Prosgegrammeni
]

UPPER_SMOOTH_ACUTE = [
    "\u1f0c",  # Ἄ Greek Capital Letter Alpha with Psili and Oxia
    "\u1f1c",  # Ἔ Greek Capital Letter Epsilon with Psili and Oxia
    "\u1f2c",  # Ἤ Greek Capital Letter Eta with Psili and Oxia
    "\u1f3c",  # Ἴ Greek Capital Letter Iota with Psili and Oxia
    "\u1f4c",  # Ὄ Greek Capital Letter Omicron with Psili and Oxia # TODO warning! found trivial switcharoo typo here, \u1fc4 (ῄ); gotta make a PR to cltk
    "\u1f6c",  # Ὤ Greek Capital Letter Omega with Psili and Oxia
    "\u1f8c",  # ᾌ Greek Capital Letter Alpha with Psili and Oxia and Prosgegrammeni
    "\u1f9c",  #  ᾜ Greek Capital Letter Eta with Psili and Oxia and Prosgegrammeni
    "\u1fac",  # ᾬ Greek Capital Letter Omega with Psili and Oxia and Prosgegrammeni
]

UPPER_SMOOTH_GRAVE = [  #
    "\u1f0a",  # Ἂ Greek Capital Letter Alpha with Psili and Varia
    "\u1f1a",  # Ἒ Greek Capital Letter Epsilon with Psili and Varia
    "\u1f2a",  # Ἢ Greek Capital Letter Eta with Psili and Varia
    "\u1f3a",  # Ἲ Greek Capital Letter Iota with Psili and Varia
    "\u1f4a",  # Ὂ Greek Capital Letter Omicron with Psili and Varia
    "\u1f6a",  # Ὢ Greek Capital Letter Omega With Psili And Varia
    "\u1f8a",  # ᾊ Greek Capital Letter Alpha With Psili And Varia And Prosgegrammeni
    "\u1f9a",  # ᾚ Greek Capital Letter Eta With Psili And Varia And Prosgegrammeni
    "\u1faa",  # ᾪ Greek Capital Letter Omega With Psili And Varia And Prosgegrammeni
]
UPPER_SMOOTH_CIRCUMFLEX = [  #
    "\u1f0e",  # Ἆ Greek Capital Letter Alpha With Psili And Perispomeni
    "\u1f2e",  # Ἦ Greek Capital Letter Eta With Psili And Perispomeni
    "\u1f3e",  # Ἶ Greek Capital Letter Iota With Psili And Perispomeni
    "\u1f6e",  # Ὦ Greek Capital Letter Omega With Psili And Perispomeni
    "\u1f8e",  # ᾎ Greek Capital Letter Alpha With Psili And Perispomeni And Prosgegrammeni
    "\u1f9e",  # ᾞ Greek Capital Letter Eta With Psili And Perispomeni And Prosgegrammeni
    "\u1fae",  # ᾮ Greek Capital Letter Omega With Psili And Perispomeni And Prosgegrammeni
]

UPPER_ROUGH = [  #
    "\u1f09",  # Ἁ Greek Capital Letter Alpha With Dasia
    "\u1f19",  # Ἑ Greek Capital Letter Epsilon With Dasia
    "\u1f29",  # Ἡ Greek Capital Letter Eta With Dasia
    "\u1f39",  # Ἱ Greek Capital Letter Iota With Dasia
    "\u1f49",  # Ὁ Greek Capital Letter Omicron With Dasia
    "\u1f59",  # Ὑ Greek Capital Letter Upsilon With Dasia
    "\u1f69",  # Ὡ Greek Capital Letter Omega With Dasia
    "\u1f89",  # ᾉ Greek Capital Letter Alpha With Dasia And Prosgegrammeni
    "\u1f99",  # ᾙ Greek Capital Letter Eta With Dasia And Prosgegrammeni
    "\u1fa9",  # ᾩ Greek Capital Letter Omega With Dasia And Prosgegrammeni
]

UPPER_ROUGH_ACUTE = [  #
    "\u1f0d",  # Ἅ Greek Capital Letter Alpha With Dasia And Oxia
    "\u1f1d",  # Ἕ Greek Capital Letter Epsilon With Dasia And Oxia
    "\u1f2d",  # Ἥ Greek Capital Letter Eta With Dasia And Oxia
    "\u1f3d",  # Ἵ Greek Capital Letter Iota With Dasia And Oxia
    "\u1f4d",  # Ὅ Greek Capital Letter Omicron With Dasia And Oxia
    "\u1f5d",  # Ὕ Greek Capital Letter Upsilon With Dasia And Oxia
    "\u1f6d",  # Ὥ Greek Capital Letter Omega With Dasia And Oxia
    "\u1f8d",  # ᾍ Greek Capital Letter Alpha With Dasia And Oxia And Prosgegrammeni
    "\u1f9d",  # ᾝ Greek Capital Letter Eta With Dasia And Oxia And Prosgegrammeni
    "\u1fad",  # ᾭ Greek Capital Letter Omega With Dasia And Oxia And Prosgegrammeni
]

UPPER_ROUGH_GRAVE = [  #
    "\u1f0b",  # Ἃ Greek Capital Letter Alpha With Dasia And Varia
    "\u1f1b",  # Ἓ Greek Capital Letter Epsilon With Dasia And Varia
    "\u1f2b",  # Ἣ Greek Capital Letter Eta With Dasia And Varia
    "\u1f3b",  # Ἳ Greek Capital Letter Iota With Dasia And Varia
    "\u1f4b",  # Ὃ Greek Capital Letter Omicron With Dasia And Varia
    "\u1f5b",  # Ὓ Greek Capital Letter Upsilon With Dasia And Varia
    "\u1f6b",  # Ὣ Greek Capital Letter Omega With Dasia And Varia
    "\u1f8b",  # ᾋ Greek Capital Letter Alpha With Dasia And Varia And Prosgegrammeni
    "\u1f9b",  # ᾛ Greek Capital Letter Eta With Dasia And Varia And Prosgegrammeni
    "\u1fab",  # ᾫ Greek Capital Letter Omega With Dasia And Varia And Prosgegrammeni
]

UPPER_ROUGH_CIRCUMFLEX = [  #
    "\u1f0f",  # Ἇ Greek Capital Letter Alpha With Dasia And Perispomeni
    "\u1f2f",  # Ἧ Greek Capital Letter Eta With Dasia And Perispomeni
    "\u1f3f",  # Ἷ Greek Capital Letter Iota With Dasia And Perispomeni
    "\u1f5f",  # Ὗ Greek Capital Letter Upsilon With Dasia And Perispomeni
    "\u1f6f",  # Ὧ Greek Capital Letter Omega With Dasia And Perispomeni
    "\u1f8f",  # ᾏ Greek Capital Letter Alpha With Dasia And Perispomeni And Prosgegrammeni
    "\u1f9f",  # ᾟ Greek Capital Letter Eta With Dasia And Perispomeni And Prosgegrammeni
    "\u1faf",  # ᾯ Greek Capital Letter Omega With Dasia And Perispomeni And Prosgegrammeni
]

LOWER_SMOOTH = [  #
    "\u1f00",  # ἀ Greek Small Letter Alpha With Psili
    "\u1f10",  # ἐ Greek Small Letter Epsilon With Psili
    "\u1f20",  # ἠ Greek Small Letter Eta With Psili
    "\u1f30",  # ἰ Greek Small Letter Iota With Psili
    "\u1f40",  # ὀ Greek Small Letter Omicron With Psili
    "\u1f60",  # ὠ Greek Small Letter Omega With Psili
    "\u1f80",  # ᾀ Greek Small Letter Alpha With Psili And Ypogegrammeni
    "\u1f90",  # ᾐ Greek Small Letter Eta With Psili And Ypogegrammeni
    "\u1fa0",  # ᾠ Greek Small Letter Omega With Psili And Ypogegrammeni
]

LOWER_SMOOTH_ACUTE = [  #
    "\u1f04",  # ἄ Greek Small Letter Alpha With Psili And Oxia
    "\u1f14",  # ἔ Greek Small Letter Epsilon With Psili And Oxia
    "\u1f24",  # ἤ Greek Small Letter Eta With Psili And Oxia
    "\u1f34",  # ἴ Greek Small Letter Iota With Psili And Oxia
    "\u1f44",  # ὄ Greek Small Letter Omicron With Psili And Oxia
    "\u1f64",  # ὤ Greek Small Letter Omega With Psili And Oxia
    "\u1f84",  # ᾄ Greek Small Letter Alpha With Psili And Oxia And Ypogegrammeni
    "\u1f94",  # ᾔ Greek Small Letter Eta With Psili And Oxia And Ypogegrammeni
    "\u1fa4",  # ᾤ Greek Small Letter Omega With Psili And Oxia And Ypogegrammeni
]

LOWER_SMOOTH_GRAVE = [  #
    "\u1f02",  # ἂ Greek Small Letter Alpha With Psili And Varia
    "\u1f12",  # ἒ Greek Small Letter Epsilon With Psili And Varia
    "\u1f22",  # ἢ Greek Small Letter Eta With Psili And Varia
    "\u1f32",  # ἲ Greek Small Letter Iota With Psili And Varia
    "\u1f42",  # ὂ Greek Small Letter Omicron With Psili And Varia
    "\u1f62",  # ὢ Greek Small Letter Omega With Psili And Varia
    "\u1f82",  # ᾂ Greek Small Letter Alpha With Psili And Varia And Ypogegrammeni
    "\u1f92",  # ᾒ Greek Small Letter Eta With Psili And Varia And Ypogegrammeni
    "\u1fa2",  # ᾢ Greek Small Letter Omega With Psili And Varia And Ypogegrammeni
]

LOWER_SMOOTH_CIRCUMFLEX = [  #
    "\u1f06",  # ἆ Greek Small Letter Alpha With Psili And Perispomeni
    "\u1f26",  # ἦ Greek Small Letter Eta With Psili And Perispomeni
    "\u1f36",  # ἶ Greek Small Letter Iota With Psili And Perispomeni
    "\u1f66",  # ὦ Greek Small Letter Omega With Psili And Perispomeni
    "\u1f86",  # ᾆ Greek Small Letter Alpha With Psili And Perispomeni And Ypogegrammeni
    "\u1f96",  # ᾖ Greek Small Letter Eta With Psili And Perispomeni And Ypogegrammeni
    "\u1fa6",  # ᾦ Greek Small Letter Omega With Psili And Perispomeni And Ypogegrammeni
]

LOWER_ROUGH = [  #
    "\u1f01",  # ἁ Greek Small Letter Alpha With Dasia
    "\u1f11",  # ἑ Greek Small Letter Epsilon With Dasia
    "\u1f21",  # ἡ Greek Small Letter Eta With Dasia
    "\u1f31",  # ἱ Greek Small Letter Iota With Dasia
    "\u1f41",  # ὁ Greek Small Letter Omicron With Dasia
    "\u1f51",  # ὑ Greek Small Letter Upsilon With Dasia
    "\u1f61",  # ὡ Greek Small Letter Omega With Dasia
    "\u1f81",  # ᾁ Greek Small Letter Alpha With Dasia And Ypogegrammeni
    "\u1f91",  # ᾑ Greek Small Letter Eta With Dasia And Ypogegrammeni
    "\u1fa1",  # ᾡ Greek Small Letter Omega With Dasia And Ypogegrammeni
]

LOWER_ROUGH_ACUTE = [  #
    "\u1f05",  # ἅ Greek Small Letter Alpha With Dasia And Oxia
    "\u1f15",  # ἕ Greek Small Letter Epsilon With Dasia And Oxia
    "\u1f25",  # ἥ Greek Small Letter Eta With Dasia And Oxia
    "\u1f35",  # ἵ Greek Small Letter Iota With Dasia And Oxia
    "\u1f45",  # ὅ Greek Small Letter Omicron With Dasia And Oxia
    "\u1f55",  # ὕ Greek Small Letter Upsilon With Dasia And Oxia
    "\u1f65",  # ὥ Greek Small Letter Omega With Dasia And Oxia
    "\u1f85",  # ᾅ Greek Small Letter Alpha With Dasia And Oxia And Ypogegrammeni
    "\u1f95",  # ᾕ Greek Small Letter Eta With Dasia And Oxia And Ypogegrammeni
    "\u1fa5",  # ᾥ Greek Small Letter Omega With Dasia And Oxia And Ypogegrammeni
]

LOWER_ROUGH_GRAVE = [  #
    "\u1f03",  # ἃ Greek Small Letter Alpha With Dasia And Varia
    "\u1f13",  # ἓ Greek Small Letter Epsilon With Dasia And Varia
    "\u1f23",  # ἣ Greek Small Letter Eta With Dasia And Varia
    "\u1f33",  # ἳ Greek Small Letter Iota With Dasia And Varia
    "\u1f43",  # ὃ Greek Small Letter Omicron With Dasia And Varia
    "\u1f53",  # ὓ Greek Small Letter Upsilon With Dasia And Varia
    "\u1f63",  # ὣ Greek Small Letter Omega With Dasia And Varia
    "\u1f83",  # ᾃ Greek Small Letter Alpha With Dasia And Varia And Ypogegrammeni
    "\u1f93",  # ᾓ Greek Small Letter Eta With Dasia And Varia And Ypogegrammeni
    "\u1fa3",  # ᾣ Greek Small Letter Omega With Dasia And Varia And Ypogegrammeni
]

LOWER_ROUGH_CIRCUMFLEX = [  #
    "\u1f07",  # ἇ Greek Small Letter Alpha With Dasia And Perispomeni
    "\u1f27",  # ἧ Greek Small Letter Eta With Dasia And Perispomeni
    "\u1f37",  # ἷ Greek Small Letter Iota With Dasia And Perispomeni
    "\u1f57",  # ὗ Greek Small Letter Upsilon With Dasia And Perispomeni
    "\u1f67",  # ὧ Greek Small Letter Omega With Dasia And Perispomeni
    "\u1f87",  # ᾇ Greek Small Letter Alpha With Dasia And Perispomeni And Ypogegrammeni
    "\u1f97",  # ᾗ Greek Small Letter Eta With Dasia And Perispomeni And Ypogegrammeni
    "\u1fa7",  # ᾧ Greek Small Letter Omega With Dasia And Perispomeni And Ypogegrammeni
]

VOWELS_UPPER_TO_LOWER = {
**{UPPER_SMOOTH[i]: LOWER_SMOOTH[i] for i in range(len(UPPER_SMOOTH))},
**{UPPER_SMOOTH_ACUTE[i]: LOWER_SMOOTH_ACUTE[i] for i in range(len(UPPER_SMOOTH_ACUTE))},
**{UPPER_SMOOTH_GRAVE[i]: LOWER_SMOOTH_GRAVE[i] for i in range(len(UPPER_SMOOTH_GRAVE))},
**{UPPER_SMOOTH_CIRCUMFLEX[i]: LOWER_SMOOTH_CIRCUMFLEX[i] for i in range(len(UPPER_SMOOTH_CIRCUMFLEX))},
**{UPPER_ROUGH[i]: LOWER_ROUGH[i] for i in range(len(UPPER_ROUGH))},
**{UPPER_ROUGH_ACUTE[i]: LOWER_ROUGH_ACUTE[i] for i in range(len(UPPER_ROUGH_ACUTE))},
**{UPPER_ROUGH_GRAVE[i]: LOWER_ROUGH_GRAVE[i] for i in range(len(UPPER_ROUGH_GRAVE))},
**{UPPER_ROUGH_CIRCUMFLEX[i]: LOWER_ROUGH_CIRCUMFLEX[i] for i in range(len(UPPER_ROUGH_CIRCUMFLEX))}
}

VOWELS_LOWER_TO_UPPER = {VOWELS_UPPER_TO_LOWER[key]: key for key in VOWELS_UPPER_TO_LOWER}

def lower_grc(string):
    '''
    The lists used have neither oxia nor composed chars, so normalizing is not of the essence.
    '''
    string_lower_consonants = "".join([CONSONANTS_UPPER_TO_LOWER.get(char, char) for char in string])
    string_lower_consonants_and_vowels = "".join([VOWELS_UPPER_TO_LOWER.get(char, char) for char in string_lower_consonants])

    return string_lower_consonants_and_vowels


def upper_grc(string):
    '''
    Strictly the inverse of lower_grc.
    The lists used have neither oxia nor composed chars, so normalizing is not of the essence.
    '''
    string_upper_consonants = "".join([CONSONANTS_LOWER_TO_UPPER.get(char, char) for char in string])
    string_upper_consonants_and_vowels = "".join([VOWELS_LOWER_TO_UPPER.get(char, char) for char in string_upper_consonants])

    return string_upper_consonants_and_vowels

if __name__ == "__main__":
    if len(UPPER_SMOOTH) != len(LOWER_SMOOTH):
        raise ValueError(
            f"UPPER_SMOOTH and LOWER_SMOOTH must be the same length. "
            f"UPPER_SMOOTH length: {len(UPPER_SMOOTH)}, "
            f"LOWER_SMOOTH length: {len(LOWER_SMOOTH)}"
        )
    if len(UPPER_SMOOTH_ACUTE) != len(LOWER_SMOOTH_ACUTE):
        raise ValueError(
            f"UPPER_SMOOTH_ACUTE and LOWER_SMOOTH_ACUTE must be the same length. "
            f"UPPER_SMOOTH_ACUTE length: {len(UPPER_SMOOTH_ACUTE)}, "
            f"LOWER_SMOOTH_ACUTE length: {len(LOWER_SMOOTH_ACUTE)}"
        )
    if len(UPPER_SMOOTH_GRAVE) != len(LOWER_SMOOTH_GRAVE):
        raise ValueError(
            f"UPPER_SMOOTH_GRAVE and LOWER_SMOOTH_GRAVE must be the same length. "
            f"UPPER_SMOOTH_GRAVE length: {len(UPPER_SMOOTH_GRAVE)}, "
            f"LOWER_SMOOTH_GRAVE length: {len(LOWER_SMOOTH_GRAVE)}"
        )
    if len(UPPER_SMOOTH_CIRCUMFLEX) != len(LOWER_SMOOTH_CIRCUMFLEX):
        raise ValueError(
            f"UPPER_SMOOTH_CIRCUMFLEX and LOWER_SMOOTH_CIRCUMFLEX must be the same length. "
            f"UPPER_SMOOTH_CIRCUMFLEX length: {len(UPPER_SMOOTH_CIRCUMFLEX)}, "
            f"LOWER_SMOOTH_CIRCUMFLEX length: {len(LOWER_SMOOTH_CIRCUMFLEX)}"
        )
    if len(UPPER_ROUGH) != len(LOWER_ROUGH):
        raise ValueError(
            f"UPPER_ROUGH and LOWER_ROUGH must be the same length. "
            f"UPPER_ROUGH length: {len(UPPER_ROUGH)}, "
            f"LOWER_ROUGH length: {len(LOWER_ROUGH)}"
        )
    if len(UPPER_ROUGH_ACUTE) != len(LOWER_ROUGH_ACUTE):
        raise ValueError(
            f"UPPER_ROUGH_ACUTE and LOWER_ROUGH_ACUTE must be the same length. "
            f"UPPER_ROUGH_ACUTE length: {len(UPPER_ROUGH_ACUTE)}, "
            f"LOWER_ROUGH_ACUTE length: {len(LOWER_ROUGH_ACUTE)}"
        )
    if len(UPPER_ROUGH_GRAVE) != len(LOWER_ROUGH_GRAVE):
        raise ValueError(
            f"UPPER_ROUGH_GRAVE and LOWER_ROUGH_GRAVE must be the same length. "
            f"UPPER_ROUGH_GRAVE length: {len(UPPER_ROUGH_GRAVE)}, "
            f"LOWER_ROUGH_GRAVE length: {len(LOWER_ROUGH_GRAVE)}"
        )
    if len(UPPER_ROUGH_CIRCUMFLEX) != len(LOWER_ROUGH_CIRCUMFLEX):
        raise ValueError(
            f"UPPER_ROUGH_CIRCUMFLEX and LOWER_ROUGH_CIRCUMFLEX must be the same length. "
            f"UPPER_ROUGH_CIRCUMFLEX length: {len(UPPER_ROUGH_CIRCUMFLEX)}, "
            f"LOWER_ROUGH_CIRCUMFLEX length: {len(LOWER_ROUGH_CIRCUMFLEX)}"
        )

    print("Combined Dictionary:")
    for key, value in VOWELS_UPPER_TO_LOWER.items():
        print(f"{key}: {value}")

    for key, value in VOWELS_LOWER_TO_UPPER.items():
        print(f"{key}: {value}")

    for key, value in CONSONANTS_LOWER_TO_UPPER.items():
        print(f"{key}: {value}")
    