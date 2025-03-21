#!/usr/bin/env python
"""
AutoTest_OutputTest.py

This module contains automated tests for the Stack Project. It includes functions
to set up the test environment, execute various test cases, and clean up after tests.
The tests cover functionalities such as adding, watching, deleting, and querying movies
in a movie queue system.

Author: Michelle Talley
Copyright 2024 Michelle Talley University of Central Arkansas
"""
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
#--------------------------------------------------------------------------
# Font colors for terminal output
#--------------------------------------------------------------------------
BLUE = '\033[34m'
RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'

def report_failure(msg):
    """
    Prints a failure message in red font.
    Parameters:
         msg (str): The message to print.
    Returns:
         None
    """
    print(f'{RED}[----------]{RESET}')
    print(f'{RED}[  FAILED  ] {msg}{RESET}')
    print(f'{RED}[----------]{RESET}')
    return

def report_success(msg):
    """
    Prints a success message in green font.
    Parameters:
         msg (str): The message to print.
    Returns:
         None
    """
    print(f'{GREEN}[----------]{RESET}')
    print(f'{GREEN}[  PASSED  ] {msg}{RESET}')
    print(f'{GREEN}[----------]{RESET}')
    return

def report_info(msg, color=RESET):
    """
    Prints an informational message in the specified font color.
    Parameters:
         msg (str): The message to print.
         color (str): The font color to use. Defaults to GREEN.
    Returns:
         None
    """
    print(f'{color}{msg}{RESET}')
    return


def execute_command(cmd, args=None, accept_rc=None):
    """
    Executes a shell command and provides verbose and debug output based upon
    the given arguments.

    Parameters:
         cmd (str): The shell command to execute.
         args (object, optional): An object containing verbose and debug flags.
            Defaults to None.
         accept_rc (list, optional): A list of acceptable return codes.
            Defaults to [0].
    Returns:
         int: The return code of the executed command.
    Behavior:
    - If `args.verbose` is True, prints the command execution details.
    - If `args.debug` is False, executes the command using `subprocess.call`.
    - If `args.verbose` is True, prints the result of the command execution,
        including specific messages for segmentation faults (rc=139)
        and uncaught exceptions (rc=134).
    """
    rc = 0

    if accept_rc is None:
        accept_rc = [0]

    if not args:
        args.verbose = False
        args.debug = False

    if args.verbose:
        print(f'{GREEN}[==========]{RESET}')
        print(f'{GREEN}[ EXECUTE  ] {cmd}{RESET}')
        print(f'{GREEN}[==========]{RESET}')

    if not args.debug:
        rc = subprocess.call(cmd, shell=True)

    if args.verbose:
        if rc == 139:
            report_failure('Segmentation Fault')
        elif rc == 134:
            report_failure('Uncaught Exception')
        elif rc not in accept_rc:
            report_failure(f'rc = {rc}')
        else:
            report_success(f'rc = {rc}')
    return rc


def file_print(file):
    """
    Prints the contents of a file.

    Args:
        file (str): The path of the file to be printed.

    Returns:
        None
    """
    with open(file, 'r', encoding='utf-8') as f:
        filedata = f.read()
    print(filedata)
    return


def file_diff(file1, file2, diff_args=None, args=None):
    """
    Compare two files and return the difference.

    Args:
        file1 (str): Path to the first file.
        file2 (str): Path to the second file.
        diff_args (str, optional): Additional arguments for the diff command.
            Defaults to None.
        args (str, optional): Additional arguments for the execute_command function.
            Defaults to None.

    Returns:
        int: Return code of the execute_command function.
    """
    diffcmd = 'diff'
    if not diff_args:
        diff_args = '--ignore-case --ignore-blank-lines --side-by-side ' \
                    '--ignore-space-change --color=always'
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

#    if args.verbose:
#        report_info(f'Check file {file} contains file {searchfile}')

    with open(file, 'r', encoding='utf-8') as f:
        filedata = f.read()
    with open(searchfile, 'r', encoding='utf-8') as f:
        searchdata = f.read()
    if searchdata in filedata:
        if args.verbose:
            report_success(f'{searchfile} found in {file}')
        return 0
    else:
        if args.verbose:
            report_failure(f'{searchfile} not found in {file}')
            report_info(f'\nExpected:\n{searchdata}')
            report_info(f'\nActual:\n{filedata}')
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

