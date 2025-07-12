#!/usr/bin/python
from urllib.request import urlopen, Request
from html.parser import HTMLParser
from sys import argv
from subprocess import call
from functools import partial, wraps
import os
from pathlib import Path

import re
import html
import time
import argparse
import platform
import logging

###########################
# User modifiable constants
###########################
language_params = {
    "c++17": {
        "TEMPLATE": "main.cc",
        "DEBUG_FLAGS": "-DDEBUG",
        "COMPILE_CMD": "g++ -g -std=c++17 -Wall $DBG",
        "RUN_CMD": "./a.out",
    },
    "c++14": {
        "TEMPLATE": "main.cc",
        "DEBUG_FLAGS": "-DDEBUG",
        "COMPILE_CMD": "g++ -g -std=c++14 -Wall $DBG",
        "RUN_CMD": "./a.out",
    },
    "go": {
        "TEMPLATE": "main.go",
        "COMPILE_CMD": "go build $DBG -o a.out",
        "DEBUG_FLAGS": '''"-ldflags '-X=main.DEBUG=Y'"''',
        "RUN_CMD": "./a.out",
    },
    "kotlin": {
        "TEMPLATE": "main.kt",
        "COMPILE_CMD": "kotlinc -include-runtime -d out.jar",
        "DEBUG_FLAGS": "-d",
        "RUN_CMD": "java -jar out.jar $DBG",
    },
    "java": {
        "TEMPLATE": "Main.java",
        "DEBUG_FLAGS": "-DDEBUG=true",
        "COMPILE_CMD": "javac $DBG",
        "RUN_CMD": "java -DDEBUG=$DBG Main",
    },
    "rust": {
        "TEMPLATE": "main.rs",
        "DEBUG_FLAGS": "--cfg debug_assertions",
        "COMPILE_CMD": "rustc $DBG -o a.out",
        "RUN_CMD": "./a.out",
    },
}

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

SAMPLE_INPUT = "input"
SAMPLE_OUTPUT = "output"
MY_OUTPUT = "my_output"

# Do not modify these!
VERSION = (
    "CodeForces Parser v1.5.1: https://github.com/johnathan79717/codeforces-parser"
)
RED_F = "\033[31m"
GREEN_F = "\033[32m"
BOLD = "\033[1m"
NORM = "\033[0m"
if platform.system() == "Darwin":
    TIME_CMD = r'`which gtime` -o time.out -f "(%es)"'
else:
    TIME_CMD = r'`which time` -o time.out -f "(%es)"'
TIME_AP = r"`cat time.out`"


# Problems parser.
class CodeforcesProblemParser(HTMLParser):

    def __init__(self, folder):
        HTMLParser.__init__(self)
        self.folder = folder
        self.num_tests = 0
        self.testcase = None
        self.start_copy = False
        self.end_line = False

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            attr_dict = dict(attrs)
            if attr_dict.get("class") == "input":
                self.num_tests += 1
                if self.testcase:
                    self.testcase.close()
                self.testcase = open(
                    f"{self.folder}/{SAMPLE_INPUT}{self.num_tests}", "wb"
                )
            elif attr_dict.get("class") == "output":
                if self.testcase:
                    self.testcase.close()
                self.testcase = open(
                    f"{self.folder}/{SAMPLE_OUTPUT}{self.num_tests}", "wb"
                )
        elif tag == "pre":
            if self.testcase is not None:
                self.start_copy = True

    def handle_endtag(self, tag):
        if tag == "br":
            if self.start_copy:
                self.testcase.write("\n".encode("utf-8"))
                self.end_line = True
        if tag == "pre":
            if self.start_copy:
                if not self.end_line:
                    self.testcase.write("\n".encode("utf-8"))
                self.testcase.close()
                self.testcase = None
                self.start_copy = False

    def handle_entityref(self, name):
        if self.start_copy:
            self.testcase.write(html.unescape(("&%s;" % name)).encode("utf-8"))

    def handle_data(self, data):
        if self.start_copy:
            self.testcase.write(data.strip("\n").encode("utf-8"))
            self.end_line = False

    def __del__(self):
        if self.testcase:
            self.testcase.close()


# Contest parser.
class CodeforcesContestParser(HTMLParser):

    def __init__(self, contest):
        HTMLParser.__init__(self)
        self.contest = contest
        self.start_contest = False
        self.start_problem = False
        self.name = ""
        self.problem_name = ""
        self.problems = []
        self.problem_names = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        
        # More robust contest name detection
        if (tag == "a" and 
            self.name == "" and 
            attr_dict.get("href") == f"/contest/{self.contest}"):
            self.start_contest = True
            
        elif tag == "option":
            value = attr_dict.get("value", "")
            # Look for problem identifiers (A, B, C, etc.)
            if re.match(r'^[A-Z][0-9]?$', value):
                self.problems.append(value)
                self.start_problem = True

    def handle_endtag(self, tag):
        if tag == "a" and self.start_contest:
            self.start_contest = False
        elif self.start_problem:
            self.problem_names.append(self.problem_name)
            self.problem_name = ""
            self.start_problem = False

    def handle_data(self, data):
        if self.start_contest:
            self.name = data
        elif self.start_problem:
            self.problem_name += data


# Parses each problem page.
def parse_problem(folder, contest, problem):
    url = f"https://codeforces.com/contest/{contest}/problem/{problem}"
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=10) as response:
            html = response.read()
        parser = CodeforcesProblemParser(folder)
        parser.feed(html.decode("utf-8"))
        logger.info(f"Successfully parsed problem {problem}")
        return parser.num_tests
    except Exception as e:
        logger.error(f"Error parsing problem {problem}: {e}")
        return 0


