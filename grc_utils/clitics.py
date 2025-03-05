'''Extracted from Anna Conser's Greek_Prosody.class_word.py'''

import re
import unicodedata

################################################
# ACCENTS
################################################

ACUTE = u'\u0301'
GRAVE = u'\u0300'
CIRCUMFLEX = u'\u0342'

ACCENTS = [ACUTE, GRAVE, CIRCUMFLEX]

ACCENT_DICT = {ACUTE: 'A',
               GRAVE: 'G',
               CIRCUMFLEX: 'C',
               None: '-'
               }

def remove_accents (text):
    split_chs = unicodedata.normalize("NFD", text)
    accentless = ''
    for ch in split_chs:
        if ch not in ACCENTS:
            accentless += ch
    return accentless

def get_accent (syllable):
    chs = unicodedata.normalize("NFD", syllable)
    for a in ACCENTS:
            if a in chs:
                return a

################################################
# CLITICS
################################################

PUNCTUATION = ".,;·:'<>[]{}()=+\u037e\u0387\u00B7⟨⟩†—"

NORMAL_ENCLITICS = ['μου', 'μοι', 'με', 'μευ', 'σου', 'σοι', 'σε',
             'οὑ', 'οἱ', 'ἑ', 'σευ', 'σεο', 'τοι', 'νιν',                #pronouns
             
             'τις', 'τι', 'τινος', 'του', 'τινι', 'τῳ', 'τινα',          #indefinite singulars
             'τινε', 'τινοιν', 'τινες', 'τινων', 'τισι', 'τινας',        #indefinite plurals (unaccented)
             'τινός', 'τοῦ', 'τινί', 'τινά', 'τινέ',                     #indefinite (acute)
             'τινοῖν', 'τινές', 'τινῶν', 'τισί', 'τινάς',
             'τινὸς', 'τινὶ', 'τινὰ', 'τινὲ', 'τινὲς', 'τισὶ', 'τινὰς',  #indefinite (grave)
             'τινʼ', 'τισʼ',
             
             'που', 'ποθι', 'ποθί', 'ποθὶ', 'ποθεν', 'ποθέν', 'ποθὲν',   #indefinite adverbs 
             'ποτε', 'ποτέ', 'ποτὲ', 'ποτʼ', 'ποθʼ', 'πω', 'πως', 'πῃ', 'ποι', 
             
             'εἰμι', 'ἐστι', 'ἐστον', 'ἐσμεν', 'ἐστε', 'εἰσι',           #'to be' (unaccented)
             'εἰμί', 'ἐστί', 'ἐστόν', 'ἐσμέν', 'ἐστέ', 'εἰσί',           #        (acute)
             'εἰμὶ', 'ἐστὶ', 'ἐστὸν', 'ἐσμὲν', 'ἐστὲ', 'εἰσὶ',           #        (grave)
             'φημι', 'φησι', 'φατον', 'φαμεν', 'φατε', 'φασι',           #'to say' (unaccented)
             'φημί', 'φησί', 'φατόν', 'φαμέν', 'φατέ', 'φασί',           #         (acute)
             'φημὶ', 'φησὶ', 'φατὸν', 'φαμὲν', 'φατὲ', 'φασὶ',            #         (grave)
             
             'γε', 'τε', 'τοι', 'περ', 'κε', 'θην', 'ῥα', 'νυ', 'νυν'    #particles
             ]

