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

  # Read Corpus.
  print('Reading corps.')
  with open('.'.join([args.input, lang])) as input_file:
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
    with open('.'.join([args.input, name, lang]), 'w') as output_file:
      output_file.write('\n'.join(info))

