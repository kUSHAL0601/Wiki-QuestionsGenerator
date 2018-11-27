from textblob import TextBlob, Word
import requests, nltk, sys, wikipedia, re
from nltk.tree import Tree
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.chunk import tree2conlltags

def data(topic):
    page=wikipedia.page(topic)
    return page.content

x=data("India").split('\n')
blocks=[]
for i in x:
    if i and not "=" in i:
        blocks.append(i)

sentences=[]
for i in blocks:
    sentences+=i.split(".")

def outputQPhrase(phraseList):
    nounPhrases = ["NN", "NNS", "NNP", "NNPS"]
    posTagList = [phrase[1] for phrase in phraseList]
    output = []
    for (i,wordTuple) in enumerate(phraseList):
        if wordTuple[1] == "PRP" or (wordTuple[2] == "PERSON" and wordTuple[1] in nounPhrases):
            output.append(("who", wordTuple[0]))
        if not (wordTuple[2] == "PERSON" or wordTuple[2] == "TIME") and wordTuple[1] in nounPhrases:
            output.append(("what", wordTuple[0]))
        if wordTuple[2] == "GPE" and "IN" in posTagList and wordTuple[1] in nounPhrases:
            inIndex = posTagList.index("IN")
            if inIndex < i and phraseList[inIndex] in ["on", "in", "at", "over", "to"]:
                output.append(("where", wordTuple[0]))
        if (wordTuple[2] == "TIME" and wordTuple[1] in nounPhrases) or (re.match("[1|2]\d\d\d$",wordTuple[0])):
            output.append(("when", wordTuple[0]))
        if (wordTuple[2] == "PERSON" and wordTuple[1] in nounPhrases) and i<(len(phraseList)-1) and phraseList[i+1][1] == "POS":
            try:
                nextNPIdx = [posTagList.index(i) for i in posTagList[i+1:] if i in nounPhrases][0]
                output.append(("whose " + phraseList[nextNPIdx][0], wordTuple[0]))
            except:
                pass
        if (wordTuple[1] == "CD"):
            try:
                nextNPIdx = [posTagList.index(i) for i in posTagList[i+1:] if i in nounPhrases][0]
                output.append(("how many " + phraseList[nextNPIdx][0], wordTuple[0]))
            except:
                pass
    return output

def getNodes(parent):
    allLeaves = []
    for node in parent:
        if type(node) is nltk.Tree:
            allLeaves.append(node.leaves())
            getNodes(node)
    allLeaves.sort(key=len, reverse=True)
    return allLeaves

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
                temp.append((tag[0] + " " + sent[i+1][0], tag[1], tag[2].split("-")[1]))
            else:
                temp.append((tag[0], tag[1], tag[2].split("-")[1]))
        else:
            temp.append((tag[0], tag[1], tag[2]))
    output = []
    print (temp)
    return outputQPhrase(temp)

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
data = sentences[:5]
for (i,text) in enumerate(data):
    temp = []
    for rule in rules:
        request_params = {"pattern": rule}
        r = requests.post(url, data=text.encode('utf-8'), params=request_params)
        s = r.json()
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

    for phraseList in finalList:
        phrase = " ".join(phraseList)
        pattern = "\s(" + phrase + ")[\s|,|:|-]"
        tp = " " + text + " "
        text = re.sub(pattern, " *#$% ", tp).strip()

    allPhrases = text.split("*#$%")
    questionsList = []
    for phrase in allPhrases:
        questionsList.append(nerTagging(phrase))
