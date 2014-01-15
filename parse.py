#!/usr/bin/python
import urllib2
import sys
from HTMLParser import HTMLParser

class CodeforcesParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.numTests = 0
        self.file = None
        self.copying = False
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            if attrs == [('class', 'input')]:
                self.numTests += 1
                self.file = open('input%d' % self.numTests , 'w')
            elif attrs == [('class', 'output')]:
                self.file = open('output%d' % self.numTests , 'w')
        elif tag == 'pre':
            if self.file != None:
                self.copying = True
    def handle_endtag(self, tag):
        if tag == 'br':
            if self.copying:
                self.file.write('\n')
        if tag == 'pre':
            if self.copying:
                self.file.close()
                self.file = None
                self.copying = False
    def handle_data(self, data):
        if self.copying:
            self.file.write(data)

def download(contestID, problemID):
    url = "http://codeforces.com/contest/%s/problem/%s" % (contestID, problemID)
    return urllib2.urlopen(url).read()

def main():
    if(len(sys.argv) < 3):
        print("USAGE: ./parse.py 379 B")
        return
    html = download(sys.argv[1], sys.argv[2])
    parser = CodeforcesParser()
    parser.feed(html)

if __name__ == '__main__':
    main()