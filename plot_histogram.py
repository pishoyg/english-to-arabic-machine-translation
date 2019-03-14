import argparse
from itertools import chain
from collections import Counter
import matplotlib.pyplot as plt

# Arguments.
parser = argparse.ArgumentParser(description=
  'Generate frequency plots.',
  formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

parser.add_argument(
    '--ref_freq_path',
    type=str,
    required=True,
    help='Full path to file in CSV-format containing words and their respective '
    'reference frequencies.'
)
parser.add_argument(
    '--freq_paths',
    type=str,
    nargs='*',
    default=[],
    help='List of paths to files in CSV-format containing words and their respective '
    'frequencies, to compare against the reference histogram.'
)
parser.add_argument(
    '--delim',
    type=str,
    help='String used as a delimiter between words and their respective '
    'counts in the frequency file.',
    default=' '
)
parser.add_argument(
    '--plot_windows',
    type=str,
    help='Plot windows. Will plot a histogram for word frequencies '
    'for each given subrange of the descendingly sorted vocab list. '
    'A value of zero on the left/right side indicates the absence of '
    'a lower/upper bound.',
    nargs='+',
    default=['0:40000']
)
parser.add_argument(
    '--curb_freq',
    type=int,
    help='Curb frequency.',
    default=1000
)
parser.add_argument(
    '--format',
    type=str,
    help='Image format.',
    default='jpg'
)
parser.add_argument(
    '--x_step',
    type=int,
    help='Grid step on the x-axis.',
    default=4000
)
parser.add_argument(
    '--y_step',
    type=int,
    help='Grid step on the y-axis.',
    default=50
)

args = parser.parse_args()


def get_histogram_as_dict(freq_path):
  histogram = dict()
  with open(freq_path) as freq_file:
    for line in freq_file.readlines():
      word, freq = line.split(args.delim)
      freq = int(freq)
      histogram[word] = freq
  return histogram


def get_histogram_as_list(freq_path):
  frequencies = list()
  words = list()
  with open(freq_path) as freq_file:
    for line in freq_file.readlines():
      word, freq = line.split(args.delim)
      words.append(word)
      frequencies.append(int(freq))
  return words, frequencies


def main():
  all_words, all_frequencies = get_histogram_as_list(args.ref_freq_path)
  assert len(all_words) == len(all_frequencies)
  histograms = [
      get_histogram_as_dict(freq_path)
      for freq_path in args.freq_paths]
  for plot_window in args.plot_windows:
    words, frequencies = all_words, all_frequencies
    s, e = list(map(int, plot_window.split(':')))
    assert s <= e, 'Invlid window: %s' % plot_window
    if e > len(words):
      words = words + [0] * (e - len(words))
      frequencies = frequencies + [0] * (e - len(frequencies))
    none_if_zero = lambda x: x if x else None
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xticks(range(s, e, args.x_step))
    ax.set_yticks(range(0, args.curb_freq, args.y_step))
    plt.plot(frequencies[none_if_zero(s):none_if_zero(e)])
    for histogram in histograms:
      plt.plot(list(histogram.get(word, 0) for word in words), 'o', markersize=1)
    plt.axis([s, e, 0, args.curb_freq])
    plt.xlabel('Order')
    plt.ylabel('Frequency')
    plt.grid(True)
    # Save and clear.
    plt.savefig('.'.join(filter(None,
        [args.ref_freq_path, 'histogram', plot_window.replace(args.delim, '-'), args.format]
    )))
    plt.clf()

if __name__ == '__main__':
  main()

