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
memo = None
def process(idx, strict=True):
  if idx in memo and (strict or memo[idx] is not None):
    return memo[idx]
  ans = None
  node = trie
  attempts = list()
  next = idx
  while next < len(words) and words[next] in node[0]:
    node = node[0][words[next]]
    next += 1
    if node[1]:
      attempts.append((node[1], next))
  # Reverse attempts to consider the longest attempt first, according to the maximum-munch principle.
  attempts = reversed(attempts)
  for buildup, next in attempts:
    process(next, strict)
    if memo[next] is not None:
      ans = [buildup] + memo[next]
      break
  if ans is None and not strict:
    process(idx + 1, strict)
    assert memo[idx + 1] is not None
    ans = [words[idx]] + memo[idx + 1]
  memo[idx] = ans


def main():
  with open(args.lookup_table) as lookup_table_file:
    for line in lookup_table_file.readlines():
      tok, detok = line.split(':')
      tok = tok.split()
      detok = detok.strip()
      TrieInsert(tok, detok)
  global words
  global memo
  with open(args.detok, 'w') as detok:
    with open(args.tok) as tok:
      for i, line in enumerate(tok):
        words = line.split()
        memo = {len(words): []}
        process(0)
        if memo[0] is None:
          process(0, False)
          assert memo[0] is not None
        final = ' '.join(memo[0])
        detok.write(final + '\n')
        print(i)


if __name__ == '__main__':
  main()
