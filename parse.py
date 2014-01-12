#!/usr/bin/python
import urllib2
import sys

def download(contestID, problemID):
  url = "http://codeforces.com/contest/%s/problem/%s" % (contestID, problemID)
  return urllib2.urlopen(url).read()

def main():
  if(len(sys.argv) < 3):
    print("USAGE: ./parse.py 379 B")
    return
  print(download(sys.argv[1], sys.argv[2]))

if __name__ == '__main__':
  main()