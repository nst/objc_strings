**Goal**

Helps in localizing Cocoa applications by detecting unused and missing keys in '.strings' files.

**Input**

path of an Objective-C project

**Output**

for each .strings file, missing keys and unused keys

**Sample run**

    $ python objc_strings.py /Users/nst/Projects/cocoaslideshow

    --------------------------------------------------------------------------------
    file: /Users/nst/Projects/cocoaslideshow/French.lproj/Localizable.strings
    --------------------------------------------------------------------------------
    
    --------------------------- missing keys in .strings ---------------------------
    
    Thumbnails
    Export
    
    --------------------------- unused keys in .strings ----------------------------
    
    Download now
    Ignore and Continue
    Add Files?
    
    --------------------------------------------------------------------------------
    file: /Users/nst/Projects/cocoaslideshow/English.lproj/Localizable.strings
    --------------------------------------------------------------------------------
    
    --------------------------- missing keys in .strings ---------------------------
    
    Thumbnails
    Export
    
    --------------------------- unused keys in .strings ----------------------------
    
    Download now
    Ignore and Continue
    Add Files?
