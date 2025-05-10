#!/usr/bin/env python3

'''
Build a LaTeX file.
Choose TeX engine, root file and command line options based on magic comments.
Filter output to show only errors, warnings, over-/underfull boxes, tracing commands and prompts.
Run biber and makeglossaries if necessary.
The hyperref package is required so that LaTeX outputs the warning which this program uses to detect that makeglossaries needs to be run.

All output from this program and it's subprocesses is written to stderr instead of stdout
except for the paths printed with --get-* so that they can be easily captured in a variable.
'''

APP_NAME = 'latex-runner'
__version__ = '1.2.0'
