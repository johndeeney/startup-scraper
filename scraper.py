import requests
from urlparse import urljoin
from pyquery import PyQuery as pq

def findNewBase(url):
    if '.' in url.split('/')[-1]:
        return url[:(-1 * len(url.split('/')[-1]))].rstrip('/') + '/'
    else:
        return url.rstrip('/') + '/'

def getNewLinkOld(url, link):
        if link[0] == '/':
            baseUrl = url.split('/')[0] + '//' + url.split('/')[2]
            if baseUrl == '/':
                fullLink = baseUrl + link[1:]
            else:
                fullLink = baseUrl + '/' + link[1:]
        elif 'http' in link:
            fullLink = link
        else:
            fullLink = findNewBase(url) + link
        return fullLink

def getNewLink(baseUrl, aTag):
    return urljoin(baseUrl, aTag)

def isValidLink(link,origin):
    if link is None or link == '':
        return False
    if '#' in link:
        return False
    if 'http' in link and origin.split('/')[2].split('.')[-2] not in link.split('/')[2]:
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
    return ('intern' in r.content.lower() and \
           r.content.lower().count('internal') + r.content.lower().count('international') + r.content.lower().count('internet') != r.content.lower().count('intern'))\
           or 'co-op' in r.content.lower()
           

def findJob(url,linklist,origin,depth):
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
        print "Failure to connect to " + url
    try:
        e = pq(r.content,parser='html')
    except:
        return
    l = list(e('a').items())
    if containsInternship(r):
        print "Intern at: " + r.url
        outputFile.write(r.url + "\n")
    if supercounter > 30:
        print str(supercounter) + " tries initiatied.  Switching to next website."
        return
    for attribute in l:
        if supercounter > 30:
            return
        link = attribute.attr['href']
        if not isValidLink(link, origin):
            continue
        fullLink = getNewLink(r.url, link)
        if fullLink not in linklist and 'facebook.com' not in fullLink and 'twitter.com' not in fullLink and 'linkedin.com' not in fullLink:
            print fullLink
            linklist.append(fullLink)
            findJob(fullLink,linklist,origin,depth + 1)

inputFile = open('E:/output2.txt','r')
outputFile = open('E:/jobs4.txt', 'w')
counter = 0
supercounter = 0
for line in inputFile:
    counter = counter + 1
    if counter < 5:
        continue
    print "Opening " + line
    original = line
    try:
        supercounter = 0
        findJob(line,[],original,1)
    except Exception as inst:
        print 'Error for some reason at ' + line
        print inst
    if counter % 1 == 0:
        print "reopening file..."
        outputFile.close()
        outputFile = open('E:/jobs4.txt', 'a')
inputFile.close();
outputFile.close();
