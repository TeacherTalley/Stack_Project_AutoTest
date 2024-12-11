#!/bin/bash
#--------------------------------------------------------------------------
# File: AutoTest_setup.sh
# Programmer: Michelle Talley
# Copyright 2024 Michelle Talley University of Central Arkansas
#
# Note project specific file copies at the end of the script.
#--------------------------------------------------------------------------
if [ -n "$1" ]; then # if argument specified, use source from that directory
    basepath="$1"
    # Remove trailing slash if it exists
    basepath="${basepath%/}"
else
    basepath=".."
fi
# Check if additional source files are provided as arguments
if [ $# -gt 1 ]; then
    srcfiles="${@:2}"
    # Prepend basepath to each file in srcfiles
    srcfiles=$(echo $srcfiles | sed "s|[^ ]*|$basepath/&|g")
else
    srcfiles="$basepath/main.cpp $basepath/*.h"
fi

red="\033[31m"
blue="\033[34m"
green="\033[32m"
reset="\033[0m"

printf "${green}[==========]${reset}\n"
printf "${green}[ SETUP    ] Source directory: ${basepath}${reset}\n"
printf "${green}[          ] Source files: ${srcfiles}${reset}\n"
printf "${green}[          ] Copying files.${reset}\n"
printf "${green}[----------]${reset}\n"
cp $srcfiles .
rc=$?

printf "${green}[==========]${reset}\n"
printf "${green}[ COMPILE  ] Compiling program.${reset}\n"
printf "${green}[----------]${reset}\n"
if [ -d "build" ]; then
    rm -rf build
fi
cmake -S . -B build
cmake --build build
rc=$?
if [ $rc -ne 0 ]; then
    printf "${red}[==========]${reset}\n"
    printf "${red}[  FAILED  ] Compile failed. Grade penalty to be assessed.${reset}\n"
    # printf "${red}[          ] Grade = 0/100${reset}\n"
    printf "${red}[==========]${reset}\n"
else
    printf "${green}[==========]${reset}\n"
    printf "${green}[  PASSED  ] Compile successful.${reset}\n"
    printf "${green}[==========]${reset}\n"
fi

#--------------------------------------------------------------------------
# Project specific file copies
#    These are the test data files used by AutoTest
#--------------------------------------------------------------------------
echo "--- Copy data files from AutoTest source to build directory ---"
cp AutoTest_movie_history.txt build/movie_history.txt
cp AutoTest_movie_queue.txt build/movie_queue.txt
echo

exit $rc

