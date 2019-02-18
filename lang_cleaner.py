import re


class _LangCleaner(object):

  def clean(self, text):
    raise NotImplementedError()


class _ArabicCleaner(_LangCleaner):

  def __init__(self):
    self.p_tashkeel = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
    self.p_longation = re.compile(r'(.)\1+')
    self.p_longation_subst = r"\1\1"
    _search = ["أ","إ","آ","ة","_","-","/",".","،"," و "," يا ",'"',"ـ","'","ى","\\",'\n', '\t','&quot;','?','؟','!']
    _replace = ["ا","ا","ا","ه"," "," ","","",""," و"," يا","","","","ي","",' ', ' ',' ',' ? ',' ؟ ',' ! ']
    self.replace_pairs = list(zip(_search, _replace))
    self.non_ara_re = re.compile(
      '[^' + ''.join(['ء', 'ؤ', 'ئ', 'ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي']) + ']+')

  def clean(self, text):
    text = self.p_tashkeel.sub("", text)
    text = self.p_longation.sub(self.p_longation_subst, text)
    for search_i, replace_i in self.replace_pairs:
      text = text.replace(search_i, replace_i)
    text = text.replace('وو', 'و').replace('يي', 'ي').replace('اا', 'ا')
    text = self.non_ara_re.sub(' ', text)
    text = text.strip()
    return text


class _EnglishCleaner(_LangCleaner):

  def __init__(self):
    self.non_eng_re = re.compile('[^a-z]+')

  def clean(self, text):
    text = text.lower()
    text = self.non_eng_re.sub(' ', text)
    text = text.strip()
    return text


_arabic_cleaner = _ArabicCleaner()
_english_cleaner = _EnglishCleaner()


# This is the only construct that is exported by this file.
lang_to_cleaner = {
  'ara': _arabic_cleaner,
  'eng': _english_cleaner
}

