import lang_cleaner
import argparse
import xml.etree.ElementTree as ET
# Define arguments.
parser = argparse.ArgumentParser(description=
  'DO NOT SUBMIT.',
  formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
  '--madamira_xmls',
  type=str,
  nargs='+',
  required=True,
  help='Path to MADAMIRA xml outputs.'
)
parser.add_argument(
  '--lookup_table',
  type=str,
  default='lookup_table.txt',
  help='Path to output file to save lookup table.'
)
parser.add_argument(
  '--xmlns',
  type=str,
  default='urn:edu.columbia.ccls.madamira.configuration:0.1',
  help='XML Namespace.'
)
args = parser.parse_args()


def main():
  def get_descendants(parent, child_tag):
    return parent.findall('.//ns:' + child_tag, {'ns': args.xmlns})
  lookup_table = dict()
  cleaner = lang_cleaner.lang_to_cleaner['ara']
  for madamira_xml in args.madamira_xmls:
    print('Processing %s.' % madamira_xml)
    root = ET.parse(madamira_xml).getroot()
    for word_info in get_descendants(root, 'word_info'):
      for word in get_descendants(word_info, 'word'):
        desegmented = cleaner.clean(word.get('word'))
        if not desegmented:
          continue
        tokenized = list(filter(lambda x: x.get('scheme') =='MyD3',
                                get_descendants(word, 'tokenized')))
        assert len(tokenized) == 1
        tokenized = tokenized[0]
        segmented = [
            cleaner.clean(tok.get('form0'))
            for tok in get_descendants(tokenized, 'tok')]
        assert segmented
        segmented = ' '.join(segmented)
        if segmented not in lookup_table:
          lookup_table[segmented] = dict()
        if desegmented not in lookup_table[segmented]:
          lookup_table[segmented][desegmented] = 0
        lookup_table[segmented][desegmented] += 1
  lookup_table = {segmented: max(desegmented.items(), key=lambda x: x[1])[0] for segmented, desegmented in lookup_table.items()}
  with open(args.lookup_table, 'w') as lookup_table_file:
    lookup_table_file.write(''.join(k + ':' + v + '\n' for k, v in lookup_table.items()))

if __name__ == '__main__':
  main()

