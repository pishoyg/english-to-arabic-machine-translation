import argparse
from lang_cleaner import lang_to_cleaner
from itertools import chain
from collections import Counter

# Arguments.
parser = argparse.ArgumentParser(description=
  'Read corpora, and generate'
  ' (1) A cleaned version of it.'
  ' (2) Vocabulary file, sorted by frequency.'
  ' (3) Alphabet file.'
  ' (4) Frequencey file, containing frequencies of each word. '
  'Notice that for every language suffix specified in args.langs, '
  'a corresponding cleaner must be available from lang_cleaner.py.'
)
parser.add_argument(
    '--input',
    type=str,
    required=True,
    help='Input text file containing corpus. '
    'This will also be used as a prefix of the output path. '
    'Please do NOT include the language suffix.'
)
parser.add_argument(
    '--langs',
    type=str,
    help='Language suffixes.',
    nargs=2,
    default=['ara', 'eng']
)
args = parser.parse_args()

for lang in args.langs:
  print('Processing language %s.' % lang)
  # Cleaner.
  cleaner = lang_to_cleaner[lang]

  # Read Corpus.
  print('Reading corps.')
  with open('.'.join([args.input, lang])) as input_file:
    clean = list(map(cleaner.clean, input_file.read().split('\n')))

  # Extract Info.
  print('Extracting Vocabulary.')
  vocab_freq = dict(Counter(chain.from_iterable(map(lambda sentence: sentence.split(), clean))))
  print('Sorting vocab by frequency.')
  sorted_vocab = sorted(list(vocab_freq.keys()), key=lambda word: vocab_freq[word], reverse=True)
  print('Listing alphabet.')
  alphabet = sorted(list(set(c for word in sorted_vocab for c in word)))
  print('Writing info.')
  # Write info.
  for name, info in [
    ('clean', clean),
    ('alphabet', alphabet),
    ('vocab', sorted_vocab),
    ('freq', map(lambda word: word + ' ' + str(vocab_freq[word]), sorted_vocab))]:
    with open('.'.join([args.input, name, lang]), 'w') as output_file:
      output_file.write('\n'.join(info))
