import argparse
import random

parser = argparse.ArgumentParser(description='Split dataset into \'train\' (~5%), \'dev\'(~5%), and \'test\'(~90%) partitions.')
parser.add_argument(
  '--input',
  type=str,
  help='Input path.',
  required=True
)
parser.add_argument(
  '--langs',
  type=str,
  help='Language suffixes.',
  nargs=2,
  default=['ara', 'eng']
)
args = parser.parse_args()

corpora = dict()
for lang in args.langs:
  with open('.'.join([args.input, lang])) as input_file:
    corpora[lang] = input_file.read().split('\n')

output = {
  (partition, lang): open('.'.join([args.input, partition, lang]), 'w')
  for lang in args.langs for partition in ['train', 'dev', 'test']
}

for sentences in zip(*[corpora[lang] for lang in args.langs]):
  r = random.uniform(0.0, 1.0)
  if r < 0.05:
    partition = 'dev'
  elif r < 0.1:
    partition = 'test'
  else:
    partition = 'train'
  assert len(args.langs) == len(sentences)  # Sanity check.
  for lang, sentence in zip(args.langs, sentences):
    output[(partition, lang)].write(sentence + '\n')

for _, f in output.items():
  f.close()
