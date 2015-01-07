#!/usr/bin/env python

# Nicolas Seriot
# 2011-05-09 - 2013-02-21
# https://github.com/nst/objc_strings/

"""
Goal: helps Cocoa applications localization by detecting unused and missing keys in '.strings' files

Input: path of an Objective-C project

Output:
    1) warnings for untranslated strings in *.m
    2) warnings for unused keys in Localization.strings
    3) errors for keys defined twice or more in the same .strings file

Typical usage: $ python objc_strings.py /path/to/obj_c/project

Xcode integration:
    1. make `objc_strings.py` executable
        $ chmod +x objc_strings.py
    2. copy `objc_strings.py` to the root of your project
    3. add a "Run Script" build phase to your target
    4. move this build phase in second position
    5. set the script path to `${SOURCE_ROOT}/objc_strings.py`
"""

import sys
import os
import re
import codecs
import optparse

def warning(file_path, line_number, message):
    print "%s:%d: warning: %s" % (file_path, line_number, message.encode("utf8"))

def error(file_path, line_number, message):
    print "%s:%d: error: %s" % (file_path, line_number, message)

m_paths_and_line_numbers_for_key = {} # [{'k1':(('f1, n1'), ('f1, n2'), ...), ...}]
s_paths_and_line_numbers_for_key = {} # [{'k1':(('f1, n1'), ('f1, n2'), ...), ...}]

def language_code_in_strings_path(p):
    m = re.search(".*/(.*?.lproj)/", p)
    if m:
        return m.group(1)
    return None

def key_in_string(s):
    m = re.search("(?u)^\"(.*?)\"\s*=", s)
    if not m:
        return None

    key = m.group(1)

    if key.startswith("//") or key.startswith("/*"):
        return None

    return key

def key_in_code_line(s):
    matches = re.findall("NSLocalizedString\(@\"(.*?)\",", s);
    if len(matches) == 0:
        return None;

    return matches

def guess_encoding(path):
    enc = 'utf-8'

    size = os.path.getsize(path)
    if size < 2:
        return enc

    f = open(path, 'rb')
    first_two_bytes = f.read(2)
    f.close()

    if first_two_bytes == codecs.BOM_UTF16:
        enc = 'utf-16'
    elif first_two_bytes == codecs.BOM_UTF16_LE:
        enc = 'utf-16-le'
    elif first_two_bytes == codecs.BOM_UTF16_BE:
        enc = 'utf-16-be'

    return enc

def keys_set_in_strings_file_at_path(p):

    enc = guess_encoding(p)
    f = codecs.open(p, encoding=enc)
    keys = set()

    line = 0
    for s in f:
        line += 1

        if s.strip().startswith('//'):
            continue

        key = key_in_string(s)

        if not key:
            continue

        if key in keys:
            error(p, line, "key already defined: \"%s\"" % key.encode(enc))
            continue

        keys.add(key)

        if key not in s_paths_and_line_numbers_for_key:
            s_paths_and_line_numbers_for_key[key] = set()
        s_paths_and_line_numbers_for_key[key].add((p, line))

    return keys

def localized_strings_at_path(p):

    enc = guess_encoding(p)
    f = codecs.open(p, encoding=enc)

    keys = set()

    line = 0
    for s in f.xreadlines():
        line += 1

        if s.strip().startswith('//'):
            continue

        keylist = key_in_code_line(s)
        if not keylist:
            continue

        keys |= set(keylist)

        for key in keylist:
            if key not in m_paths_and_line_numbers_for_key:
                m_paths_and_line_numbers_for_key[key] = set()

            m_paths_and_line_numbers_for_key[key].add((p, line))

    return keys

def paths_with_files_passing_test_at_path(test, path, exclude_dirs):
    for root, dirs, files in os.walk(path, topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for p in (os.path.join(root, f) for f in files if test(f)):
            yield p

def keys_set_in_code_at_path(path, exclude_dirs):
    m_paths = paths_with_files_passing_test_at_path(lambda f:f.endswith('.m'), path, exclude_dirs)

    localized_strings = set()

    for p in m_paths:
        keys = localized_strings_at_path(p)
        localized_strings.update(keys)

    return localized_strings

def show_untranslated_keys_in_project(project_path, exclude_dirs):

    if not project_path or not os.path.exists(project_path):
        error("", 0, "bad project path:%s" % project_path)
        return

    keys_set_in_code = keys_set_in_code_at_path(project_path, exclude_dirs)

    strings_paths = paths_with_files_passing_test_at_path(lambda f:f == "Localizable.strings", project_path, exclude_dirs)

    for p in strings_paths:

        keys_set_in_strings = keys_set_in_strings_file_at_path(p)

        missing_keys = keys_set_in_code - keys_set_in_strings

        unused_keys = keys_set_in_strings - keys_set_in_code

        language_code = language_code_in_strings_path(p)

        for k in missing_keys:
            message = "missing key in %s: \"%s\"" % (language_code, unicode(k, 'utf-8'))

            for (p_, n) in m_paths_and_line_numbers_for_key[k]:
                warning(p_, n, message)

        for k in unused_keys:
            message = "unused key in %s: \"%s\"" % (language_code, k)

            for (p, n) in s_paths_and_line_numbers_for_key[k]:
                warning(p, n, message)

def main():

    p = optparse.OptionParser()
    p.add_option('--project-path', '-p', dest="project_path")
    p.add_option('--exclude-dirs', '-e', type="string", default=[], dest="exclude_dirs")
    options, arguments = p.parse_args()

    project_path = None

    if 'PROJECT_DIR' in os.environ:
        project_path = os.environ['PROJECT_DIR']
    elif options.project_path:
        project_path = options.project_path

    show_untranslated_keys_in_project(project_path, options.exclude_dirs)

if __name__ == "__main__":
    main()