#    if args.verbose:
#        report_info(f'Check file {file} contains "{searchstring}"')

    with open(file, 'r', encoding='utf-8') as f:
        filedata = f.read()
    if searchstring in filedata:
        if args.verbose:
            report_success(f'{searchstring} found in {file}')
        return 0
    else:
        if args.verbose:
            report_failure(f'"{searchstring}" not found in {file}')
            report_info(f'\nExpected:\n{searchstring}')
            report_info(f'\nActual:\n{filedata}')
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

#    if args.verbose:
#        report_info(f'Check file {file} contains regex "{searchstring}"')

    with open(file, 'r', encoding='utf-8') as f:
        filedata = f.read()
    if re.search(searchstring, filedata):
        if args.verbose:
            report_success(f'Regex "{searchstring}" found in {file}')
        return 0
    else:
        if args.verbose:
            report_failure(f'Regex "{searchstring}" not found in {file}')
            report_info(f'\nExpected:\nRegex {searchstring}')
            report_info(f'\nActual:\n{filedata}')
        return 1


def file_copy(src, dest):
    """
    Copy a file from the source path to the destination path.

    Args:
        src (str): The path of the source file.
        dest (str): The path of the destination file.

    Returns:
        int: 0 if the file copy is successful, 1 otherwise.
    """
    try:
        shutil.copyfile(src, dest)
    except shutil.Error as err:
        report_failure(f'Unable to copy {src} to {dest}: {err}')
        return 1
    return 0


