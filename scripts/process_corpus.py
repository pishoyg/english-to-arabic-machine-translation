import argparse
from lang_cleaner import lang_to_cleaner
from itertools import chain

# Arguments.
parser = argparse.ArgumentParser(description=
  'Read corpora, and generate'
  ' (1) A clean version of it.'
  ' (2) Vocabulary file, sorted by frequency.'
  ' (3) Alphabet file.'
  'Notice that for every language suffix specified in args.langs, '
  'a corresponding cleaner must be available from lang_cleaner.py.'
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
parser.add_argument(
    '--vocab_sizes',
    type=str,
    help='Language suffixes.',
    nargs=2,
    default=[40000, 20000]
)
args = parser.parse_args()
args.vocab_sizes = {lang: sz for lang, sz in zip(args.langs, args.vocab_sizes)}

for lang in args.langs:
  # Cleaner.
  cleaner = lang_to_cleaner[lang]

  # Read Corpus.
  with open('.'.join([args.input, lang])) as input_file:
    corpus = input_file.read().split('\n')

  # Extract Info.
  vocab = set()
  clean = []
  vocab_freq = dict()
  print('reading corpus')
  for sentence in corpus:
    words = list(filter(lambda x: x, [cleaner.clean(word) for word in sentence.split()]))
    clean.append(' '.join(words))
    for word in words:
      if word not in vocab:
        vocab.add(word)
        vocab_freq[word] = 0
      vocab_freq[word] += 1
  print('sorting vocab by frequency')
  vocab = sorted(list(vocab), key=lambda word: vocab_freq[word], reverse=True)
  print('listing alphabet')
  alphabet = sorted(list(set(c for word in vocab for c in word)))
  print('writing info')
  # Write info.
  for name, info in [
    ('clean', clean),
    ('alphabet', alphabet),
    ('vocab', vocab),
    ('vocab.head', vocab[0:args.vocab_sizes[lang]]),
    ('freq', map(lambda x: x[0] + ': ' + str(x[1]), sorted(list(vocab_freq.items()), reverse=True, key=lambda x: x[1])))
    ]:
    with open('.'.join([args.input, name, lang]), 'w') as output_file:
      output_file.write('\n'.join(info))