NORMAL_PROCLITICS = ['ὁ', 'ἡ', 'οἱ', 'αἱ', 'ἐν', 'εἰς', 'ἐς',  #traditional enclitics
              'ἐξ', 'ἐκ', 'εἰ', 'αἰ', 'ὡς', 'οὐ', 'οὐκ', 'οὐχ',
              
              'ἀμφʼ', 'ἀμφί', 'ἀμφίς', 'ἀμφὶ', 'ἀμφὶς', #prepositions accented on ultima
              'ἀνʼ', 'ἀνά', 'ἀνὰ', 
              'ἀντί', 'ἀντὶ', 
              'ἀπʼ', 'ἀπό', 'ἀπύ', 'ἀπὸ', 'ἀπὺ', 
              'διʼ', 'διά', 'διὰ', 
              'ἐκτός', 'ἐκτὸς', 'ἐνί', 'ἐνὶ', 
              'ἐπʼ', 'ἐπί', 'ἐπὶ', 'ἐφʼ',
              'καθʼ', 'κατʼ', 'κατά', 'κατὰ', 
              'μεθʼ', 'μετʼ', 'μετά', 'μετὰ', 
              'παρʼ', 'παρά', 'παρὰ', 
              'περί', 'περὶ', 
              'πλήν', 'πλὴν', 'πλάν', 'πλὰν',
              'πρός', 'πρὸς', 'ποτί', 'ποτὶ', 'προτί', 'προτὶ',
              'πρό', 'πρὸ',
              'σύν', 'σὺν', 
              'ὑπό', 'ὑπὸ', 'ὑφʼ', 'ὑπʼ', 
              'ὑπέρ', 'ὑπὲρ',
              'ὑποπρό', 'ὑποπρὸ', 'ὑππρό', 'ὑππρὸ',
              'χωρίς', 'χωρὶς',
              
              'ὁ', 'ἡ', 'τό', 'τὸ', 'τοῦ', 'τῆς',       #def articles
              'τῷ', 'τῇ', 'τόν', 'τὸν', 'τήν', 'τὴν',   #(redundant forms removed)
              'οἱ', 'αἱ', 'τά', 'τὰ', 'τῶν', 'τοῖς', 'ταῖς', 
              'τούς', 'τοὺς', 'τάς', 'τὰς',
              'τώ', 'τὼ', 'τᾱ́', 'τᾱ̀', 'τοῖν', 'ταῖν',
              'τάν', 'τὰν', 'τᾷ', 'ἁ', 'τᾶς',   #doric forms....
              
              'οὐ', 'οὐκ', 'οὐχ', 'οὐδ’',
              
              'ἠδʼ', 'ἀλλʼ'
              ]

OCT_ENCLITICS = [re.sub('ς|σ', 'ϲ', w) for w in NORMAL_ENCLITICS if re.search('ς|σ', w)]
OCT_PROCLITICS = [re.sub('ς|σ', 'ϲ', w) for w in NORMAL_PROCLITICS if re.search('ς|σ', w)]

ENCLITICS = NORMAL_ENCLITICS + OCT_ENCLITICS
PROCLITICS = NORMAL_PROCLITICS + OCT_PROCLITICS
                 
APOSTROPHE = u'\u02bc',  #MODIFIER LETTER APOSTROPHE

def _clean (text):
    """Removes whitespace and punctuation from edges of a string.  Punctuation
    does not include apostrophes marking elision."""
    return text.strip().strip(PUNCTUATION)

################################################
# THE TWO MAIN FUNCTIONS
################################################

def is_enclitic (word):
    """Checks whether a word is one of the Greek enclitics. For forms with an 
    acute, I have included both the acute and the grave form.  Elided forms are
    also included.
    
    :param str word: a Greek word
    :rtype: bool
    """
    return _clean(word) in ENCLITICS

def is_proclitic (word):
    """Checks whether a word is one of the Greek proclitics. In addition to the 
    traditional (unaccented) proclitics, I have included prepositions accented 
    on the ultima, and all definite articles.  For forms with an acute, I have 
    included both the acute and the grave form, as well as elided (and roughened)
    forms. I am also including as proclitic any word which has lost its accent
    through elision but is not one of the enclitics.
    
    Note: I should check this against Devine and Stevens when I have the chance.
    They might include even more forms.
    
    :param str word: a Greek word
    :rtype: bool
    """
    w = _clean(word)
    if w in PROCLITICS:
        return True
    if w.endswith(APOSTROPHE) and get_accent(w) == None and not is_enclitic(w):
        return True
    else:
        return False