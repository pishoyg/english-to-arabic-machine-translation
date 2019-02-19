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
    '--corpus_prefix',
    type=str,
    required=True,
    help='Corpora prefix. '
    'The input path will be "<corpus_prefix>.<lang_extension>.<lang>", '
    'and the output path will be "<corpus_prefix>.<lang_extension>.clean.<lang>". '
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

assert len(args.lang_extensions) == len(args.langs)

for lang, lang_extension in zip(args.langs, args.lang_extensions):
  print('Processing language %s.' % lang)
  input_file = '.'.join(filter(None, [args.corpus_prefix, lang_extension, lang]))
  output_file = '.'.join(filter(None, [args.corpus_prefix, lang_extension, 'clean', lang]))
  with open(input_file) as input_file:
    cleaned_corpus = map(lang_to_cleaner[lang].clean, input_file.read().split('\n'))
  with open(output_file, 'w') as output_file:
    output_file.write('\n'.join(cleaned_corpus))
