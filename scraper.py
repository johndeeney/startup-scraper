import requests
from urlparse import urljoin
from pyquery import PyQuery as pq

def findNewBase(url):
    if '.' in url.split('/')[-1]:
        return url[:(-1 * len(url.split('/')[-1]))].rstrip('/') + '/'
    else:
        return url.rstrip('/') + '/'

def getNewLink(r, link):
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
        return fullLink

def isValidLink(link,origin):
    if link is None or link == '':
        return False
    if '#' in link:
        return False
    if 'http' in link and origin not in link.split('/')[2]:
        return False
    if link == '/':
        return False
    if '.pdf' in link:
        return False
    if '.mp4' in link:
        return False
    if '.zip' in link:
        return False
    if 'mailto' in link:
        return False
    if 'javascript:' in link:
        return False
    if 'twitter.com' in link or 'facebook.com' in link or 'linkedin.com' in link:
        return False
    return True

def containsInternship(r):
    return 'intern' in r.content.lower() and r.content.lower().count('internal') + r.content.lower().count('international') + r.content.lower().count('internet') != r.content.lower().count('intern')

def findJob(url,linklist,origin):
    global outputFile
    global supercounter
    supercounter = supercounter + 1
    if '.mp4' in url:
        return
    if '.zip' in url:
        return
    try:
        r = requests.Session().get(url)
    except:
        print "!!!!!!FAILUIRE!!!!!!\n" + url + "\n!!!!!!FAILuRE!!!!!!\n"
    try:
        e = pq(r.content,parser='html')
    except:
        return
    l = list(e('a').items())
    if containsInternship(r):
        print "Intern at: " + r.url
        outputFile.write(r.url + "\n")
    for attribute in l:
        link = attribute.attr['href']
        if not isValidLink(link, origin):
            continue
        fullLink = getNewLink(r, link)
        if link not in linklist and 'facebook.com' not in fullLink and 'twitter.com' not in fullLink and 'linkedin.com' not in fullLink:
            if supercounter > 30:
                print 'too many tries'
                return
            print fullLink
            linklist.append(link)
            findJob(fullLink,linklist,origin)

inputFile = open('E:/output2.txt','r')
outputFile = open('E:/jobs4.txt', 'w')
counter = 0
supercounter = 0
for line in inputFile:
    if counter < 1201:
        counter = counter + 1
        continue
    print "Opening " + line
    original = line
    try:
        #parts = line.split('/')[-2].split('.')
        #original = parts[-2] + '.' + parts[-1]
        original = line
    except:
        print 'Failed to parse ' + line
    try:
        supercounter = 0
        findJob(line,[],original)
    except Exception as inst:
        print 'Error for some reason at ' + line
        print inst
inputFile.close();
outputFile.close();
