#!/bin/bash
pip install cpplint
cd Stack_AutoTest

srcfiles="main.cpp Stack.h Queue.h"
echo "Source files:" $srcfiles

# for some reason, GitHub Classroom environment does not use cpplint.cfg
# explcitly ignore some style checks
filters=-legal/copyright,-build/header_guard,-whitespace/braces,-runtime/explicit,\
-whitespace/newline,-whitespace/end_of_line,-whitespace/blank_line,\
-whitespace/indent,-whitespace/comments,-runtime/string,-whitespace/line_length,\
-whitespace/ending_newline,-readability/todo,-readability/braces

cpplint --filter=$filters $srcfiles