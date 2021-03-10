import spacy
import operator
from collections import Counter
from PyDictionary import PyDictionary

dict1 = PyDictionary()




File = open('harry1.txt',encoding="utf8") #open file
text = File.read() #read all lines



spacy_nlp  = spacy.load('en_core_web_sm')#loading the spacy small model 

# parse text into spacy document
doc = spacy_nlp(text.strip())



len(doc.ents)
labels = [x.label_ for x in doc.ents]
Counter(labels)



names =[]
for ent in doc.ents:
    entry = str(ent.lemma_).lower()
    if ent.label_ =='PERSON':
        names.append(entry.title())



count = {ent:names.count(ent) for ent in names}
print(count)
print("#####################################################")
newcount = dict(sorted(count.items(), key= operator.itemgetter(1), reverse=True))##getting the top 10 charecters from the story
print(newcount)
print(len(newcount))






values_newcount=[]
for key,value in newcount.items():
    values_newcount.append(value)
print(values_newcount)##giving only the values of the word count dictionary
print(len(values_newcount))



freq = {} 
for items in values_newcount: 
    freq[items] = values_newcount.count(items)
print(freq)##giving the freq of the occurence of numbers
            
#
#print(freq)
#sorted_freq = sorted(freq.items(), key=operator.itemgetter(1))
#print(sorted_freq)

#import collections
#sorted_dict = collections.OrderedDict(freq)
#print(sorted_dict)



values_list = []
for x in list(reversed(list(freq.keys())))[0:5]:
    values_list.append(x)
print(values_list)

key_list =[]
for key,value in newcount.items():
    for y in values_list:
        if value == y:
            key_list.append(key)
print(len(key_list))
#print(key_list)###########names that are there in the newcount with less number of occurrences


#####deleting those nouns from newcount which appeared in the key_list
name_list1= []
for key,value in newcount.items():
    name_list1.append(key)
print(name_list1)
print(len(name_list1))




#name_list1 = list(set(name_list1))
#key_list = list(set(key_list))



name_list1 = set(name_list1)-set(key_list)

#x = 1
#for w in name_list1:
#    for u in key_list:
#        if w == u:
#            name_list1.remove(w)
print(len(name_list1))

print(len(key_list))
##############################################






#######pre processing
for w in key_list:
    y = w.split()
    for r in y:
        if r == "The":
            key_list.remove(w)
print(len(key_list))
print(key_list)






            

##############deleting those nouns which have a meaning in dictionary
name_after_meaning= []
name_deleted =[]
for word in key_list:
#    if " " in word:
        words = word.split()
        for w in words:
            meaning = dict1.meaning(w)
            if meaning == None:
                name_after_meaning.append(word)
            else:
                name_deleted.append(word)
                
print(len(name_after_meaning))
print(len(name_deleted))
            

#x=1
#for w in name_after_meaning:
#    for y in name_deleted:
#        if w == y:
#            print(x)
#            x =x+1







names_after = list(set(name_after_meaning))## removing the duplicates present in the list
print(len(names_after))



name_deleted = list(set(name_deleted))## removing the duplicates present in the list
print(name_deleted)


#x=1
#for w in names_after:
#    for y in name_deleted:
#        if w == y:
#            print(x)
#            x =x+1
#            name_deleted.remove(y)

names_after = list(set(names_after) - set(name_deleted))
print(len(names_after))
print(names_after)
#######################################################




#########adding the names_after meaning to name_list1
name_list2 = name_list1
name_list2 = list(name_list2)


print(len(name_list2))
for r in names_after:
    if r not in name_list1:
        name_list2.append(r)
        
print(len(name_list2))




##########################adding prefixes
pre = ['mr','mrs','miss','dr','prof']
name_prefixes=[]
for p in pre:
    for w in newcount:
        u= w.lower()
        y = u.split()
        for i in y:
            if p == i:
                print("yes")
                name_prefixes.append(w)

print(name_prefixes)    

name_list3 = name_list2 + name_prefixes
##########################################################


##############################final names
def word2vec(word):
    from collections import Counter
    from math import sqrt

    # count the characters in word
    cw = Counter(word)
    # precomputes a set of the different characters
    sw = set(cw)
    # precomputes the "length" of the word vector
    lw = sqrt(sum(c*c for c in cw.values()))

    # return a tuple
    return cw, sw, lw

def cosdis(v1, v2):
    # which characters are common to the two words?
    common = v1[1].intersection(v2[1])
    # by definition of cosine distance we have
    return sum(v1[0][ch]*v2[0][ch] for ch in common)/v1[2]/v2[2]

name_list4=name_list3
print(len(name_list4))
threshold = 0.90     # if needed
for key in name_list3:
    for word in name_list3:
            if key != word:
                res = cosdis(word2vec(word), word2vec(key))
                
                if res>0.95:
                    print("first word '{}',second word '{}', res {}".format(word,key,res))
                    name_list4.remove(key)
print(len(name_list4))




namel2d={}
nm =[]
val=[]

for w in name_list4:
    for k,v in newcount.items():
        if w == k:
            nm.append(k)
            val.append(v)
            
#            namel2d[k].append(v)

namel2d = dict(zip(nm, val))

namel2d = dict(sorted(namel2d.items(), key= operator.itemgetter(1), reverse=True))##getting the top 10 charecters from the story
print(namel2d)
