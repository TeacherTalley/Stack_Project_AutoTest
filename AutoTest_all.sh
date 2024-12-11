#!/bin/bash
#--------------------------------------------------------------------------
# File: AutoTest_all.sh
# Programmer: Michelle Talley
# Copyright 2024 Michelle Talley University of Central Arkansas
#--------------------------------------------------------------------------
repo=Stack_Project_AutoTest
echo "#################### START: AutoTest Setup ##################################"
echo " To be consistent with the grading environment, assume we are starting out "
echo " in the source directory (i.e., the parent of the AutoTest directory)."
echo " You will get a cd error if you execute directly from the AutoTest directory."
echo "#############################################################################"
cd $repo
echo
echo "#################### START: AutoTest Results #####################"
echo "--- Checking code format (cpplint) ---"
./AutoTest_Style.sh $repo main.cpp Stack.h Queue.h
echo
echo "--- Test user commands individually ---"
# AutoTest_OutputTest.py assumes starting in the source directory
cd ..
./$repo/AutoTest_OutputTest.py -t test_exit
./$repo/AutoTest_OutputTest.py -t test_add 
./$repo/AutoTest_OutputTest.py -t test_watch
./$repo/AutoTest_OutputTest.py -t test_delete
./$repo/AutoTest_OutputTest.py -t test_history 
./$repo/AutoTest_OutputTest.py -t test_recent
./$repo/AutoTest_OutputTest.py -t test_queue
./$repo/AutoTest_OutputTest.py -t test_next
echo
echo "--- Switch to build directory for remaining tests ---"
cd $repo
cd build
# echo "--- Checking main output (diff) ---"
# ../AutoTest_OutputTest.sh
# echo
echo "--- Unit testing (googletest - all tests at once) ---"
ctest
echo
# GitHub Classroom auto-grading runs the following commands from the current
# directory of the project being tested.  To similate that here, we need to
# change to the project directory before running the tests.
#
cd ../..
echo "--- Unit testing (single test at a time) ---"
# Note: The following commands should be exactly the same as specified in classroom.yml
./Stack_Project_AutoTest/AutoTest_gtest.sh StackTest.Empty
./Stack_Project_AutoTest/AutoTest_gtest.sh StackTest.Size
./Stack_Project_AutoTest/AutoTest_gtest.sh StackTest.Top
./Stack_Project_AutoTest/AutoTest_gtest.sh StackTest.TopEmptyStack
./Stack_Project_AutoTest/AutoTest_gtest.sh StackTest.Push
./Stack_Project_AutoTest/AutoTest_gtest.sh StackTest.Pop
./Stack_Project_AutoTest/AutoTest_gtest.sh StackTest.PopEmptyStack
./Stack_Project_AutoTest/AutoTest_gtest.sh StackTest.ToString
./Stack_Project_AutoTest/AutoTest_gtest.sh StackTest.Print
./Stack_Project_AutoTest/AutoTest_gtest.sh StackTest.CopyConstructor
./Stack_Project_AutoTest/AutoTest_gtest.sh StackTest.SaveRestore

./Stack_Project_AutoTest/AutoTest_gtest.sh QueueTest.Empty
./Stack_Project_AutoTest/AutoTest_gtest.sh QueueTest.Size
./Stack_Project_AutoTest/AutoTest_gtest.sh QueueTest.Front
./Stack_Project_AutoTest/AutoTest_gtest.sh QueueTest.FrontEmptyQueue
./Stack_Project_AutoTest/AutoTest_gtest.sh QueueTest.Enqueue
./Stack_Project_AutoTest/AutoTest_gtest.sh QueueTest.Dequeue
./Stack_Project_AutoTest/AutoTest_gtest.sh QueueTest.DequeueEmptyQueue
./Stack_Project_AutoTest/AutoTest_gtest.sh QueueTest.ToString
./Stack_Project_AutoTest/AutoTest_gtest.sh QueueTest.Print
./Stack_Project_AutoTest/AutoTest_gtest.sh QueueTest.CopyConstructor
./Stack_Project_AutoTest/AutoTest_gtest.sh QueueTest.SaveRestore

echo
cd ..
echo "#################### END: AutoTest Results   #####################"
echo