# Parses the contest page.
def parse_contest(contest):
    url = f"https://codeforces.com/contest/{contest}"
    req = Request(url, headers=headers)
    try:
        html = urlopen(req).read()
        parser = CodeforcesContestParser(contest)
        parser.feed(html.decode("utf-8"))
        return parser
    except Exception as e:
        print(f"Error parsing contest {contest}: {e}")
        return None


# Generates the test script.
def generate_test_script(folder, language, num_tests, problem):
    param = language_params[language]

    with open(folder + "test.sh", "w") as test:
        test.write(
            (
                "#!/bin/bash\n"
                'DBG=""\n'
                'while getopts ":d" opt; do\n'
                "  case $opt in\n"
                "    d)\n"
                '      echo "-d was selected; compiling in DEBUG mode!" >&2\n'
                "      DBG=" + param["DEBUG_FLAGS"] + "\n"
                "      ;;\n"
                r"    \?)" + "\n"
                '      echo "Invalid option: -$OPTARG" >&2\n'
                "      ;;\n"
                "  esac\n"
                "done\n"
                "\n"
                "if ! " + param["COMPILE_CMD"] + " {0}.{1}; then\n"
                "    exit\n"
                "fi\n"
                "INPUT_NAME=" + SAMPLE_INPUT + "\n"
                "OUTPUT_NAME=" + SAMPLE_OUTPUT + "\n"
                "MY_NAME=" + MY_OUTPUT + "\n"
                "rm -R $MY_NAME* &>/dev/null\n"
            ).format(problem, param["TEMPLATE"].split(".")[1])
        )
        test.write(
            "for test_file in $INPUT_NAME*\n"
            "do\n"
            "    i=$((${{#INPUT_NAME}}))\n"
            "    test_case=${{test_file:$i}}\n"
            "    if ! {5} {run_cmd} < $INPUT_NAME$test_case > $MY_NAME$test_case; then\n"
            r"        echo {1}{4}Sample test \#$test_case: Runtime Error{2} {6}" + "\n"
            "        echo ========================================\n"
            r"        echo Sample Input \#$test_case" + "\n"
            "        cat $INPUT_NAME$test_case\n"
            "    else\n"
            "        if diff --brief --ignore-space-change --ignore-blank-lines $MY_NAME$test_case $OUTPUT_NAME$test_case; then\n"
            r"            echo {1}{3}Sample test \#$test_case: Accepted{2} {6}" + "\n"
            "        else\n"
            r"            echo {1}{4}Sample test \#$test_case: Wrong Answer{2} {6}" + "\n"
            "            echo ========================================\n"
            r"            echo Sample Input \#$test_case" + "\n"
            "            cat $INPUT_NAME$test_case\n"
            "            echo ========================================\n"
            r"            echo Sample Output \#$test_case" + "\n"
            "            cat $OUTPUT_NAME$test_case\n"
            "            echo ========================================\n"
            r"            echo My Output \#$test_case" + "\n"
            "            cat $MY_NAME$test_case\n"
            "            echo ========================================\n"
            "        fi\n"
            "    fi\n"
            "done\n".format(
                num_tests,
                BOLD,
                NORM,
                GREEN_F,
                RED_F,
                TIME_CMD,
                TIME_AP,
                run_cmd=param["RUN_CMD"],
            )
        )
    call(["chmod", "+x", folder + "test.sh"])


def main():
    print(VERSION)
    parser = argparse.ArgumentParser(description="Parse Codeforces contest problems")
    parser.add_argument(
        "--language",
        "-l",
        default="c++17",
        choices=list(language_params.keys()),
        help="The programming language you want to use"
    )
    parser.add_argument("contest", help="Contest number", type=int)
    args = parser.parse_args()

    contest = args.contest
    language = args.language

    # Validate contest number
    if contest <= 0:
        print("Contest number must be positive")
        return

    # Find contest and problems.
    print(f"Parsing contest {contest} for language {language}, please wait...")
    content = parse_contest(contest)
    if content is None:
        print("Failed to parse contest. Check if the contest number is correct.")
        return
    
    if not content.problems:
        print("No problems found in this contest.")
        return
        
    print(f"{BOLD}{GREEN_F}*** Round name: {content.name} ***{NORM}")
    print(f"Found {len(content.problems)} problems!")

    # Find problems and test cases.
    TEMPLATE = language_params[language]["TEMPLATE"]
    for index, problem in enumerate(content.problems):
        problem_name = content.problem_names[index] if index < len(content.problem_names) else "Unknown"
        print(f"Downloading Problem {problem}: {problem_name}...")
        
        folder = Path(f"{contest}-{language}") / problem
        folder.mkdir(parents=True, exist_ok=True)
        
        template_src = Path(TEMPLATE)
        template_dst = folder / f"{problem}.{TEMPLATE.split('.')[1]}"
        
        if template_src.exists() and not template_dst.exists():
            import shutil
            shutil.copy2(template_src, template_dst)
        
        num_tests = parse_problem(str(folder) + "/", contest, problem)
        print(f"{num_tests} sample test(s) found.")
        
        if num_tests > 0:
            generate_test_script(str(folder) + "/", language, num_tests, problem)
        print("=" * 40)
        time.sleep(1)

    print("Use ./test.sh to run sample tests in each directory.")


if __name__ == "__main__":
    logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
    logger = logging.getLogger(__name__)
    main()
