#!/usr/bin/python
from urllib2 import urlopen
from sys import argv
from HTMLParser import HTMLParser
from subprocess import call

class CodeforcesParser(HTMLParser):
    def __init__(self, folder):
        HTMLParser.__init__(self)
        self.folder = folder
        self.num_tests = 0
        self.testcase = None
        self.start_copy = False

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            if attrs == [('class', 'input')]:
                self.num_tests += 1
                self.testcase = open(
                    '%s/sample_input%d' % (self.folder, self.num_tests), 'w')
            elif attrs == [('class', 'output')]:
                self.testcase = open(
                    '%s/sample_output%d' % (self.folder, self.num_tests), 'w')
        elif tag == 'pre':
            if self.testcase != None:
                self.start_copy = True

    def handle_endtag(self, tag):
        if tag == 'br':
            if self.start_copy:
                self.testcase.write('\n')
        if tag == 'pre':
            if self.start_copy:
                self.testcase.close()
                self.testcase = None
                self.start_copy = False

    def handle_data(self, data):
        if self.start_copy:
            self.testcase.write(data)

def download(contest, problem):
    url = "http://codeforces.com/contest/%s/problem/%s" % (contest, problem)
    return urlopen(url).read()

def parse(folder, html):
    parser = CodeforcesParser(folder)
    parser.feed(html)
    return parser.num_tests

def generate_tests(folder, num_tests):
    with open(folder + 'test.sh', 'w') as test:
        test.write(
            '#!/bin/bash\n'
            'if ! g++ -g main.cc -std=c++11; then\n'
            '    exit\n'
            'fi\n')
        for num in xrange(1, num_tests + 1):
            test.write(
                'if ! ./a.out < sample_input{0} > my_output{0}; then\n'
                '    echo Sample test \#{0}: Runtime Error\n'
                'else\n'
                '    if diff --brief my_output{0} sample_output{0}; then\n'
                '        echo Sample test \#{0}: Accepted\n'
                '    else\n'
                '       echo ========================================\n'
                '       echo Sample Input \#{0}\n'
                '       cat sample_input{0}\n'
                '       echo ========================================\n'
                '       echo Sample Output \#{0}\n'
                '       cat sample_output{0}\n'
                '       echo ========================================\n'
                '       echo My Output \#{0}\n'
                '       cat my_output{0}\n'
                '       echo ========================================\n'
                '    fi\n'
                'fi\n'
                .format(num))
    call(['chmod', '+x', folder + 'test.sh'])

def main():
    if(len(argv) < 2):
        print("USAGE: ./parse.py 379")
        return
    contest = argv[1]
    for problem in ['A', 'B', 'C', 'D', 'E']:
        folder = '%s/%s/' % (contest, problem)
        # print 'Making directory', folder
        call(['mkdir', '-p', folder])
        # print 'Copying main.cc to %s/%s/' % (contest, problem)
        call(['cp', '-n', 'main.cc', '%s/%s/' % (contest, problem)])
        print 'Downloading Problem %s ...' % problem
        html = download(contest, problem)
        num_tests = parse(folder, html)
        print num_tests, 'sample test(s) found.'
        # print 'Generating sample tests ...'
        generate_tests(folder, num_tests)
        print '========================================'
    print 'Use ./test.sh to run sample tests in each directory.'

if __name__ == '__main__':
    main()