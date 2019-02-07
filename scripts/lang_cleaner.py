import re


class _LangCleaner(object):

    def clean(self, text):
        raise NotImplementedError()


class _ArabicCleaner(_LangCleaner):

    def __init__(self):
        self.p_eliminate = list(map(re.compile, [
            r'(.)\1+',  # longation.
            r'[\u0617-\u061A\u064B-\u0652]',  # tashkeel.
            r'[a-zA-Z0-9]+'  # alphanumerics.
        ]))
        self.replace_dict = dict()
        self.alphabet = {'ء', 'ؤ', 'ئ', 'ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي'}
        self.replace_pairs = []
        _search = ["أ","إ","آ","ة","_","-","/",".","،"," و "," يا ",'"',"ـ","'","ى","\\",'\n', '\t','&quot;','?','؟','!']
        _replace = ["ا","ا","ا","ه"," "," ","","",""," و"," يا","","","","ي","",' ', ' ',' ',' ? ',' ؟ ',' ! ']
        for search_i, replace_i in zip(_search, _replace):
          if len(search_i) == 1:
              self.replace_dict[search_i] = replace_i
          else:
              self.replace_pairs.append((search_i, replace_i))

    def clean(self, text):
        # Eliminations.
        for p in self.p_eliminate:
            text = re.sub(p, "", text)
        # Replacements.
        text = ''.join(c if c not in self.replace_dict else self.replace_dict[c] for c in text)
        for search_i, replace_i in self.replace_pairs:
            text.replace(search_i, replace_i)
        text = text.replace('وو', 'و').replace('يي', 'ي').replace('اا', 'ا')
        # Restrict to alphabetical characters.
        text = ''.join(c for c in text if c in self.alphabet)
        # Trim.
        text = text.strip()
        return text


class _EnglishCleaner(_LangCleaner):

    def __init__(self):
        self.non_eng = re.compile('[^a-z-]')
        self.dashes = re.compile('-+')

    def clean(self, text):
        text = text.lower()
        text = re.sub(self.non_eng, '', text)
        text = re.sub(self.dashes, '-', text)
        while text.startswith('-'):
            text = text[1:]
        while text.endswith('-'):
            text = text[:-1]
        return text


_arabic_cleaner = _ArabicCleaner()
_english_cleaner = _EnglishCleaner()

lang_to_cleaner = {
    'ara': _arabic_cleaner,
    'eng': _english_cleaner
}

