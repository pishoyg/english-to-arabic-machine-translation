import argparse
from lang_cleaner import lang_to_cleaner
from itertools import chain
from collections import Counter

# Arguments.
parser = argparse.ArgumentParser(description=
  'Read corpora, and generate a cleaned version of it. '
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

  print('Reading corps.')
  with open('.'.join([args.input, lang])) as input_file:
    clean = list(map(cleaner.clean, input_file.read().split('\n')))

  print('Writing info.')
  with open('.'.join([args.input, 'clean', lang]), 'w') as output_file:
    output_file.write('\n'.join(clean))
