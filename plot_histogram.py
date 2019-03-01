import argparse
from itertools import chain
from collections import Counter
import matplotlib.pyplot as plt

# Arguments.
parser = argparse.ArgumentParser(description=
  'Generate frequency plots.'
)

parser.add_argument(
    '--freq_path',
    type=str,
    required=True,
    help='Full path to file in CSV-format containing words and their respective '
    'frequencies.'
)
parser.add_argument(
    '--delim',
    type=str,
    help='String used as a delimiter between words and their respective '
    'counts in the frequency file.',
    nargs=1,
    default=' '
)
parser.add_argument(
    '--plot_windows',
    type=str,
    help='Plot windows. Will plot a histogram for word frequencies '
    'for each prefix of length <plot_window> from the descendingly '
    'sorted vocab array. A value of zero indicates printing the entire '
    'vocab.',
    nargs='+',
    default=['0:40000']
)
parser.add_argument(
    '--curb_freq',
    type=int,
    help='Curb frequency.',
    nargs=1,
    default=1000
)
parser.add_argument(
    '--x_step',
    type=int,
    help='Grid step on the x-axis.',
    nargs=1,
    default=4000
)
parser.add_argument(
    '--y_step',
    type=int,
    help='Grid step on the y-axis.',
    nargs=1,
    default=50
)

args = parser.parse_args()

def main():
  with open(args.freq_path) as freq_file:
    histogram = list(
      map(
        lambda line: int(line.split(args.delim)[1]),
        freq_file.read().split('\n')
      )
    )
  max_freq = max(histogram)
  for plot_window in args.plot_windows:
    s, e = list(map(int, plot_window.split(':')))
    assert s <= e
    if e > len(histogram):
      histogram = histogram + [0] * (e - len(histogram))
    none_if_zero = lambda x: x if x else None
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xticks(range(s, e, args.x_step))
    ax.set_yticks(range(0, args.curb_freq, args.y_step))
    plt.fill_between(range(s, e), 0, histogram[none_if_zero(s):none_if_zero(e)])
    plt.axis([s, e, 0, args.curb_freq])
    plt.xlabel('Order')
    plt.ylabel('Frequency')
    plt.grid(True)
    # Save and clear.
    plt.savefig('.'.join(filter(None,
        [args.freq_path, 'histogram', plot_window.replace(args.delim, '-'), 'jpg']
    )))
    plt.clf()

if __name__ == '__main__':
  main()

