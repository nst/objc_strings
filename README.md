#### Goal

Helps Cocoa applications localization by detecting unused and missing keys in '.strings' files.

#### Input

Path of an Objective-C project.

#### Output

1. warnings for untranslated strings in *.m
2. warnings for unused keys in Localization.strings
3. errors for keys defined twice or more in the same .strings file

#### Typical usage

    $ python objc_strings.py /path/to/obj_c/project
    ./MyProject/en.lproj/Localizable.strings:13: warning: unused key in en.lproj: "Misc"
    ./MyProject/ViewController.m:16: warning: missing key in fr.lproj: "World"

#### Xcode integration

1. make `objc_strings.py` executable

    $ chmod +x objc_strings.py

2. copy `objc_strings.py` to the root of your project
3. add a "Run Script" build phase to your target
4. move this build phase in second position
5. set the script path to `${SOURCE_ROOT}/objc_strings.py`
6. ensure your .strings file are encoded in utf-8

![settings](https://github.com/nst/objc_strings/raw/master/images/settings.png "settings")
![warnings](https://github.com/nst/objc_strings/raw/master/images/warnings.png "warnings")
