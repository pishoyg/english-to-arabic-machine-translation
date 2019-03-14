import argparse
from bleu_calculator import corpus_bleu

# Define arguments.
parser = argparse.ArgumentParser(description=
  'Driver for bleu_calculator.py.',
  formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
  '--ref_corpus_path',
  type=str,
  required=True,
  help='Path to the reference corpus.'
)
parser.add_argument(
  '--hyp_corpus_path',
  type=str,
  help='Path to the hypothesis corpus.'
)
args = parser.parse_args()

def main():
  print(100 * corpus_bleu(args.ref_corpus_path, args.hyp_corpus_path))

if __name__ == '__main__':
  main()
