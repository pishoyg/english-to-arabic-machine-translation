import argparse
from lang_cleaner import lang_to_cleaner
from itertools import chain

# Arguments.
parser = argparse.ArgumentParser(description='Argument parser.')
parser.add_argument(
    '--corpus_path',
    type=str,
    required=True,
    help='Input text file containing corpus. '
    'Please do NOT include the language suffix. '
    'This will also be used to deduce the output path.')
parser.add_argument(
    '--lang',
    type=str,
    required=True,
    choices=['ara', 'eng'],
    help='Language suffix.'
)
args = parser.parse_args()

# Cleaner.
cleaner = lang_to_cleaner[args.lang]

# Read Corpus.
with open('.'.join([args.corpus_path, args.lang])) as input_file:
    corpus = input_file.read().split('\n')

# Extract Info.
clean = [' '.join([cleaner.clean(word) for word in sentence.split()]) for sentence in corpus]

vocab = sorted(list(set(chain.from_iterable([sentence.split() for sentence in clean]))))

alphabet = sorted(list(set(chain.from_iterable([set(word) for word in vocab]))))

# Write info.
for name, info in [('alphabet', alphabet), ('vocab', vocab), ('clean', clean)]:
    with open('.'.join([args.corpus_path, name, args.lang]), 'w') as output_file:
        output_file.write('\n'.join(info))

