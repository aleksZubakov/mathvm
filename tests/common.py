#!/usr/bin/env python2.7

import collections
import glob
import optparse
import os
import re
import subprocess

def make_diff(expect_file, actual_data):
    pipe = subprocess.Popen(['/usr/bin/diff', '-u', '-b', expect_file, '-'],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    (out, err) = pipe.communicate(actual_data)
    return out

def kw_compare(str1, str2):
    def remove_comments(str):
        return re.sub(r'//.*?\n' , '', str)
    def split(str):
        return re.split(r'[^a-zA-Z0-9_]+', str)
    def counts(tokens):
        return collections.Counter(tokens)
    v1 = counts(split(remove_comments(str1)))
    v2 = counts(split(remove_comments(str2)))
    for kw in ['function', 'native', 'int', 'double', 'string', 'print', 'for', 'while']:
        if v1.get(kw, 0) != v2.get(kw, 0):
            return False
    return True

def read_file(name):
    with open(name, 'r') as f:
        return f.read()

def write_file(name, content):
    with open(name, 'w') as f:
        f.write(content)

def run_mvm(bin, impl, file):
    pipe = subprocess.Popen([bin, impl, file],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    (out, err) = pipe.communicate()
    if pipe.returncode != 0:
        raise Exception("Program exited with code %d" % (pipe.returncode))
    return out

def load_tests():
    parser = optparse.OptionParser()
    parser.add_option('-e', '--executable',
                      action='store',
                      type='string',
                      help='path to the executable')
    parser.add_option('-k', '--kind',
                      default='debug',
                      action='store',
                      type='string',
                      help='executable kind (debug or opt)')
    parser.add_option('-t', '--testdir',
                      default='./tests',
                      action='store',
                      type='string',
                      help='tests directory')
    (options, _) = parser.parse_args()

    if options.executable is None:
        options.executable = os.path.join('./build', options.kind, 'mvm')

    test_files = glob.glob(os.path.join(options.testdir, '*.mvm'))

    tests = []
    for t in test_files:
        m = re.search(r"([\w-]+)\.mvm", t)
        if m is None:
            continue
        t = m.group(1)
        tests.append((options.executable, options.testdir, t))

    return tests
