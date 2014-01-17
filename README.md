Codeforces Parser v1.1
=================

Summary
-------

[Codeforces](http://codeforces.com/) is a website for _competitive programming_. It holds contests, so-called **Codeforces Rounds**, about every week.

This is a python program that parses the sample tests from the contest problem pages. For each problem, it generates the sample input/output files and a shell script to run sample tests.

You can also find this article here, [http://codeforces.com/blog/entry/10416](http://codeforces.com/blog/entry/10416)

### Example:
`./parse.py contest_number (e.g. ./parse.py 380)`

### Effect:

##### What will happen, for example, if `./parse.py 380` is executed?

1. Directories `380/A`, `380/B`, `380/C`, `380/D`, and `380/E` are created.
2. For each problem, `main.cc` is copied to the corresponding directory. **You can put the path of your usual template in `parse.py:9`**.
3. Problem page is downloaded from Codeforces website, and parsed. Sample input/output files are generated, e.g. `sample_input1`, `sample_output1`, `sample_input2`, `sample_output2`, etc.
4. A script `test.sh` is generated. You can use it to compile and run the sample tests after you finish coding. Just run `./test.sh` in the problem directory.

##### What will happen if `./test.sh` is executed?

1. Compilation: `g++ -g main.cc -std=c++0x`. **You can change the compile options in `parse.py:8`**.
2. Run each sample tests on your program (`a.out`), and check the output by `diff`. If it's correct, print **Accepted**, or else print the sample test that went wrong.

### Collaborators and Versions:

##### List of CodeForces Collaborators:
+ [johnathan79717](http://codeforces.com/profile/johnathan79717)
+ [brunoja](http://codeforces.com/profile/brunoja)

##### Versions Changes
+ **1.0:** Initial Version.
+ **1.1:**
        ++ Cleaner generation of the test script, now it auto detects the test cases, making you able to create your own cases.
        ++ Echo color output, for accepted we get a green message, otherwise it is red.
        ++ Added the time measurement for running the test cases.
        ++ For the runtime error case, it now outputs the input case.
        ++ Created some constants, such as compile options. These user modifiable constants should be easily spotted at the first lines of the python script.
        
