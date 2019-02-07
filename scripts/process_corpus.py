import argparse
from lang_cleaner import lang_to_cleaner
from itertools import chain

# Arguments.
parser = argparse.ArgumentParser(description=
  'Read corpora, and generate'
  ' (1) A clean version of it.'
  ' (2) Vocabulary file.'
  ' (3) Alphabet file.'
  'Notice that for every language suffix specified in args.langs, '
  'a corresponding cleaner must be available from lang_to_cleaner.py.'
)
parser.add_argument(
    '--input',
    type=str,
    required=True,
    help='Input text file containing corpus. '
    'Please do NOT include the language suffix. '
    'This will also be used to deduce the output path.'
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
  # Cleaner.
  cleaner = lang_to_cleaner[lang]

  # Read Corpus.
  with open('.'.join([args.input, lang])) as input_file:
    corpus = input_file.read().split('\n')

  # Extract Info.
  clean = [' '.join([cleaner.clean(word) for word in sentence.split()]) for sentence in corpus]

  vocab = sorted(list(set(chain.from_iterable([sentence.split() for sentence in clean]))))

  alphabet = sorted(list(set(chain.from_iterable([set(word) for word in vocab]))))

  # Write info.
  for name, info in [('alphabet', alphabet), ('vocab', vocab), ('clean', clean)]:
    with open('.'.join([args.input, name, lang]), 'w') as output_file:
      output_file.write('\n'.join(info))
