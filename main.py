from textblob import TextBlob, Word
import requests, nltk, sys, wikipedia
from nltk.tree import Tree
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.chunk import tree2conlltags

def getNodes(parent):
	allLeaves = []
	for node in parent:
		if type(node) is nltk.Tree:
			allLeaves.append(node.leaves())
			getNodes(node)
	allLeaves.sort(key=len, reverse=True)
	return allLeaves

def data(topic):
	page=wikipedia.page(topic)
	return page.content

x=data("India").split('\n')
blocks=[]
for i in x:
	if i and not "=" in i:
		blocks.append(i)

# def outputQPhrase(tagList):
# 	nounPhrases = ["NN", "NNS", "NNP", "NNPS"]
# 	if tagList[1] == "PRP" or (tagList[2] == "PERSON" and tagList[1] in nounPhrases):
# 		return ("who", tagList[0])
# 	elif tagList[1] in nounPhrases and (tagList[2] != "TIME" and tagList[2] != "PERSON"):
# 		return ("what", tagList[0])
# 	elif 


def nerTagging(sentence):
	sent = tree2conlltags(ne_chunk(pos_tag(word_tokenize(sentence))))
	temp = []
	skip_next = False
	for (i,tag) in enumerate(sent):
		if skip_next:
			skip_next = False
			continue
		if "-" in tag[2]:
			if (i+1) <len(sent) and '-' in sent[i+1][2] and tag[2].split('-')[1]==sent[i+1][2].split('-')[1]:
				skip_next = True
				temp.append((tag[0] + sent[i+1][0], tag[1], tag[2].split("-")[1]))
			else:
				temp.append((tag[0], tag[1], tag[2].split("-")[1]))
		else:
			temp.append((tag[0], tag[1], tag[2]))
	# print (temp)
	# final = []
	# for t in temp:
	# 	final.append(outputQPhrase(t))


def genQuestion(sent):
	if type(sent) is str:
		sent = TextBlob(sent)
	bucket = {}
	for i,j in enumerate(sent.tags):
		if j[1] not in bucket:
			bucket[j[1]] = i
	question = ''

sentences=[]
for i in blocks:
	sentences+=i.split(".")


rules = [
	"VP < (S=unmv $,, /,/)",
	"S < PP|ADJP|ADVP|S|SBAR=unmv > ROOT",
	"/\\.*/ < CC << NP|ADJP|VP|ADVP|PP=unmv",
	"SBAR < (IN|DT < /[^that]/) << NP|PP=unmv",
	"SBAR < /^WH.*P$/ << NP|ADJP|VP|ADVP|PP=unmv",
	"SBAR <, IN|DT < (S < (NP=unmv !$,, VP))",
	"NP << (PP=unmv !< (IN < of|about))",
	"PP << PP=unmv",
	"NP $ VP << PP=unmv",
	"SBAR=unmv [ !> VP | $-- /,/ | < RB ]",
	"SBAR=unmv !< WHNP <(/^[^S].*/ !<< that|whether|how)",
	"NP=unmv < EX",
	" /^S/ < '' << NP|ADJP|VP|ADVP|PP=unmv",
	"PP=unmv !< NP",
	"NP=unmv $ @NP",
	"NP|PP|ADJP|ADVP << NP|ADJP|VP|ADVP|PP=unmv",
	"@UNMV << NP|ADJP|VP|ADVP|PP=unmv"
]
url = "http://localhost:9010/tregex"
treesList = []
data = [sentences[0]]
# data = ["Darwin studied how species evolve"]
# print(data)
print (data[0])

for (i,text) in enumerate(data):
	temp = []
	for rule in rules:
		request_params = {"pattern": rule}
		r = requests.post(url, data=text.encode('utf-8'), params=request_params)
		s = r.json()
		# print (s['sentences'])
		temp.append(list(s['sentences']))
	unmovableWords = []
	for j in temp:
		for k in j:
			for l in k:
				if 'namedNodes' in k[l]:
					if 'unmv' in k[l]['namedNodes'][0]:
						string = k[l]['namedNodes'][0]['unmv']
						unmovableWords.extend(getNodes(Tree.fromstring(string)))
	unmovableWords.sort(key=len, reverse=True)
	finalList = []
	exceptions = ["-LRB-", "-RRB-", ":", ","]
	for phrase in unmovableWords:
		tmp = []
		for word in phrase:
			if word not in exceptions:
				tmp.append(word)
		finalList.append(tmp)
	finalList.sort(key=len, reverse=True)
	sentExceptions = ["(",")",":",","]
	for sentExcept in sentExceptions:
		text = text.replace(sentExcept, "")
	allPhrases = []
	# print(finalList)
	for phraseList in finalList:
		phrase = " ".join(phraseList)
		text = text.replace(phrase, "*#$%")
	
	allPhrases = text.split("*#$%")
	for phraseList in allPhrases:
		# print ("phraseList:",phraseList)
		for item in phraseList:
			nerTagging(item.strip())
	print ("****",text.strip(),"****")




# for sent in nltk.sent_tokenize(sentence):
#    for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
#       if hasattr(chunk, 'label'):
#          print(chunk.label(), ' '.join(c[0] for c in chunk))
