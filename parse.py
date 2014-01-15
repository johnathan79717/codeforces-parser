#!/usr/bin/python
from urllib2 import urlopen
from sys import argv
from HTMLParser import HTMLParser
from subprocess import call

class CodeforcesParser(HTMLParser):
    def __init__(self, folder):
        HTMLParser.__init__(self)
        self.num_tests = 0
        self.file = None
        self.copying = False
        self.folder = folder
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            if attrs == [('class', 'input')]:
                self.num_tests += 1
                self.file = open(
                    '%s/input%d' % (self.folder, self.num_tests), 'w')
            elif attrs == [('class', 'output')]:
                self.file = open(
                    '%s/output%d' % (self.folder, self.num_tests), 'w')
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

def download(contest, problem):
    url = "http://codeforces.com/contest/%s/problem/%s" % (contest, problem)
    return urlopen(url).read()

def parse(folder, html):
    parser = CodeforcesParser(folder)
    parser.feed(html)
    with open(folder + 'num_tests', 'w') as num_tests:
        num_tests.write(str(parser.num_tests))

def main():
    if(len(argv) < 2):
        print("USAGE: ./parse.py 379")
        return
    contest = argv[1]
    call(['mkdir', contest])
    call(['cd', contest])
    for problem in ['A', 'B', 'C', 'D', 'E']:
        folder = '%s/%s/' % (contest, problem)
        call(['mkdir', folder])
        html = download(contest, problem)
        parse(folder, html)

if __name__ == '__main__':
    main()