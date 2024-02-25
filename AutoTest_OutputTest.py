#!/usr/bin/env python
#--------------------------------------------------------------------------
# File: AutoTest_OutputTest.py
# Programmer: Michelle Talley
# Copyright 2024 Michelle Talley University of Central Arkansas
#--------------------------------------------------------------------------
import sys
import os
import subprocess
import shutil
import argparse
import re


#--------------------------------------------------------------------------
# list all test cases to be executed here - modify as needed
#--------------------------------------------------------------------------
TEST_CASES = ['test_exit',
              'test_add', 
              'test_watch', 
              'test_delete', 
              'test_history', 
              'test_recent', 
              'test_queue',
              'test_next']

#--------------------------------------------------------------------------
# Global variables - modify as needed
#--------------------------------------------------------------------------
PARENT_PROJECT = '../..'
PROJECT = 'Stack_Project_AutoTest'
BUILD = 'build'
TEST_DIR = os.path.join(PROJECT, BUILD)
EXECUTABLE = './main'
# DIFF = 'diff --ignore-case --ignore-blank-lines --side-by-side  --ignore-space-change  --suppress-common-lines --color=always'

DATA_DIR = '..'
AUTOTEST_MOVIE_QUEUE_FILE = 'AutoTest_movie_queue.txt'
AUTOTEST_MOVIE_HISTORY_FILE = 'AutoTest_movie_history.txt'
STUDENT_MOVIE_QUEUE_FILE = 'movie_queue.txt'
STUDENT_MOVIE_HISTORY_FILE = 'movie_history.txt'
TESTDATAFILES = [AUTOTEST_MOVIE_QUEUE_FILE, AUTOTEST_MOVIE_HISTORY_FILE]
DATAFILES = [STUDENT_MOVIE_QUEUE_FILE, STUDENT_MOVIE_HISTORY_FILE]

AUTOTEST_MAIN_MISSING_FILE = 'AutoTest_main_missing_file.txt'
STUDENT_MAIN_MISSING_FILE = 'test_main_missing_file.txt'

AUTOTEST_MAIN_OUTPUT_FILE = 'AutoTest_main_output.txt'
STUDENT_MAIN_OUTPUT_FILE = 'test_main_output.txt'

AUTOTEST_MOVIE_QUEUE_UPDATE_FILE = 'AutoTest_movie_queue_updated.txt'
STUDENT_MOVIE_QUEUE_UPDATE_FILE = 'movie_queue_updated.txt'

AUTOTEST_MOVIE_HISTORY_UPDATE_FILE = 'AutoTest_movie_history_updated.txt'
STUDENT_MOVIE_HISTORY_UPDATE_FILE = 'movie_history_updated.txt'

#--------------------------------------------------------------------------
# Program commands - modify as needed
#--------------------------------------------------------------------------
USER_COMMANDS = {'add': 'a', 
                 'watch': 'w', 
                 'delete': 'd', 
                 'history': 'h', 
                 'recent': 'r',
                 'queue': 'q',
                 'next': 'n',
                 'exit': 'x'
                }

ADD_MOVIE = 'Black Widow'



#--------------------------------------------------------------------------
# Helper functions
#--------------------------------------------------------------------------

def execute_command(cmd, args=None):
    """
    Executes a command and returns the return code.

    Args:
        cmd (str): The command to be executed.
        args (object): Optional arguments.

    Returns:
        int: The return code of the command execution.
    """
    rc = 0

    if not args:
        args.verbose = False
        args.debug = False

    if args.verbose:
        print(f'Executing: {cmd}')
    if not args.debug:
        rc = subprocess.call(cmd, shell=True)
    return rc

def file_print(file, args=None):
    """
    Prints the contents of a file.

    Args:
        file (str): The path of the file to be printed.
        args (optional): Additional arguments (not used in this function).

    Returns:
        None
    """
    with open(file, 'r') as f:
        filedata = f.read()
    print(filedata)
    return

