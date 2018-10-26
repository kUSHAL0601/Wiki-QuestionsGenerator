from textblob import TextBlob, Word
import requests, nltk, sys, wikipedia


def data(topic):
	page=wikipedia.page(topic)
	return page.content

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
for (i,text) in enumerate(sentences):
	temp = []
	for rule in rules:
		request_params = {"pattern": rule}
		r = requests.post(url, data=text.encode('utf-8'), params=request_params)
		# print (text)
		# print (r.text)
		temp.append(r.json())
	treesList.append(temp)

