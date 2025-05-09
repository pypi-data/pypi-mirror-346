#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Thu Mar 13 14:32:31 2025

@author: Wiesinger Franz
'''


# Python 3+
from enum import Enum, auto


class AppFonts:
    fontheader = ('TkDefaultFont', 16, 'bold')
    fontdefault = ('TkDefaultFont', 10)
    fontabout_header = ('TkDefaultFont', 12, 'bold')


class FieldTypes(Enum):
    string = auto()
    string_list = auto()
    short_string_list = auto()
    iso_datetime_string = auto()
    long_string = auto()
    decimal = auto()
    integer = auto()
    boolean = auto()
