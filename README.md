Codeforces Parser
=================

Summary
-------

[Codeforces](http://codeforces.com/) is a website for _competitive programming_. It holds contests, so-called __Codeforces Rounds__, about every week.

The programs in this project is to generate sample tests for contestants automatically. Python 2 is needed.

### Example:
`./parse.py contest_number (e.g. ./parse.py 380)`

###Effect:

Create a directory named as the contest_number. Inside that directory,

- Create a directory for each of the five problems, namely A, B, C, D, and E.
- Copy code template main.cc into the directory.
- Download the problem page, and parse the sample tests.
- Generate sample inputs, sample outputs, and a shell script to run the tests.