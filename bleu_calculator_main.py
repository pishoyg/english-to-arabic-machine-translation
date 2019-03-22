import argparse
from bleu_calculator import corpus_bleu
# DO NOT SUBMIT
import time
# DO NOT SUBMIT

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
parser.add_argument(
  '--track',
  type=int,
  default=0,
  help='Print counter every <track> sentences. If 0, print nothing. '
  'Only usable with --memory_friendly.'
)
parser.add_argument(
  '--memory_friendly',
  dest='memory_friendly',
  action='store_true',
  default=True,
  help='If set, will implement a memory-friendly generator wrapper '
  'for BLEU score calculation.'
)
parser.add_argument(
  '--no-memory_friendly',
  dest='memory_friendly',
  action='store_false',
  default=False,
  help='Opposite of --memory_friendly.'
)

args = parser.parse_args()
assert not args.track or args.memory_friendly, '--track is only available with --memory_friendly.'

def main():
  start_time = time.clock()
  print('BLEU: ',
        100 * corpus_bleu(args.ref_corpus_path,
                          args.hyp_corpus_path,
                          memory_friendly=args.memory_friendly,
                          track=args.track))
  print('Time: ',
        time.clock() - start_time)


if __name__ == '__main__':
  main()
