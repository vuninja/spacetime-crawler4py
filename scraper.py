import re
from urllib.parse import urlparse, urldefrag
from bs4 import BeautifulSoup

stopwords = []

domains = ("ics.uci.edu", "cs.uci.edu", "informatics.uci.edu", "stat.uci.edu")

with open('stopwords.txt') as stopwords_file:
    for word in stopwords_file:
        stopwords.append(word)

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation requred.
    # We need to do things here
    # Check if response is good. Please check my knowledge as this was done at like 1 AM LOL
    if resp:
        if resp >= 300:
            return list()
        html_content = resp.raw_response.content

        soup = BeautifulSoup(page_content, 'lxml')
        tokenize(soup.get_text())
        links = soup.find_all('a')
        # [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
        #  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
        #  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
        
        # get just href

    return list()

def is_valid(url):
    try:
        url_defrag = urldefrag(url).url
        parsed = urlparse(url_defrag)

        if parsed.scheme not in set(["http", "https"]):
            return False

        #Seeing if the current url is in the list of allowed domains
        domain_allowed = False
        for domain in domains:
            if domain in parsed.netloc:
                domain_allowed = True
        #Checking separately as it includes specific path
        if "today.uci.edu/department/information_computer_sciences" in parsed.netloc + parsed.path:
            domain_allowed = True

        #avoiding not allowed urls
        if not domain_allowed:
            return False
        
        #avoid calendars 
        if re.match(r"^.*calendar.*$", parsed.path.lower()):
            return False
        if "wics.ics.uci.edu/events/" in url: #also a calendar
            return False

        #avoid too long url (set arbitrarily at 300 for now)
        if len(url) > 300:
            return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise


# Ethan's implementation from Assingment 1. Feel free to change
def tokenize(text):
    tokens = []
    if len(text) > 0:
        current_token = ""
        try:
            matches = re.findall('\w{2,}', text)
            tokens.extend(matches)
        except UnicodeDecodeError as UDE:
            print("Ran into decoding error.")
    return tokens