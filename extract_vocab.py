import argparse
from itertools import chain
from collections import Counter
import matplotlib.pyplot as plt

# Arguments.
parser = argparse.ArgumentParser(description=
  'Read corpora, and generate'
  ' (1) Vocabulary file, sorted by frequency.'
  ' (2) Alphabet file.'
  ' (3) Frequencey file, containing frequencies of each word. ',
  formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    '--corpus_prefix',
    type=str,
    required=True,
    help='Corpora prefix. '
    'The input path will be "<corpus_prefix>.<lang_extension>.<lang>", '
    'and the output path will be "<corpus_prefix>.<lang_extension>.<info>.<lang>". '
    'If any field is missing, it will be ignored.'
)
parser.add_argument(
    '--lang_extensions',
    type=str,
    help='Language extensions. See documentation of --corpus_prefix for details.',
    nargs='+',
    default=['stanford.clean', 'clean']
)
parser.add_argument(
    '--langs',
    type=str,
    help='Language suffixes. See documentation of --corpus_prefix for details.',
    nargs='+',
    default=['ara', 'eng']
)
parser.add_argument(
    '--freq_delim',
    type=str,
    help='String to use as a delimiter between words and their respective '
    'counts in the frequency file.',
    nargs=1,
    default=' '
)

args = parser.parse_args()
assert len(args.langs) == len(args.lang_extensions)
args.lang_extensions = {lang: lang_extension for lang, lang_extension in zip(args.langs, args.lang_extensions)}

for lang in args.langs:
  lang_extension = args.lang_extensions[lang]
  print('Processing language %s.' % lang)

  # Read Corpus.
  print('Reading corps.')
  with open('.'.join(filter(None, [args.corpus_prefix, lang_extension, lang]))) as input_file:
    corpus = input_file.read().split('\n')

  # Extract Info.
  print('Extracting Vocabulary.')
  vocab_freq = dict(Counter(chain.from_iterable(map(lambda sentence: sentence.split(), corpus))))
  print('Listing alphabet.')
  alphabet = sorted(list(set(c for word in vocab_freq for c in word)))
  print('Sorting vocab by frequency.')
  vocab_freq = sorted(vocab_freq.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
  print('Writing info.')
  # Write info.
  for name, info in [
    ('alphabet', alphabet),
    ('vocab', map(lambda kv: kv[0], vocab_freq)),
    ('freq', map(lambda kv: args.freq_delim.join((kv[0], str(kv[1]))), vocab_freq))]:
    with open('.'.join(filter(None, [args.corpus_prefix, lang_extension, name, lang])), 'w') as output_file:
      output_file.write('\n'.join(info))