def file_diff(file1, file2, diff_args=None, args=None):
    """
    Compare two files and return the difference.

    Args:
        file1 (str): Path to the first file.
        file2 (str): Path to the second file.
        diff_args (str, optional): Additional arguments for the diff command. Defaults to None.
        args (str, optional): Additional arguments for the execute_command function. Defaults to None.

    Returns:
        int: Return code of the execute_command function.
    """
    diffcmd = 'diff'
    if not diff_args:
        diff_args = '--ignore-case --ignore-blank-lines --side-by-side  --ignore-space-change  --suppress-common-lines --color=always'
    cmd = f'{diffcmd} {diff_args} {file1} {file2}'
    rc = execute_command(cmd, args)
    return rc

def file_contains_file(file, searchfile, args=None):
    """
    Check if a file contains another file.

    Args:
        file (str): The path to the file to be checked.
        searchfile (str): The path to the file to search for.
        args (argparse.Namespace, optional): Additional arguments. Defaults to None.

    Returns:
        int: 0 if the searchfile is found in the file, 1 otherwise.
    """
    if not args:
        args.verbose = False
        args.debug = False

    if args.verbose:
        print(f'Executing: Check file {file} contains file {searchfile}')

    with open(file, 'r') as f:
        filedata = f.read()
    with open(searchfile, 'r') as f:
        searchdata = f.read()
    if searchdata in filedata:
        return 0
    else:
        if args.verbose:
            print(f'ERROR: {searchfile} not found in {file}')
            print(f'\nExpected:\n{searchdata}')
            print(f'\nActual:\n{filedata}')
        return 1

def file_contains_string(file, searchstring, args=None):
    """
    Check if a file contains a specific string.

    Args:
        file (str): The path to the file to be checked.
        searchstring (str): The string to search for in the file.
        args (argparse.Namespace, optional): Additional arguments. Defaults to None.

    Returns:
        int: 0 if the searchstring is found in the file, 1 otherwise.
    """
    if not args:
        args.verbose = False
        args.debug = False

    if args.verbose:
        print(f'Executing: Check file {file} contains {searchstring}')

    with open(file, 'r') as f:
        filedata = f.read()
    if searchstring in filedata:
        return 0
    else:
        if args.verbose:
            print(f'ERROR: {searchstring} not found in {file}')
            print(f'\nExpected:\n{searchstring}')
            print(f'\nActual:\n{filedata}')
        return 1

def file_contains_regex(file, searchstring, args=None):
    """
    Check if a file contains a specific string using regular expression.

    Args:
        file (str): The path of the file to be checked.
        searchstring (str): The string to search for in the file.
        args (argparse.Namespace, optional): Additional arguments. Defaults to None.

    Returns:
        int: 0 if the searchstring is found in the file, 1 otherwise.
    """
    if not args:
        args.verbose = False
        args.debug = False

    if args.verbose:
        print(f'Executing: Check file {file} contains {searchstring}')

    with open(file, 'r') as f:
        filedata = f.read()
    if re.search(searchstring, filedata):
        return 0
    else:
        if args.verbose:
            print(f'ERROR: {searchstring} not found in {file}')
            print(f'\nExpected:\n{searchstring}')
            print(f'\nActual:\n{filedata}')
        return 1

import shutil

def file_copy(src, dest, args=None):
    """
    Copy a file from the source path to the destination path.

    Args:
        src (str): The path of the source file.
        dest (str): The path of the destination file.
        args (optional): Additional arguments (not used in this function).

    Returns:
        int: 0 if the file copy is successful, 1 otherwise.
    """
    try:
        shutil.copyfile(src, dest)
    except:
        print(f'ERROR: Unable to copy {src} to {dest}')
        return 1
    return 0

def file_exists(file, args=None):
    return os.path.exists(file)

def file_remove(file, args=None):
    if file_exists(file):
        os.remove(file)
    return

def copy_test_input_files():
    # make sure the data files exist; overwrite if necessary
    for file, testfile in zip(DATAFILES, TESTDATAFILES):
        rc = file_copy(os.path.join(DATA_DIR, testfile), file)
        if rc != 0:
            return rc
    return 0