def file_exists(file):
    """
    Check if a file exists at the given path.

    Args:
        file (str): The path to the file.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists(file)


def file_remove(file):
    """
    Remove a file if it exists at the given path.

    Args:
        file (str): The path to the file.

    Returns:
        None
    """
    if file_exists(file):
        os.remove(file)
    return

def copy_test_input_files():
    """
    Copy test input files from the data directory to the current directory.

    Returns:
        int: 0 if the files are copied successfully, 1 otherwise.
    """
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
        except OSError as err:
            report_failure(f'Unable to change directory to: {TEST_DIR}. Exception: {err}')
            sys.exit(1)
    if args.debug:
        report_info(f'\nsetup: Changed directory to: {os.getcwd()}')
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
        except OSError as err:
            report_failure(
                f'Unable to change directory to: {TEST_DIR}. Exception: {err}')
            sys.exit(1)
    if args.debug:
        report_info(f'\ncleanup: Changed directory to: {os.getcwd()}')
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
        report_failure(f'{autotest_file} not found')
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
    if copy_test_input_files() != 0:
        report_failure('Unable to copy test input files')
        return 1

    user_cmd = 'exit'

    # build the command sequence into a string
    test_cmd = f'{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(test_cmd)

    test_output_file = f'test_output_{user_cmd}.txt'

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)

    return rc


def test_add(args):
    """
    Test the 'add' functionality of the program.

    Args:
        args: Additional arguments passed to the function.

    Returns:
        int: Return code indicating the success or failure of the test.
    """
    if copy_test_input_files() != 0:
        report_failure('Unable to copy test input files')
        return 1

    user_cmd = 'add'

    # build the command sequence into a string
    movie = ADD_MOVIE
    test_cmd = f'{USER_COMMANDS[user_cmd]}\n{movie}\n{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(test_cmd)

    test_output_file = f'test_output_{user_cmd}.txt'

    # identify the test output file using the user command

    # extract filename from STUDENT_MOVIE_QUEUE_FILE without file extension
    autotest_queue_file = f'{os.path.splitext(STUDENT_MOVIE_QUEUE_FILE)[0]}_{user_cmd}.txt'

    # make a copy of the movie queue file
    rc = file_copy(STUDENT_MOVIE_QUEUE_FILE, autotest_queue_file)
    if rc != 0:
        report_failure(f'{autotest_queue_file} not constructed')
        return rc

    # append the new movie to the test movie queue file
    with open(autotest_queue_file, 'a', encoding='utf-8') as f:
        f.write(f'{movie}\n')

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)
    if rc != 0:
        return rc

    if args.verbose:
        report_info(f'Checking {movie} is appended to {STUDENT_MOVIE_QUEUE_FILE}')

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
    if copy_test_input_files() != 0:
        report_failure('Unable to copy test input files')
        return 1

    user_cmd = 'watch'

    # build the command sequence into a string
    test_cmd = f'{USER_COMMANDS[user_cmd]}\n{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(test_cmd)

    test_output_file = f'test_output_{user_cmd}.txt'

    # identify the test output file using the user command

    # extract filename from STUDENT_MOVIE_QUEUE_FILE without file extension
    autotest_queue_file = f'{os.path.splitext(STUDENT_MOVIE_QUEUE_FILE)[0]}_{user_cmd}.txt'

    # make a copy of the movie queue file
    rc = file_copy(STUDENT_MOVIE_QUEUE_FILE, autotest_queue_file)
    if rc != 0:
        report_failure(f'{autotest_queue_file} not constructed')
        return rc

    # extract filename from STUDENT_MOVIE_HISTORY_FILE without file extension
    autotest_history_file = f'{os.path.splitext(STUDENT_MOVIE_HISTORY_FILE)[0]}_{user_cmd}.txt'

    # make a copy of the movie history file
    rc = file_copy(STUDENT_MOVIE_HISTORY_FILE, autotest_history_file)
    if rc != 0:
        report_failure(f'{autotest_history_file} not constructed')
        return rc

    # remove the first movie from the test movie queue file
    with open(autotest_queue_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    with open(autotest_queue_file, 'w', encoding='utf-8') as f:
        f.writelines(lines[1:]) # remove the first movie

    # extract the first movie from the test movie queue file
    movie = lines[0].strip()

    # prepend the first movie to the test movie history file
    with open(autotest_history_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    with open(autotest_history_file, 'w', encoding='utf-8') as f:
        f.write(movie + '\n') # prepend the first movie
        f.writelines(lines)

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)
    if rc != 0:
        return rc

    # check that the updated movie queue file does not contain the first movie
    if args.verbose:
        report_info(f'Checking {movie} is not in {STUDENT_MOVIE_QUEUE_UPDATE_FILE}')

    rc = file_diff(autotest_queue_file,
                   STUDENT_MOVIE_QUEUE_UPDATE_FILE,
                   args=args)
    if rc != 0:
        report_failure(f'{movie} not removed from {STUDENT_MOVIE_QUEUE_UPDATE_FILE}')
        return rc

    # check that the updated movie history file contains the first movie
    if args.verbose:
        report_info(f'Checking {movie} is in {STUDENT_MOVIE_HISTORY_UPDATE_FILE}')

    rc = file_diff(autotest_history_file,
                   STUDENT_MOVIE_HISTORY_UPDATE_FILE,
                   args=args)
    if rc != 0:
        report_failure(f'{movie} not added to {STUDENT_MOVIE_HISTORY_UPDATE_FILE}')
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
    if copy_test_input_files() != 0:
        report_failure('Unable to copy test input files')
        return 1

    user_cmd = 'delete'

    # build the command sequence into a string
    test_cmd = f'{USER_COMMANDS[user_cmd]}\n{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(test_cmd)

    test_output_file = f'test_output_{user_cmd}.txt'

    # identify the test output file using the user command

    # extract filename from STUDENT_MOVIE_QUEUE_FILE without file extension
    autotest_queue_file = f'{os.path.splitext(STUDENT_MOVIE_QUEUE_FILE)[0]}_{user_cmd}.txt'

    # make a copy of the movie queue file
    rc = file_copy(STUDENT_MOVIE_QUEUE_FILE, autotest_queue_file)
    if rc != 0:
        report_failure(f'{autotest_queue_file} not constructed')
        return rc

    # extract filename from STUDENT_MOVIE_HISTORY_FILE without file extension
    autotest_history_file = f'{os.path.splitext(STUDENT_MOVIE_HISTORY_FILE)[0]}_{user_cmd}.txt'

    # make a copy of the movie history file
    rc = file_copy(STUDENT_MOVIE_HISTORY_FILE, autotest_history_file)
    if rc != 0:
        report_failure(f'{autotest_history_file} not constructed')
        return rc

    # remove the first movie from the test movie queue file
    with open(autotest_queue_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    with open(autotest_queue_file, 'w', encoding='utf-8') as f:
        f.writelines(lines[1:]) # remove the first movie

    # extract the first movie from the test movie queue file
    movie = lines[0].strip()

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)
    if rc != 0:
        return rc

    # check that the updated movie queue file does not contain the first movie
    if args.verbose:
        report_info(f'Checking {movie} is not in {STUDENT_MOVIE_QUEUE_UPDATE_FILE}')

    rc = file_diff(autotest_queue_file,
                   STUDENT_MOVIE_QUEUE_UPDATE_FILE,
                   args=args)
    if rc != 0:
        report_failure(f'{movie} not removed from {STUDENT_MOVIE_QUEUE_UPDATE_FILE}')
        return rc

    # make sure the updated movie history file is the same as the original
    if args.verbose:
        report_info(f'Checking {movie} is not in {STUDENT_MOVIE_HISTORY_UPDATE_FILE}')

    rc = file_diff(autotest_history_file,
                   STUDENT_MOVIE_HISTORY_UPDATE_FILE,
                   args=args)
    if rc != 0:
        report_failure(f'{movie} present in {STUDENT_MOVIE_HISTORY_UPDATE_FILE}')
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
    if copy_test_input_files() != 0:
        report_failure('Unable to copy test input files')
        return 1

    user_cmd = 'history'

    # build the command sequence into a string
    test_cmd = f'{USER_COMMANDS[user_cmd]}\n{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(test_cmd)

    test_output_file = f'test_output_{user_cmd}.txt'

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)
    if rc != 0:
        return rc

    # check that the updated movie queue file does not contain the first movie
    if args.verbose:
        report_info(f'Checking if history is in {test_output_file}')

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
    if copy_test_input_files() != 0:
        report_failure('Unable to copy test input files')
        return 1

    user_cmd = 'recent'

    # build the command sequence into a string
    test_cmd = f'{USER_COMMANDS[user_cmd]}\n{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(test_cmd)

    test_output_file = f'test_output_{user_cmd}.txt'

    # extract the first movie from the test movie history file
    with open(STUDENT_MOVIE_HISTORY_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    movie = lines[0].strip()

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)
    if rc != 0:
        return rc

    # check that the updated movie queue file does not contain the first movie
    if args.verbose:
        report_info(f'Checking if {movie} is in {test_output_file}')

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
    if copy_test_input_files() != 0:
        report_failure('Unable to copy test input files')
        return 1

    user_cmd = 'queue'

    # build the command sequence into a string
    test_cmd = f'{USER_COMMANDS[user_cmd]}\n{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(test_cmd)

    test_output_file = f'test_output_{user_cmd}.txt'

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)
    if rc != 0:
        return rc

    # check that the updated movie queue file does not contain the first movie
    if args.verbose:
        report_info(f'Checking if queue is in {test_output_file}')

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
    if copy_test_input_files() != 0:
        report_failure('Unable to copy test input files')
        return 1

    user_cmd = 'next'

    # build the command sequence into a string
    test_cmd = f'{USER_COMMANDS[user_cmd]}\n{USER_COMMANDS["exit"]}\n'
    input_file = f'test_input_{user_cmd}.txt'
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(test_cmd)

    test_output_file = f'test_output_{user_cmd}.txt'

    # extract the first movie from the test movie queue file
    with open(STUDENT_MOVIE_QUEUE_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    movie = lines[0].strip()

    # run the program
    cmd = f'{EXECUTABLE} < {input_file} > {test_output_file} 2>&1'
    rc = execute_command(cmd, args)
    if rc != 0:
        return rc

    # check that the updated movie queue file does not contain the first movie
    if args.verbose:
        report_info(f'Checking if {movie} is in {test_output_file}')

    rc = file_contains_string(test_output_file, movie, args=args)
    return rc




#--------------------------------------------------------------------------
# Everything below this line is generic code to execute tests defined above
# Do not modify anything below this line
#--------------------------------------------------------------------------
def banner(msg, args):
    """
    Print a banner message for the test.

    Args:
        msg (str): The message to print.
        args (argparse.Namespace): The command-line arguments.

    Returns:
        None
    """
    if args.verbose:
        print(f'{BLUE}[==========]{RESET}')
        print(f'{BLUE}[   TEST   ] {msg}{RESET}')
        print(f'{BLUE}[==========]{RESET}')

def footer(msg, rc, args):
    """
    Print a footer message for the test.

    Args:
        msg (str): The message to print.
        rc (int): The return code of the test.
        args (argparse.Namespace): The command-line arguments.

    Returns:
        None
    """
    if args.verbose:
        print(f'{BLUE}[==========]{RESET}')
        print(f'{BLUE}[   END    ] {msg} rc: {rc}{RESET}')
        print(f'{BLUE}[==========]{RESET}')

def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: The parsed command-line arguments.
    """
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
    """
    Main function to execute the tests.

    Returns:
        None
    """
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

    for test in tests:
        banner(test, args)
        try:
            rc = globals()[test](args)
        except NameError:
            report_failure(f'Test function {test} not found.')
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
    """
    Main entry point of the script.

    Returns:
        None
    """
    test_main()

if __name__ == "__main__":
    main()
