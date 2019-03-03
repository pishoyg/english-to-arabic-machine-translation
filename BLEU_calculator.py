from nltk.translate.bleu_score import corpus_bleu

candidatePath = 'ISI.ara.cand'
referencePath = 'ISI.ara.ref'


candidate = []
with open(candidatePath,'r') as f:
	for line in f:
		for word in line.split():			
			candidate.append(word)
#convert candidate (machine translated) corpus to 2d array proper format
c2 = [candidate]

#get reference (proper translation) corpus and format into 3d array
ref = []
with open(referencePath,'r') as f:
	for line in f:
		for word in line.split():			
			ref.append(word)
reference = [[ref]]

score = corpus_bleu(reference, c2)
print('BLEU Score: ' + str(score))