import wikipedia
from textblob import TextBlob
import nltk
from textblob import Word
import sys

# from textblob import TextBlob

def data(topic):
	page=wikipedia.page(topic)
	# print(page.content)
	return page.content
	# print(page.summary)

x=data("India").split('\n')
blocks=[]
for i in x:
	if i and not "=" in i:
		blocks.append(i)


def genQuestion(sent):
	if type(sent) is str:
		sent = TextBlob(sent)
	bucket = {}
	for i,j in enumerate(sent.tags):
		if j[1] not in bucket:
			bucket[j[1]] = i
	# print(bucket)
	question = ''

	# Rule based approach

	l1 = ['NNP', 'VBG', 'VBZ', 'IN']
	l2 = ['NNP', 'VBG', 'VBZ']
	l3 = ['PRP', 'VBG', 'VBZ', 'IN']
	l4 = ['PRP', 'VBG', 'VBZ']
	l5 = ['PRP', 'VBG', 'VBD']
	l6 = ['NNP', 'VBG', 'VBD']
	l7 = ['NN', 'VBG', 'VBZ']
	l8 = ['NNP', 'VBZ', 'JJ']
	l9 = ['NNP', 'VBZ', 'NN']
	l10 = ['NNP', 'VBZ']
	l11 = ['PRP', 'VBZ']
	l12 = ['NNP', 'NN', 'IN']
	l13 = ['NN', 'VBZ']
	if all(key in  bucket for key in l1):
		question = 'What' + ' ' + sent.words[bucket['VBZ']] +' '+ sent.words[bucket['NNP']]+ ' '+ sent.words[bucket['VBG']] + '?'
	elif all(key in  bucket for key in l2):
		question = 'What' + ' ' + sent.words[bucket['VBZ']] +' '+ sent.words[bucket['NNP']] +' '+ sent.words[bucket['VBG']] + '?'
	elif all(key in  bucket for key in l3):
		question = 'What' + ' ' + sent.words[bucket['VBZ']] +' '+ sent.words[bucket['PRP']]+ ' '+ sent.words[bucket['VBG']] + '?'
	elif all(key in  bucket for key in l4):
		question = 'What ' + sent.words[bucket['PRP']] +' '+  ' does ' + sent.words[bucket['VBG']]+ ' '+  sent.words[bucket['VBG']] + '?'
	elif all(key in  bucket for key in l7):
		question = 'What' + ' ' + sent.words[bucket['VBZ']] +' '+ sent.words[bucket['NN']] +' '+ sent.words[bucket['VBG']] + '?'
	elif all(key in bucket for key in l8):
		question = 'What' + ' ' + sent.words[bucket['VBZ']] + ' ' + sent.words[bucket['NNP']] + '?'
	elif all(key in bucket for key in l9):
		question = 'What' + ' ' + sent.words[bucket['VBZ']] + ' ' + sent.words[bucket['NNP']] + '?'
	elif all(key in bucket for key in l11):
		if sent.words[bucket['PRP']] in ['she','he']:
			question = 'What' + ' does ' + sent.words[bucket['PRP']].lower() + ' ' + sent.words[bucket['VBZ']].singularize() + '?'
	elif all(key in bucket for key in l10):
		question = 'What' + ' does ' + sent.words[bucket['NNP']] + ' ' + sent.words[bucket['VBZ']].singularize() + '?'
	elif all(key in bucket for key in l13):
		question = 'What' + ' ' + sent.words[bucket['VBZ']] + ' ' + sent.words[bucket['NN']] + '?'

	if 'VBZ' in bucket and sent.words[bucket['VBZ']] == "’":
		question = question.replace(" ’ ","'s ")
	return question

sentences=[]
for i in blocks:
	sentences+=i.split(".")

qsns=[]
for i in sentences:
	qsn=genQuestion(i)
	if qsn:
		qsns.append(qsn)
		print(qsn)
qsns=list(set(qsns))