import argparse


# Define arguments.
parser = argparse.ArgumentParser(description=
  'Filter embeddings in word2vec format into Glove format.',
  formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
  '--input_path',
  type=str,
  required=True,
  help='Path to input file in word2vec format.'
)
parser.add_argument(
  '--vocab_path',
  type=str,
  required=True,
  help='Path to vocab file. Only embeddings belonging to '
  'vocabulary in this file will be part of the output.'
)
parser.add_argument(
  '--output_path',
  type=str,
  required=True,
  help='Path to filtered output file in glove format.'
)
args = parser.parse_args()


def main():
  with open(args.vocab_path) as vocab_file:
    vocab = set(map(lambda line: line.strip(), vocab_file))
  with open(args.input_path) as input_file:
    with open(args.output_path, 'w') as output_file:
      for line in input_file:
        if line[:line.find(' ')] in vocab:
          output_file.write(line)


if __name__ == '__main__':
  main()