#--------------------------------------------------------------------------
# Test functions - Add your test functions here
#
# setup(args) - function to execute before running tests
# cleanup(args) - function to execute after running tests
#--------------------------------------------------------------------------

def setup(args):
    """
    Set up the test environment by changing the current working directory to the test directory.

    Args:
        args (object): The command-line arguments.

    Returns:
        None
    """
    cwd = os.getcwd()
    if not cwd.endswith(TEST_DIR):
        try:
            os.chdir(TEST_DIR)
        except:
            print(f'ERROR: Unable to change directory to: {TEST_DIR}')
            sys.exit(1)
    if args.debug:
        print(f'\nsetup: Changed directory to: {os.getcwd()}')
    return


def cleanup(args):
    """
    Cleans up the current working directory by changing it to the parent project directory.

    Args:
        args: Command-line arguments.

    Returns:
        None
    """
    cwd = os.getcwd()
    if cwd.endswith(TEST_DIR):
        try:
            os.chdir(PARENT_PROJECT)
        except:
            print(f'ERROR: Unable to change directory to: {".."}')
            sys.exit(1)
    if args.debug:
        print(f'\ncleanup: Changed directory to: {os.getcwd()}')
    return


def test_missing_file(args):
    """
    Test case for checking if a file is missing.

    Args:
        args: Additional arguments for executing the command.

    Returns:
        int: Return code indicating the result of the test case.
    """
    # make sure the data files do NOT exist
    for file in DATAFILES:
        if os.path.exists(file):
            os.remove(file)

    # run the program
    cmd = f'{EXECUTABLE} > {STUDENT_MAIN_MISSING_FILE} 2>&1'
    rc = execute_command(cmd, args)

    autotest_file = os.path.join(DATA_DIR, AUTOTEST_MAIN_MISSING_FILE)

    if not file_exists(autotest_file):
        print(f'ERROR: {autotest_file} not found')
        return 1

    # check that the updated movie queue file contains the new movie
    rc = file_diff(autotest_file, STUDENT_MAIN_MISSING_FILE, args=args)
    return rc


def test_exit(args):
    """
    Test the 'exit' functionality of the program.

    Args:
        args: Additional arguments passed to the function.

    Returns:
        int: Return code indicating the success or failure of the test.
    """
    if (copy_test_input_files() != 0):
        return 1

    user_cmd = 'exit'

    # build the command sequence into a string
    test_cmd = f'{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w') as f:
        f.write(test_cmd)
    
    test_output_file = f'test_output_{user_cmd}.txt'

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)
    if rc != 0:
        if args.verbose:
            print(f'FAILED (rc={rc}): {cmd}')
        return rc
    
    return rc


def test_add(args):
    """
    Test the 'add' functionality of the program.

    Args:
        args: Additional arguments passed to the function.

    Returns:
        int: Return code indicating the success or failure of the test.
    """
    if (copy_test_input_files() != 0):
        return 1

    user_cmd = 'add'

    # build the command sequence into a string
    movie = ADD_MOVIE
    test_cmd = f'{USER_COMMANDS[user_cmd]}\n{movie}\n{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w') as f:
        f.write(test_cmd)
    
    test_output_file = f'test_output_{user_cmd}.txt'

    # identify the test output file using the user command
    
    # extract filename from STUDENT_MOVIE_QUEUE_FILE without file extension
    autotest_queue_file = f'{os.path.splitext(STUDENT_MOVIE_QUEUE_FILE)[0]}_{user_cmd}.txt'

    # make a copy of the movie queue file
    rc = file_copy(STUDENT_MOVIE_QUEUE_FILE, autotest_queue_file, args=args)
    if rc != 0:
        print(f'ERROR: {autotest_queue_file} not constructed')
        return rc

    # append the new movie to the test movie queue file
    with open(autotest_queue_file, 'a') as f:
        f.write(f'{movie}\n')

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)
    if rc != 0:
        if args.verbose:
            print(f'FAILED (rc={rc}): {cmd}')
        return rc
    
    if args.verbose:
        print(f'Checking {movie} is appended to {STUDENT_MOVIE_QUEUE_FILE}')

    # check that the updated movie queue file contains the new movie
    rc = file_diff(autotest_queue_file, 
                   STUDENT_MOVIE_QUEUE_UPDATE_FILE,
                   args=args)
    return rc


