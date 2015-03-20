import requests
from pyquery import PyQuery as pq

def findNewBase(url):
    if '.' in url.split('/')[-1]:
        return url[:(-1 * len(url.split('/')[-1]))].rstrip('/') + '/'
    else:
        return url.rstrip('/') + '/'

def findJob(url,linklist,origin):
    global outputFile
    global supercounter
    supercounter = supercounter + 1

    try:
        r = requests.Session().get(url)
    except:
        print "!!!!!!FAILUIRE!!!!!!\n" + url + "\n!!!!!!FAILuRE!!!!!!\n"
    try:
        e = pq(r.content,parser='html')
    except:
        return
    l = list(e('a').items())
    if 'intern' in r.content.lower() and r.content.lower().count('internal') + r.content.lower().count('international') + r.content.lower().count('internet') != r.content.lower().count('intern'):
        print "Intern at: " + r.url
        outputFile.write(r.url + "\n")
    for attribute in l:
        link = attribute.attr['href']
        if link is None or link == '':
            continue
        if '#' in link:
            continue
        if 'http' in link and origin not in link.split('/')[2]:
            continue
        if link == '/':
            continue
        if '.pdf' in link:
            continue
        if 'mailto' in link:
            continue
        if 'javascript:' in link:
            continue
        if 'twitter.com' in link or 'facebook.com' in link or 'linkedin.com' in link:
            continue
        if link[0] == '/':
            baseUrl = r.url.split('/')[0] + '//' + r.url.split('/')[2]
            if baseUrl == '/':
                fullLink = baseUrl + link[1:]
            else:
                fullLink = baseUrl + '/' + link[1:]
        elif 'http' in link:
            fullLink = link
        else:
            fullLink = findNewBase(r.url) + link
        
        if link not in linklist and 'facebook.com' not in fullLink and 'twitter.com' not in fullLink and 'linkedin.com' not in fullLink:
            if supercounter > 30:
                print 'too many tries'
                return
            print fullLink
            linklist.append(link)
            findJob(fullLink,linklist,origin)

inputFile = open('E:/output2.txt','r')
outputFile = open('E:/jobs.txt', 'w')
counter = 0
supercounter = 0
for line in inputFile:
    if counter < 255:
        counter = counter + 1
        continue
    print "Opening " + line
    try:
        parts = line.split('/')[-2].split('.')
        original = parts[-2] + '.' + parts[-1]
    except:
        print 'Failed to parse ' + line
    try:
        supercounter = 0
        findJob(line,[],original)
    except:
        print 'Error for some reason at ' + line
inputFile.close();
outputFile.close();
