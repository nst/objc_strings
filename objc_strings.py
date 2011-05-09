#! /usr/bin/python
# https://github.com/nst/objc_strings

__author__ = "Nicolas Seriot"
__date__ = "2011-05-09"

"""
Goal: helps Cocoa applications localization by detecting unused and missing keys in '.strings' files

Input: path of an Objective-C project

Output: for each .strings file, missing keys and unused keys

Typical usage: $ python objc_strings.py /path/to/cocoa/project
"""

import sys
import os
import re
import codecs

def keys_in_file_at_path(p):

    for encoding in ('utf-8', 'utf-16'):

        try:
            keys = set()
            f = codecs.open(p, encoding=encoding)
            
            for s in f.readlines():
                m = re.search("\"(.*?)\"", s)
                if not m:
                    continue
                
                key = m.group(1)
        
                if key.startswith("//") or key.startswith("/*"):
                    continue
                
                keys.add(key)
                
            return keys

        except:
            pass
    
    return None

def localized_strings_at_path(p):
    f = open(p)
    
    keys = set()
    
    for s in f.xreadlines():
        # we don't use genstrings because it won't redirect output to stdout
        m = re.search("NSLocalizedString\(@\"(.*?)\"", s)
        if not m:
            continue
        
        key = m.group(1)
        
        keys.add(key)
        
    return keys

def add_objc_m_files(set, dir, files):
    for f in files:
        path = os.path.join(dir, f)
        if not os.path.isdir(path) and f.endswith('.m'):
            set.add(path)
    return set

def add_localizable_files(set, dir, files):
    for f in files:
        path = os.path.join(dir, f)
        if not os.path.isdir(path) and f == "Localizable.strings":
            set.add(path)
    return set
    
def objc_m_paths_in_directory(path):
    paths = set()
    os.path.walk(path, add_objc_m_files, paths)
    return paths
    
def strings_paths_in_dir(path):
    paths = set()
    os.path.walk(path, add_localizable_files, paths)
    return paths

def keys_in_code_at_path(path):
    m_paths = objc_m_paths_in_directory(path)
    
    localized_strings = set()
    
    for p in m_paths:
        keys = localized_strings_at_path(p)
        
        localized_strings.update(keys)

    return localized_strings
    
def main():
    if len(sys.argv) != 2 or not os.path.exists(sys.argv[1]):
        print "-- prints missing and unused keys in cocoa .strings files"
        print "USAGE: $ python %s PROJECT_PATH" % sys.argv[0]
        exit(0)
    
    project_path = sys.argv[1]
    
    keys_in_code = keys_in_code_at_path(project_path)
    
    strings_paths = strings_paths_in_dir(project_path)
    
    for p in strings_paths:
        print ""
        print "-" * 80
        print "file:", p
        print "-" * 80

        keys_in_strings = keys_in_file_at_path(p)

        missing_keys = keys_in_code - keys_in_strings
        unused_keys = keys_in_strings - keys_in_code
        
        print "\n--------------------------- missing keys in .strings ---------------------------\n"
        for k in missing_keys:
            print k

        print "\n--------------------------- unused keys in .strings ----------------------------\n"
        for k in unused_keys:
            print k
    print ""
        
if __name__=='__main__':
    main()
