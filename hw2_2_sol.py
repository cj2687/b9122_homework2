from bs4 import BeautifulSoup
import urllib.request
import regex as re

#Q1)2)
seed = "https://www.sec.gov"
seed_url = "https://www.sec.gov/news/pressreleases"

urls = [seed_url]    #queue of urls to crawl
seen = [seed_url]    #stack of urls seen so far
opened = []          #we keep track of seen urls so that we don't revisit them
qualified = []  #list that contains urls of press releases that feature the word charges
text = ['x']  #list that contains text of press releases
spec = [] #list that contains text of qualified press releases
n = -1
maxNumUrl = 21; #set the maximum number of urls to visit

while len(urls) > 0 and len(qualified) < maxNumUrl:
    # DEQUEUE A URL FROM urls AND TRY TO OPEN AND READ IT
    try:
        curr_url=urls.pop(0)
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read().lower()  #use lower() to consider both lower and upper case versions of charges
        opened.append(curr_url)

    except Exception as ex:
        print("Unable to access= "+curr_url)
        print(ex)
        continue    #skip code below

    # IF URL OPENS, CHECK WHICH URLS THE PAGE CONTAINS
    # ADD THE URLS FOUND TO THE QUEUE url AND seen
    soup = BeautifulSoup(webpage, "lxml")  #creates object soup
    result = soup.body.find_all(string=re.compile('charges')) #find if the word "charges" is in the page

    n = n+1  # keep track of the number of press releases that have been read

    if len(result) != 0:
        qualified.append(curr_url)  # add url to qualified if charges is featured in the page
        spec.append(text[n])  #record text of qualified press release in the list spec


    # collect childUrls of the seed url, i.e. collect urls of press releases
    for link in soup.find_all('a', attrs={'href': re.compile("^/news/press-release")}):
        childUrl = link.get('href')
        title = link.text
        newUrl = urllib.parse.urljoin(seed, childUrl)

        if newUrl not in seen:
            urls.append(newUrl)
            seen.append(newUrl)
            text.append(title)

qualified.pop(0) #drop the first url since it is the seed url that contains the word "charges" but itself is not a press release
text.pop(0) #drop the first text that corresponds to the first url
spec.pop(0)

print("Number of URLs seen = %d and qualified = %d" % (len(seen), len(qualified)))
print()
print("The list of qualified URLs and corresponding phrases containing the word charges:")

for i in range(len(qualified)):
    print(qualified[i], spec[i])

