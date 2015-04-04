import requests
from urlparse import urljoin
from pyquery import PyQuery as pq

def getNewLink(baseUrl, aTag):
    """Returns a new link based on the original URL and the href link contained in the <a> tag"""
    return urljoin(baseUrl, aTag)

def isValidLink(link,origin):
    """Returns True if the link might go somewhere we want to look (e.g. .mp4 files and .zips will be useless.
    Will not return True if it leads to an external website.
    """
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

def containsInternship(content):
    """Returns True, if the content contains any mention of intern or co-op, ignoring the words international and internet"""
    return ('intern' in content and \
           content.count('internal') + content.count('international') + content.count('internet') != content.count('intern'))\
           or 'co-op' in content
           

def findJob(url,linklist,origin,depth):
    """Finds and saves all links with content relating to internships to a text file"""
    global outputFile
    global supercounter
    supercounter = supercounter + 1
    try:
        r = requests.Session().get(url)
    except:
        print "Failure to connect to " + url
    try:
        e = pq(r.content,parser='html')
    except:
        return
    l = list(e('a').items())
    if containsInternship(r.content.lower()):
        print "Intern at: " + r.url
        with open('internships.txt','a') as outputFile:
            outputFile.write(r.url + '\n')
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
        if fullLink not in linklist and 'facebook.com' not in fullLink \
           and 'twitter.com' not in fullLink and 'linkedin.com' not in fullLink:
            print fullLink
            linklist.append(fullLink)
            findJob(fullLink,linklist,origin,depth + 1)

with open('startup_websites.txt','r') as inputFile:
    websites = inputFile.read().splitlines()
try:
    with open('visited_sites.txt','r') as visitedFile:
        visitedSites = visitedFile.read()
except:
    visitedSites = "" 
supercounter = 0 #global variable for determining if there has been too many tries on
for website in websites:                                                #this website
    if website in visitedSites:
        continue
    print "Opening " + website
    original = website
    try:
        supercounter = 0
        findJob(website,[],original,1)
    except Exception as inst:
        print 'Error for some reason at ' + website
        print inst
    with open('visited_sites.txt','a') as visitedFile:  #opens an closes every time
        visitedFile.write(website + '\n')       #in case program stops unexpectedly
