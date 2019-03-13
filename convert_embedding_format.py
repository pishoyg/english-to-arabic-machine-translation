import gensim
import argparse


parser = argparse.ArgumentParser(
  description='Convert word2vec model to text format.',
  formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
  '--input_mdl',
  type=str,
  required=True,
  help='Path to input model in gensim-compatiable format.'
)
parser.add_argument(
  '--output_txt',
  type=str,
  default='email_specs.json',
  help='Path to output model in text format.'
)
args = parser.parse_args()


def main():
  model = gensim.models.Word2Vec.load(args.input_mdl)
  model.wv.save_word2vec_format(
      args.output_txt,
      binary=False)


if __name__ == '__main__':
  main()

