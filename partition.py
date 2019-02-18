import argparse
import random

parser = argparse.ArgumentParser(description='Split dataset into partitions.')
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
parser.add_argument(
  '--partitions',
  type=str,
  help='Partitions.',
  nargs=3,
  default=['train', 'dev', 'test']
)
parser.add_argument(
  '--partition_distributions',
  type=float,
  help='Partition distributions.',
  nargs=3,
  default=[0.9, 0.95, 1.0]
)
args = parser.parse_args()
is_valid_prop = lambda x: x >= 0.0 and x <= 1.0
assert len(args.partitions) == len(args.partition_distributions)
assert all(is_valid_prop(p) for p in args.partition_distributions)
args.partition_distributions = {partition: prop for partition, prop in zip(args.partitions, args.partition_distributions)}

corpora = dict()
for lang in args.langs:
  with open('.'.join([args.input, lang])) as input_file:
    corpora[lang] = input_file.read().split('\n')
corpora = list(zip(*[corpora[lang] for lang in args.langs]))
random.shuffle(corpora)

output = {
  (partition, lang): []
  for lang in args.langs for partition in args.partitions
}

for lang_sentences in corpora:
  r = random.uniform(0.0, 1.0)
  partition = None
  for loop_partition in args.partitions:
    if r <= args.partition_distributions[loop_partition]:
      partition = loop_partition
      break
  if not partition:
    raise ValueError('Invalid partition distribution!')
  assert len(args.langs) == len(lang_sentences)  # Sanity check. It is sure to be true.
  for lang, sentence in zip(args.langs, lang_sentences):
    output[(partition, lang)].append(sentence)

for partition_lang_tuple, partition_lang_output in output.items():
  partition = partition_lang_tuple[0]
  lang = partition_lang_tuple[1]
  with open('.'.join([args.input, partition] + [lang]), 'w') as output_file:
    output_file.write('\n'.join(partition_lang_output))
