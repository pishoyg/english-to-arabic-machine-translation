from nltk.translate import bleu_score

def corpus_bleu(ref_corpus_path, hyp_corpus_path):
  with open(ref_corpus_path) as ref_corpus_file:
    with open(hyp_corpus_path) as hyp_corpus_file:
      list_of_references = map(lambda line: [line.split()], ref_corpus_file)
      hypotheses = map(lambda line: line.split(), hyp_corpus_file)
      return bleu_score.corpus_bleu(list_of_references, hypotheses)