def test_watch(args):
    """
    Test the 'watch' functionality of the program.

    Args:
        args: Additional arguments passed to the function.

    Returns:
        int: Return code indicating the success or failure of the test.
    """
    if (copy_test_input_files() != 0):
        return 1

    user_cmd = 'watch'

    # build the command sequence into a string
    test_cmd = f'{USER_COMMANDS[user_cmd]}\n{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w') as f:
        f.write(test_cmd)
    
    test_output_file = f'test_output_{user_cmd}.txt'

    # identify the test output file using the user command
    
    # extract filename from STUDENT_MOVIE_QUEUE_FILE without file extension
    autotest_queue_file = f'{os.path.splitext(STUDENT_MOVIE_QUEUE_FILE)[0]}_{user_cmd}.txt'

    # make a copy of the movie queue file
    rc = file_copy(STUDENT_MOVIE_QUEUE_FILE, autotest_queue_file, args=args)
    if rc != 0:
        print(f'ERROR: {autotest_queue_file} not constructed')
        return rc

    # extract filename from STUDENT_MOVIE_HISTORY_FILE without file extension
    autotest_history_file = f'{os.path.splitext(STUDENT_MOVIE_HISTORY_FILE)[0]}_{user_cmd}.txt'

    # make a copy of the movie history file
    rc = file_copy(STUDENT_MOVIE_HISTORY_FILE, autotest_history_file, args=args)
    if rc != 0:
        print(f'ERROR: {autotest_history_file} not constructed')
        return rc
    
    # remove the first movie from the test movie queue file
    with open(autotest_queue_file, 'r') as f:
        lines = f.readlines()
    with open(autotest_queue_file, 'w') as f:
        f.writelines(lines[1:]) # remove the first movie

    # extract the first movie from the test movie queue file
    movie = lines[0].strip()

    # prepend the first movie to the test movie history file
    with open(autotest_history_file, 'r') as f:
        lines = f.readlines()
    with open(autotest_history_file, 'w') as f:
        f.write(movie + '\n') # prepend the first movie
        f.writelines(lines) 

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)
    if rc != 0:
        if args.verbose:
            print(f'FAILED (rc={rc}): {cmd}')
        return rc 

    # check that the updated movie queue file does not contain the first movie
    if args.verbose:
        print(f'Checking {movie} is not in {STUDENT_MOVIE_QUEUE_UPDATE_FILE}')

    rc = file_diff(autotest_queue_file, 
                   STUDENT_MOVIE_QUEUE_UPDATE_FILE,
                   args=args)
    if rc != 0:
        if args.verbose:
            print(f'ERROR: {movie} not removed from {STUDENT_MOVIE_QUEUE_UPDATE_FILE}')
        return rc 

    # check that the updated movie history file contains the first movie
    if args.verbose:
        print(f'Checking {movie} is in {STUDENT_MOVIE_HISTORY_UPDATE_FILE}')

    rc = file_diff(autotest_history_file, 
                   STUDENT_MOVIE_HISTORY_UPDATE_FILE,
                   args=args)
    if rc != 0:
        if args.verbose:
            print(f'ERROR: {movie} not added to {STUDENT_MOVIE_HISTORY_UPDATE_FILE}')
        return rc 

    return rc


