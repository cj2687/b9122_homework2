from bs4 import BeautifulSoup
import urllib.request
import regex as re

#Q1)1)
seed = "https://www.federalreserve.gov/"
seed_url = "https://www.federalreserve.gov/newsevents/pressreleases.htm"

urls = [seed_url]    #queue of urls to crawl
seen = [seed_url]    #stack of urls seen so far
opened = []          #we keep track of seen urls so that we don't revisit them
qualified = []  #list of qualified URLs

maxNumUrl = 10; #set the maximum number of urls to visit

while len(urls) > 0 and len(qualified) < maxNumUrl:
    # DEQUEUE A URL FROM urls AND TRY TO OPEN AND READ IT
    try:
        curr_url=urls.pop(0)
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read().lower()  #use lower() to consider both lower and upper case versions of covid
        opened.append(curr_url)

    except Exception as ex:
        print("Unable to access= "+curr_url)
        print(ex)
        continue    #skip code below

    # IF URL OPENS, CHECK WHICH URLS THE PAGE CONTAINS
    # ADD THE URLS FOUND TO THE QUEUE url AND seen
    soup = BeautifulSoup(webpage, "lxml")  #creates object soup
    result = soup.body.find_all(string=re.compile('covid'))
    # print(result)

    # add url to qualified if "covid" is featured in the page
    if len(result) != 0:
        qualified.append(curr_url)

    for link in soup.find_all('a', attrs={'href': re.compile("^/newsevents/pressreleases")}):
        childUrl = link.get('href')
        newUrl = urllib.parse.urljoin(seed, childUrl)
        if newUrl not in seen:
            urls.append(newUrl)
            seen.append(newUrl)

print("Number of URLs seen = %d and qualified = %d" % (len(seen), len(qualified)))
print("List of qualified URLs:")

for qualified_url in qualified:
    print(qualified_url)
