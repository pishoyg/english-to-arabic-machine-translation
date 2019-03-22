from nltk.translate import bleu_score


class ZeroLengthGeneratorWrapper(object):
  """A hacky generator wrapper.
  nltk.translate.bleu_score expects an object that provides
  the following fuctionality:
  1. It is iterable.
  2. Its length is measurable through __len___.
  A list satisfies both requirements, while a generator only
  satisfies the first, which forces us to build lists in order
  to use the method.
  This class implements the __len__ method, returning a dummy
  value of 0, while mimicing the generator's memory-friendly
  iteration through elements, which is needed for outrageously
  large corpora.
  """

  def __init__(self, generator, track):
    self._counter = 0
    self._track = track
    self._generator = generator

  def __iter__(self):
    return self

  def __next__(self):
    if self._track:
      self._counter += 1
      if self._counter % self._track == 0:
        print(self._counter)
    return self._generator.__next__()

  def __len__(self):
    return 0


def corpus_bleu(ref_corpus_path, hyp_corpus_path, memory_friendly=True, track=10000):
  with open(ref_corpus_path) as ref_corpus_file:
    with open(hyp_corpus_path) as hyp_corpus_file:
      list_of_references = map(lambda line: [line.split()], ref_corpus_file)
      hypotheses = map(lambda line: line.split(), hyp_corpus_file)
      wrapper = (lambda gen: ZeroLengthGeneratorWrapper(gen, track)) if memory_friendly else list
      return bleu_score.corpus_bleu(wrapper(list_of_references), wrapper(hypotheses))
