import argparse


# Define arguments.
parser = argparse.ArgumentParser(description=
  'Given a file containing vocabulary and a file containing embeddings '
  'in word2vec foramt, output two files containing the intersection of '
  'both sets of vocabulary.',
  formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
  '--input_glove',
  type=str,
  required=True,
  help='Path to input glove file.'
)
parser.add_argument(
  '--input_vocab',
  type=str,
  required=True,
  help='Path to input vocab file.'
)
parser.add_argument(
  '--output_glove',
  type=str,
  required=True,
  help='Path to filtered output file in glove format.'
)
parser.add_argument(
  '--output_vocab',
  type=str,
  required=True,
  help='Path to filtered vocabulary format.'
)
args = parser.parse_args()


def main():
  with open(args.input_vocab) as input_vocab:
    vocab = {line.strip(): False for line in input_vocab}
  with open(args.input_glove) as input_glove:
    with open(args.output_glove, 'w') as output_glove:
      for line in input_glove:
        word = line[:line.find(' ')]
        if word in vocab:
          output_glove.write(line)
          vocab[word] = True
  with open(args.output_vocab, 'w') as output_vocab:
    for word, seen in vocab.items():
      if seen:
        output_vocab.write(word + '\n')


if __name__ == '__main__':
  main()

