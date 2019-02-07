import argparse
import random

parser = argparse.ArgumentParser(description='Argument parser.')
parser.add_argument('--input', type=str, help='Input path.', required=True)
parser.add_argument('--langs', type=str, help='Language suffixes.', nargs=2, required=True, default=['ara', 'eng'])

args = parser.parse_args()

with corpus_file as open('.'.join([args.input, lang])):
    corpus = {lang: corpus_file.read().split('\n') for lang in langs}
output = {
  (partition, lang): open('.'.join([args.input, partition, lang]), 'w')
  for lang in langs for partition in ['train', 'dev', 'test']
}

for ara_line, eng_line in zip(corpus['ara'], corpus['eng']):
  r = random.uniform(0.0, 1.0)
  if r < 0.05:
    partition = 'dev'
  elif r < 0.1:
    partition = 'test'
  else:
    partition = 'train'
  output[(partition, 'ara')].write(ara_line + '\n')
  output[(partition, 'eng')].write(eng_line + '\n')

for _, f in output.items():
  f.close()

