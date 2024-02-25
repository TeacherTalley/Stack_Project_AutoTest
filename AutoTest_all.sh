#!/bin/bash
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
./AutoTest_Style.sh
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
echo "--- Unit testing (single test at a time) ---"
./AutoTest_gtests --gtest_filter=StackTest.Empty
./AutoTest_gtests --gtest_filter=StackTest.Size
./AutoTest_gtests --gtest_filter=StackTest.Top
./AutoTest_gtests --gtest_filter=StackTest.TopEmptyStack
./AutoTest_gtests --gtest_filter=StackTest.Push
./AutoTest_gtests --gtest_filter=StackTest.Pop
./AutoTest_gtests --gtest_filter=StackTest.PopEmptyStack
./AutoTest_gtests --gtest_filter=StackTest.ToString
./AutoTest_gtests --gtest_filter=StackTest.Print
./AutoTest_gtests --gtest_filter=StackTest.CopyConstructor
./AutoTest_gtests --gtest_filter=StackTest.SaveRestore

./AutoTest_gtests --gtest_filter=QueueTest.Empty
./AutoTest_gtests --gtest_filter=QueueTest.Size
./AutoTest_gtests --gtest_filter=QueueTest.Front
./AutoTest_gtests --gtest_filter=QueueTest.FrontEmptyQueue
./AutoTest_gtests --gtest_filter=QueueTest.Enqueue
./AutoTest_gtests --gtest_filter=QueueTest.Dequeue
./AutoTest_gtests --gtest_filter=QueueTest.DequeueEmptyQueue
./AutoTest_gtests --gtest_filter=QueueTest.ToString
./AutoTest_gtests --gtest_filter=QueueTest.Print
./AutoTest_gtests --gtest_filter=QueueTest.CopyConstructor
./AutoTest_gtests --gtest_filter=QueueTest.SaveRestore

echo
cd ..
echo "#################### END: AutoTest Results   #####################"
echo
