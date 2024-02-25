#!/bin/bash
echo Testing: $1
./Stack_Project_AutoTest/build/AutoTest_gtests --gtest_filter=$1
