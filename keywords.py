import json

file_name = 'keywords.json'

f = open(file_name)
d = 1
dictMerged2 = {}
try:
    while True:
        line = f.readline()
        r = json.loads(line)
        r['keyword%s'%d] = r.pop('keyword')
        r['B%s'%d] = r.pop('article_id')
        r['A%s'%d] = d
        dictMerged2 = dict(dictMerged2, **r)
        d += 1

except:
    f.close()
m = 2
for m in range(2,736):
    if dictMerged2['B%s'%m] == dictMerged2['B%s'%(m-1)]:
        dictMerged2['A%s'%m] = dictMerged2['A%s'%(m-1)]
    else:
        dictMerged2['A%s'%m] = dictMerged2['A%s'%(m-1)] +1
    m+=1
print(dictMerged2)
for i in range(1,736):
    for j in range(i+1,736):
        if dictMerged2['keyword%s'%i] == dictMerged2['keyword%s'%(j)]:
            print(dictMerged2['A%s'%i],dictMerged2['A%s'%j])
        j += 1
    i+= 1