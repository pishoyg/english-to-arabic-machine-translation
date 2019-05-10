import argparse

# Define arguments.
parser = argparse.ArgumentParser(description=
  'Detokenize.',
  formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
  '--lookup_table',
  type=str,
  required=True,
  help='Path to lookup table.'
)
parser.add_argument(
  '--tok',
  type=str,
  required=True,
  help='Path to input tokenized corpus.'
)
parser.add_argument(
  '--detok',
  type=str,
  required=True,
  help='Path to output detokenized corpus.'
)
args = parser.parse_args()


trie = [dict(), None]


def TrieInsert(tok, detok):
  node = trie
  for word in tok:
    if word not in node[0]:
      node[0][word] = [dict(), None]
    node = node[0][word]
  node[1] = detok


words = None
def process(idx, strict=True):
  if idx == len(words):
    return True, []
  node = trie
  attempts = list()
  start = idx
  while idx < len(words) and words[idx] in node[0]:
    node = node[0][words[idx]]
    idx += 1
    if node[1]:
      attempts.append((node[1], idx))
  # Reverse attempts to consider the longest attempt first, according to the maximum-munch principle.
  attempts = reversed(attempts)
  for buildup, idx in attempts:
    success, sentence = process(idx, strict)
    if success:
      return True, [buildup] + sentence
  if not strict:
    return True, words[start] + process(start + 1, strict)
  return False, None


def main():
  with open(args.lookup_table) as lookup_table_file:
    for line in lookup_table_file.readlines():
      tok, detok = line.split(':')
      tok = tok.split()
      detok = detok.strip()
      TrieInsert(tok, detok)
  global words
  with open(args.detok, 'w') as detok:
    with open(args.tok) as tok:
      for line in tok:
        words = line.split()
        success, sentence = process(0)
        if not success:
          success, sentence = process(0, False)
          assert success
        detok.write(' '.join(sentence) + '\n')
        print(' '.join(sentence) + '\n')

if __name__ == '__main__':
  main()
