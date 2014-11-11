Codeforces Parser v1.4.1
=================

Summary
-------

[Codeforces](http://codeforces.com/) is a website for _competitive programming_. It holds contests, so-called **Codeforces Rounds**, about every week.

This is a python program that parses the sample tests from the contest problem pages. For each problem, it generates the sample input/output files and a shell script to run sample tests.

You can also find this article here, [http://codeforces.com/blog/entry/10416](http://codeforces.com/blog/entry/10416)

### Example:
`./parse.py contest_number (e.g. ./parse.py 464)`

Where `464` is the contest number, not the round number! Check the URL of the contest on your browser, that is the number you are supposed to use.

### Effect:

##### What will happen, for example, if `./parse.py 464` is executed?

1. Directories `464/A`, `464/B`, `464/C`, `464/D` and so on are created depending on the contest number of problems.
2. For each problem, `main.cc` is copied and renamed to the problem letter to the corresponding directory. **You can put the path of your usual template in `parse.py:20`**.
3. Problem page is downloaded from Codeforces website, and parsed. Sample input/output files are generated, e.g. `input1`, `output1`, `input2`, `output2` and so on. You can create your own test cases after that, just keep the same naming format as others test cases.
4. A script `test.sh` is generated. You can use it to compile and run the sample tests after you finish coding. Just run `./test.sh` in the problem directory.

##### What will happen if `./test.sh` is executed?

1. Compilation: `g++ -g -std=c++0x -Wall $DBG main.cc`. **You can change the compile options in `parse.py:21`**. Variable $DBG is set to -DDEBUG if you start "./test.sh -d", otherwise it is empty. This allows for compilation with and without debug macros.
2. Run each sample tests on your program (`a.out`), and check the output by `diff`. If it's correct, print **Accepted**, or else print the sample test that went wrong.

### Collaborators and Versions:

##### List of CodeForces Collaborators:
+ [johnathan79717](http://codeforces.com/profile/johnathan79717)
+ [brunoja](http://codeforces.com/profile/brunoja)
+ [Matthias Kauer (mini addition)]
If you have any suggestions and/or bugs drop a message!

##### Versions Changes:
+ **1.4.1:**
Minor fixes, such as typos, bugs and special characters handling.
+ **1.4:**
Changed how the parser gets the problems. During the competitions the page is slightly different.
Fixed some invalid character on input and output causing the script to crash.
Forcing a new line on the input/output if there is none.
Fixed some line number information in this README file.
+ **1.3:**
Some minor fixes and code organizing. Also fixed some typos.
Removed the _sample_ from default input and output files.
+ **1.2:**
Fixed some typos and constants. 
Fetching contest info, printing contest name and problem names. 
The contest may now have more or less than 5 problems, it will auto detect.
The script will now generate the template with the problem letter.
Fixed test cases fetching. The script was stopping for escaped html characters, such as '&lt'.
Fixed script to work with python 3.
+ **1.1:**
Cleaner generation of the test script, now it auto detects the test cases, making you able to create your own cases.
Echo color output, for accepted we get a green message, otherwise it is red.
Added the time measurement for running the test cases.
For the runtime error case, it now outputs the input case.
Created some constants, such as compile options. These user modifiable constants should be easily spotted at the first lines of the python script.
+ **1.0:** Initial Version.

##### Todo, Bugs & Troubleshootings:

+ In OS X it is necessary to install the `gnu-time` to measure time.
+ This parser currently works only on Unix OSes. If you want to add Windows/Other support let us know.