def test_delete(args):
    """
    Test the 'delete' functionality of the program.

    Args:
        args: Additional arguments passed to the function.

    Returns:
        int: Return code indicating the success or failure of the test.
    """
    if (copy_test_input_files() != 0):
        return 1

    user_cmd = 'delete'

    # build the command sequence into a string
    test_cmd = f'{USER_COMMANDS[user_cmd]}\n{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w') as f:
        f.write(test_cmd)
    
    test_output_file = f'test_output_{user_cmd}.txt'

    # identify the test output file using the user command
    
    # extract filename from STUDENT_MOVIE_QUEUE_FILE without file extension
    autotest_queue_file = f'{os.path.splitext(STUDENT_MOVIE_QUEUE_FILE)[0]}_{user_cmd}.txt'

    # make a copy of the movie queue file
    rc = file_copy(STUDENT_MOVIE_QUEUE_FILE, autotest_queue_file, args=args)
    if rc != 0:
        print(f'ERROR: {autotest_queue_file} not constructed')
        return rc

    # extract filename from STUDENT_MOVIE_HISTORY_FILE without file extension
    autotest_history_file = f'{os.path.splitext(STUDENT_MOVIE_HISTORY_FILE)[0]}_{user_cmd}.txt'

    # make a copy of the movie history file
    rc = file_copy(STUDENT_MOVIE_HISTORY_FILE, autotest_history_file, args=args)
    if rc != 0:
        print(f'ERROR: {autotest_history_file} not constructed')
        return rc

    # remove the first movie from the test movie queue file
    with open(autotest_queue_file, 'r') as f:
        lines = f.readlines()
    with open(autotest_queue_file, 'w') as f:
        f.writelines(lines[1:]) # remove the first movie

    # extract the first movie from the test movie queue file
    movie = lines[0].strip()

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)
    if rc != 0:
        if args.verbose:
            print(f'FAILED (rc={rc}): {cmd}')
        return rc
    
    # check that the updated movie queue file does not contain the first movie
    if args.verbose:
        print(f'Checking {movie} is not in {STUDENT_MOVIE_QUEUE_UPDATE_FILE}')

    rc = file_diff(autotest_queue_file, 
                   STUDENT_MOVIE_QUEUE_UPDATE_FILE,
                   args=args)
    if rc != 0:
        if args.verbose:
            print(f'ERROR: {movie} not removed from {STUDENT_MOVIE_QUEUE_UPDATE_FILE}')
        return rc 
    
    # make sure the updated movie history file is the same as the original
    if args.verbose:
        print(f'Checking {movie} is not in {STUDENT_MOVIE_HISTORY_UPDATE_FILE}')

    rc = file_diff(autotest_history_file, 
                   STUDENT_MOVIE_HISTORY_UPDATE_FILE,
                   args=args)
    if rc != 0:
        if args.verbose:
            print(f'ERROR: {movie} present in {STUDENT_MOVIE_HISTORY_UPDATE_FILE}')
        return rc 
    
    return rc


def test_history(args):
    """
    Test the 'history' functionality of the program.

    Args:
        args: Additional arguments passed to the function.

    Returns:
        int: Return code indicating the success or failure of the test.
    """
    if (copy_test_input_files() != 0):
        return 1

    user_cmd = 'history'

    # build the command sequence into a string
    test_cmd = f'{USER_COMMANDS[user_cmd]}\n{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w') as f:
        f.write(test_cmd)
    
    test_output_file = f'test_output_{user_cmd}.txt'

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)
    if rc != 0:
        if args.verbose:
            print(f'FAILED (rc={rc}): {cmd}')
        return rc
    
    # check that the updated movie queue file does not contain the first movie
    if args.verbose:
        print(f'Checking if history is in {test_output_file}')

    rc = file_contains_file(test_output_file, STUDENT_MOVIE_HISTORY_FILE, args=args)
    return rc


def test_recent(args):
    """
    Test the 'recent' functionality of the program.

    Args:
        args: Additional arguments passed to the function.

    Returns:
        int: Return code indicating the success or failure of the test.
    """
    if (copy_test_input_files() != 0):
        return 1

    user_cmd = 'recent'

    # build the command sequence into a string
    test_cmd = f'{USER_COMMANDS[user_cmd]}\n{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w') as f:
        f.write(test_cmd)
    
    test_output_file = f'test_output_{user_cmd}.txt'

    # extract the first movie from the test movie history file
    with open(STUDENT_MOVIE_HISTORY_FILE, 'r') as f:
        lines = f.readlines()
    movie = lines[0].strip()

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)
    if rc != 0:
        if args.verbose:
            print(f'FAILED (rc={rc}): {cmd}')
        return rc
    
    # check that the updated movie queue file does not contain the first movie
    if args.verbose:
        print(f'Checking if {movie} is in {test_output_file}')

    rc = file_contains_string(test_output_file, movie, args=args)
    return rc


