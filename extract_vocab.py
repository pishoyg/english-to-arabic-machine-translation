import argparse
from itertools import chain
from collections import Counter

# Arguments.
parser = argparse.ArgumentParser(description=
  'Read corpora, and generate'
  ' (1) Vocabulary file, sorted by frequency.'
  ' (2) Alphabet file.'
  ' (3) Frequencey file, containing frequencies of each word. '
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
    nargs=2,
    default=['stanford', '']
)
parser.add_argument(
    '--langs',
    type=str,
    help='Language suffixes. See documentation of --corpus_prefix for details.',
    nargs=2,
    default=['ara', 'eng']
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
  print('Sorting vocab by frequency.')
  sorted_vocab = sorted(list(vocab_freq.keys()), key=lambda word: vocab_freq[word], reverse=True)
  print('Listing alphabet.')
  alphabet = sorted(list(set(c for word in sorted_vocab for c in word)))
  print('Writing info.')
  # Write info.
  for name, info in [
    ('alphabet', alphabet),
    ('vocab', sorted_vocab),
    ('freq', map(lambda word: word + ' ' + str(vocab_freq[word]), sorted_vocab))]:
    with open('.'.join(filter(None, [args.corpus_prefix, lang_extension, name, lang])), 'w') as output_file:
      output_file.write('\n'.join(info))
