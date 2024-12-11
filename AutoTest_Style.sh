#!/bin/bash
#--------------------------------------------------------------------------
# File: AutoTest_Style.sh
# Programmer: Michelle Talley
# Copyright 2024 Michelle Talley University of Central Arkansas
#--------------------------------------------------------------------------
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <test_directory> <source_files...>"
    exit 1
fi

test_directory=$1
shift
srcfiles="$@"

red="\033[31m"
blue="\033[34m"
green="\033[32m"
reset="\033[0m"

printf "${green}[==========]${reset}\n"
printf "${green}[ STYLE    ] Checking ${srcfiles}${reset}\n"
printf "${green}[----------]${reset}\n"

pip install cpplint

cd "$test_directory"

# for some reason, GitHub Classroom environment does not use cpplint.cfg
# explcitly ignore some style checks
filters=-legal/copyright,-build/header_guard,\
-runtime/explicit,,-runtime/string,-runtime/references,\
-readability/todo,-readability/braces,\
-whitespace/newline,-whitespace/end_of_line,-whitespace/blank_line,\
-whitespace/indent,-whitespace/comments,-whitespace/line_length,\
-whitespace/ending_newline,-whitespace/braces

cpplint --filter=$filters $srcfiles
rc=$?

if [ $rc -ne 0 ]; then
  printf "${red}[==========]${reset}\n"
  printf "${red}[  FAILED  ] Coding style checks.${reset}\n"
  printf "${red}[==========]${reset}\n"
else
  printf "${green}[==========]${reset}\n"
  printf "${green}[  PASSED  ] Coding style checks${reset}\n"
  printf "${green}[==========]${reset}\n"
fi
exit $rc