def test_queue(args):
    """
    Test the 'queue' functionality of the program.

    Args:
        args: Additional arguments passed to the function.

    Returns:
        int: Return code indicating the success or failure of the test.
    """
    if (copy_test_input_files() != 0):
        return 1

    user_cmd = 'queue'

    # build the command sequence into a string
    test_cmd = f'{USER_COMMANDS[user_cmd]}\n{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w') as f:
        f.write(test_cmd)
    
    test_output_file = f'test_output_{user_cmd}.txt'

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)
    if rc != 0:
        if args.verbose:
            print(f'FAILED (rc={rc}): {cmd}')
        return rc
    
    # check that the updated movie queue file does not contain the first movie
    if args.verbose:
        print(f'Checking if queue is in {test_output_file}')

    rc = file_contains_file(test_output_file, STUDENT_MOVIE_QUEUE_FILE, args=args)
    return rc


def test_next(args):
    """
    Test the 'next' functionality of the program.

    Args:
        args: Additional arguments passed to the function.

    Returns:
        int: Return code indicating the success or failure of the test.
    """
    if (copy_test_input_files() != 0):
        return 1

    user_cmd = 'next'

    # build the command sequence into a string
    test_cmd = f'{USER_COMMANDS[user_cmd]}\n{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w') as f:
        f.write(test_cmd)
    
    test_output_file = f'test_output_{user_cmd}.txt'

    # extract the first movie from the test movie queue file
    with open(STUDENT_MOVIE_QUEUE_FILE, 'r') as f:
        lines = f.readlines()
    movie = lines[0].strip()

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)
    if rc != 0:
        if args.verbose:
            print(f'FAILED (rc={rc}): {cmd}')
        return rc
    
    # check that the updated movie queue file does not contain the first movie
    if args.verbose:
        print(f'Checking if {movie} is in {test_output_file}')

    rc = file_contains_string(test_output_file, movie, args=args)
    return rc




#--------------------------------------------------------------------------
# Everything below this line is generic code to execute tests defined above
# Do not modify anything below this line
#--------------------------------------------------------------------------
def banner(msg, args):
    if args.verbose:
        print(f'\n{"-"*10} TEST: {msg} {"-"*40}\n')

def footer(msg, rc, args):
    if args.verbose:
        print(f'\n{"-"*10} END: {msg} rc: {rc} {"-"*35}\n') 

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", default=True, 
                        help="Enable verbose output")
    parser.add_argument("-q", "--quiet", action="store_true", default=False, 
                        help="Enable quiet mode")
    parser.add_argument("--nosetup", action="store_true", default=False, 
                        help="Disable setup before running tests")
    parser.add_argument("--nocleanup", action="store_true", default=False, 
                        help="Disable cleanup after running tests")
    parser.add_argument("--debug", action="store_true", default=False, 
                        help="Enable debug mode")
    parser.add_argument("-t", "--test", nargs='+', type=str, default=None, 
                        help=f"Specify the test(s) to run from: {TEST_CASES}")
    return parser.parse_args()

def test_main():
    args = parse_arguments()

    if args.quiet:
        args.verbose = False

    if not args.nosetup:
        # execute the setup function if it exists
        try:
            setup(args)
        except NameError:
            pass

    # if no test ID is provided, run all tests
    if not args.test:
        tests = TEST_CASES
    else:
        tests = args.test

    if args.verbose:
        print(f"\nRunning tests: {tests}...\n")
    for test in tests:
        banner(test, args)
        try:
            rc = globals()[test](args)
        except NameError:
            print(f"ERROR: Test function {test} not found.")
            rc = 0
        footer(test, rc, args)

    if not args.nocleanup:
        # execute the cleanup function if it exists
        try:
            cleanup(args)
        except NameError:
            pass

    sys.exit(rc)

def main():
    test_main()

if __name__ == "__main__":
    main()
