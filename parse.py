#!/usr/bin/python
from urllib2 import urlopen
from sys import argv
from HTMLParser import HTMLParser
from subprocess import call
 
# User modifiable constants:
COMPILE_CMD='g++ -g main.cc -std=c++0x'
TEMPLATE='main.cc'
SAMPLE_INPUT='sample_input'
SAMPLE_OUTPUT='sample_output'
MY_OUTPUT='my_output'

# Do not modify these!
VERSION='CodeForces Parser v1.1'
RED_F='\033[31m'
GREEN_F='\033[32m'
BOLD='\033[1m'
NORM='\033[0m'
TIME_CMD='/usr/bin/time -o time.out -f "(%es)"'
TIME_AP='`cat time.out`'
 
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
                    '%s/%s%d' % (self.folder, SAMPLE_INPUT, self.num_tests), 'w')
            elif attrs == [('class', 'output')]:
                self.testcase = open(
                    '%s/%s%d' % (self.folder, SAMPLE_OUTPUT, self.num_tests), 'w')
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
    url = 'http://codeforces.com/contest/%s/problem/%s' % (contest, problem)
    return urlopen(url).read()
 
def parse(folder, html):
    parser = CodeforcesParser(folder)
    parser.feed(html)
    return parser.num_tests
 
def generate_tests(folder, num_tests):
    with open(folder + 'test.sh', 'w') as test:
        test.write(
            '#!/bin/bash\n'
            'if ! '+COMPILE_CMD+'; then\n'
            '    exit\n'
            'fi\n'
            'INPUT_NAME='+SAMPLE_INPUT+'\n'
            'OUTPUT_NAME='+SAMPLE_OUTPUT+'\n'
            'MY_NAME='+MY_OUTPUT+'\n')
        test.write(
            'for test_file in $INPUT_NAME*\n'
            'do\n'
            '    i=$((${{#INPUT_NAME}}))\n'
            '    test_case=${{test_file:$i}}\n'
            '    rm -R $MY_NAME*\n'
            '    if ! /usr/bin/time -o time.out -f "(%es)" ./a.out < $INPUT_NAME$test_case > $MY_NAME$test_case; then\n'
            '        echo {1}{4}Sample test \#$test_case: Runtime Error{2} {6}\n'
            '        echo ========================================\n'
            '        echo Sample Input \#$test_case\n'
            '        cat $INPUT_NAME$test_case\n'
            '    else\n'
            '        if diff --brief $MY_NAME$test_case $OUTPUT_NAME$test_case; then\n'
            '            echo {1}{3}Sample test \#$test_case: Accepted{2} {6}\n'
            '        else\n'
            '            echo {1}{4}Sample test \#$test_case: Wrong Answer{2} {6}\n'
            '            echo ========================================\n'
            '            echo Sample Input \#$test_case\n'
            '            cat $INPUT_NAME$test_case\n'
            '            echo ========================================\n'
            '            echo Sample Output \#$test_case\n'
            '            cat $OUTPUT_NAME$test_case\n'
            '            echo ========================================\n'
            '            echo My Output \#$test_case\n'
            '            cat $MY_NAME$test_case\n'
            '            echo ========================================\n'
            '        fi\n'
            '    fi\n'
            'done\n'
            .format(num_tests, BOLD, NORM, GREEN_F, RED_F, TIME_CMD, TIME_AP))
    call(['chmod', '+x', folder + 'test.sh'])
 
def main():
    print VERSION
    if(len(argv) < 2):
        print('USAGE: ./parse.py 379')
        return
    contest = argv[1]
    for problem in ['A', 'B', 'C', 'D', 'E']:
        folder = '%s/%s/' % (contest, problem)
        # print 'Making directory', folder
        call(['mkdir', '-p', folder])
        # print 'Copying main.cc to %s/%s/' % (contest, problem)
        call(['cp', '-n', TEMPLATE, '%s/%s/' % (contest, problem)])
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
