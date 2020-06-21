from konlpy.tag import Mecab
from pymongo import MongoClient

stop_word = dict()
DBname = "db20140825"
conn = MongoClient("localhost")
db = conn[DBname]

def make_stop_word():
    # stop words in wordList.txt
    f = open('wordList.txt', 'r')
    while True:
        line = f.readline()
        if not line:
            break
        stop_word[line.strip()] = True
    f.close()


# Data Copy function
def p0():
    col1 = db['news']
    col2 = db['news_freq']

    # renew the collection : news_freq
    col2.drop()
    
    # colletion > document > key:value
    for doc in col1.find():
        contentDic = dict()
        # copy the data from news col. into news_freq col.
        # except "_id" key-value
        for key in doc.keys():
            if key != "_id":
                contentDic[key] = doc[key]
        col2.insert(contentDic)


# store morphemes into news_freq and update document id in news_freq
def p1():
    for doc in db['news_freq'].find():
        doc['morph'] = morphing(doc['content'])
        db['news_freq'].update({"_id": doc["_id"]}, doc)


# store nouns, not stop_word
def morphing(content):
    # morpheme analyzer : mecab
    mecab = Mecab()
    morphList = []
    for word in mecab.nouns(content):
        if word not in stop_word:
            morphList.append(word)
    return morphList


# print out the morphs from a random news
def p2():
    doc = db['news_freq'].find_one()
    for m in doc['morph']:
        print(m)


# create new collection : wordset
def p3():
    col1 = db['news_freq']
    col2 = db['news_wordset']

    # renew the collection
    col2.drop()
    
    # make new wordset collection from news_freq
    # remove redundant words
    for doc in col1.find():
        new_doc = dict()
        new_set = set()
        for w in doc['morph']:
            new_set.add(w)

        # news_wordset schema
        # : _id, word_set, news_freq_id
        new_doc['word_set'] = list(new_set)
        new_doc['news_freq_id'] = doc['_id']
        col2.insert(new_doc)


# create new collection : wordset
def p4():
    doc = db['news_wordset'].find_one()
    for w in doc['word_set']:
        print(w)


def p5(length):
	colf = db['news_freq']
    colw = db['news_wordset']

    min_sup = db['news'].count() * 0.04
	
	# L1
    col1 = db['candidate_L1']
    col1.drop()

    # get the support value for 1 word
	word_support = dict()
	for doc in colw.find():
		# count the support value
        for word in doc['morph']:
			word_support[word] = word_support.get(word, 0) + 1

	# save the item of word_support whose support is not less than min_sup
	for word, support in word_support.items():
		if support >= min_sup:
			col1.insert({'item_set':word, 'support':support})

    if length == 1: 
		return
	

	# L2
    col_cand2 = db['candidate_L2']
    col_cand2.drop()



    for i in range(0, len(temp_list3)-1):
        for j in range(i+1, len(temp_list3)):
            sumin = list()
            sumin.append(temp_list3[i])
            sumin.append(temp_list3[j])
            temp_list2.append(sumin)

    temp_list = list()

    # C2
    for wduo in temp_list2:
        count = 0
        for doc in col_word.find():
            if wduo[0].decode('utf-8') in doc['word_set'] 
				and wduo[1].decode('utf-8') in doc['word_set']:
                count += 1
        #L2
        if count >= min_sup:
            temp_list.append(wduo)
            temp_doc = {}
            temp_doc['item_set'] = wduo
            temp_doc['support'] = count
            col_cand2.insert(temp_doc)

    if length == 2:
        return

    col_cand3 = db['candidate_L3']
    col_cand3.drop()

    count = 0
    temp_list2 = list()

    # C3 - candidate
    for i in range(0, len(temp_list) - 1):
        for j in range(i+1, len(temp_list)):
            if temp_list[i][1] == temp_list[j][0]:
                search = list()
                search.append(temp_list[i][0])
                search.append(temp_list[j][1])
                if search in temp_list:
                    sumin = list(temp_list[i])
                    sumin.append(temp_list[j][1])
                    temp_list2.append(sumin)

    temp_list = list()
    # C3
    for wtrio in temp_list2:
        count = 0
        for doc in col_word.find():
            if wtrio[0].decode('utf-8') in doc['word_set'] and wtrio[1].decode('utf-8') in doc['word_set'] and wtrio[2].decode('utf-8') in doc['word_set']:
                count += 1
        #L3
        if count >= min_sup:
            temp_list.append(wtrio)
            temp_doc = {}
            temp_doc['item_set'] = wtrio
            temp_doc['support'] = count
            col_cand3.insert(temp_doc)



def p6(length):
    pass

def printMenu():
    print("0. CopyData")
    print("1. Morph")
    print("2. print Morphs")
    print("3. print wordset")
    print("4. frequent item set")
    print("5. association rule")

if __name__ == "__main__":
    make_stop_word()
    printMenu()
    selector = int(input())
    if selector == 0:
        p0()
    elif selector == 1:
        p1()
        p3()
    elif selector == 2:
        p2()
    elif selector == 3:
        p4()
    elif selector == 4:
        print("input length of the frequent item:")
        length = int(input())
        p5(length)
    elif selector == 5:
        print("input length of the frequent item:")
        length = int(input())
        p6(length)

