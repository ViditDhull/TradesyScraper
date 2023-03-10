from bs4 import BeautifulSoup
import requests
import json
import sys

source_id=str(sys.argv[1])
filename_id=str(sys.argv[2])
url=str(sys.argv[3])
tags=str(sys.argv[5])
tags=tags.split(',')
ids=str(sys.argv[6])
ids=ids.split(',')
classes=str(sys.argv[7])
classes=classes.split(',')
classes=classes

# output = source_id+'/scrapped/'+filename_id+'.json'
output = filename_id+'.json'
result = []

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

file = requests.get(url, headers=headers)
data = file.text
soup = BeautifulSoup(data, 'html.parser')

tags_dict = {}
for t in tags:
    t1 = []
    if t == 'meta':
        metas = soup.find_all(t)
        for i in metas:
            if 'property' in i.attrs:
                t1.append(i.attrs)
            elif 'name' in i.attrs:
                t1.append(i.attrs)
    
    if t == 'link':
        links = soup.find_all(t)
        for i in links:
            d = {'rel':i['rel'], 'href':i['href']}
            t1.append(d)
            
    if t == 'script':
        scripts = soup.find_all(t)
        for i in scripts:
            if 'type' in i.attrs:
                e = {'type':i['type'], 'innerhtml':i.decode_contents()}
                t1.append(e)
            


    tags_dict[t] = t1

result.append({'tags':tags_dict})    
    
ids_dict = {}
for k in ids:
    idp = []
    idps = soup.find_all(id=k)
    a = 0
    for i in idps:
        idp.append({a:{"innerhtml":i.decode_contents()}})
        a += 1
        
    ids_dict[k] = idp

result.append({'ids':ids_dict})    
    
classes_dict = {}
for c in classes:
    if c == 'img__1bebd':
        img = []
        imgs = soup.find_all('img', {"class": c})
        for i in imgs:
            f = {'class':i['class'], 'src':i['src'], 'loading':i['loading'], 'alt':i['alt']}
            img.append(f)
        classes_dict[c] = img
    else:
        idp = []
        print(c)

        if c == 'text-wrap':
            idps = soup.find_all('span', {'class': 'text-wrap'})
            a = 0
            for s in idps:
                idp.append({a:s.text})
            a += 1

        if c == 'brand':
            idps = soup.find_all('div', {'itemprop': 'brand'})
            a = 0
            for s in idps:
                idp.append({a:s.text})
            a += 1

        if c == 'original-price':
            idps = soup.find_all('span', {'class': 'original-price'})
            a = 0
            for s in idps:
                idp.append({a:s.text})
            a += 1

        if c == 'idp-item-size':
            idps = soup.find_all('span', {'data-testid': 'idp-item-size'})
            a = 0
            for s in idps:
                idp.append({a:s.text})
            a += 1

        if c == 'idp-accordion-panel':
            idps = soup.find_all('div', {'class': 'idp-accordion-panel'})
            a = 0
            for s in idps:
                idp.append({a:s.text})
            a += 1   

        if c == 'title':
            idps = soup.find_all('span', {'class': 'title'})
            a = 0
            for s in idps:
                idp.append({a:s.text})
            a += 1

        if c == 'condition':
            idps = soup.find_all('b', {'class': 'condition'})
            a = 0
            for s in idps:
                idp.append({a:s.text})
            a += 1

        classes_dict[c] = idp
    
result.append({'classes':classes_dict})

with open(output, 'w') as fp:
    json.dump(result, fp)

print(output)
