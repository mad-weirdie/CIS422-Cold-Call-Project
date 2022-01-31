#!/usr/bin/env python3

###############################################################################
"""
Script Name:    CoolCall Testing Script

Description:    This script can be run at the command line to test the program
                during development.

Author:         Amy Reichhold

Last Edited:    1/25/2022
Last Edit By:   Amy Reichhold
"""
###############################################################################
from student import Student
###############################################################################

# Set of tests for the student class


a = Student(
    "First", "Last", "950000000", "student@uoregon.edu", "first", "0")
b = Student(
    "First", "Last", "950000000", "student@uoregon.edu", "first", "0")

# different reveal code
c = Student(
    "First", "Last", "950000000", "student@uoregon.edu", "first", "1")

# different first name
d = Student(
    "Newname", "Last", "950000000", "student@uoregon.edu", "first", "1")

# different last name
e = Student(
    "Newname", "Newlast", "950000000", "student@uoregon.edu", "first", "1")

def test_equality():
    assert a == b
    assert not a == c
    assert not c == d
    assert not c == e

def test_include_on_deck():
    assert a.include_on_deck()
    assert b.include_on_deck()
    assert not c.include_on_deck()
    assert not d.include_on_deck()
    assert not e.include_on_deck()

def test_call_on():
    print(a.total_num_flags)
    print(a.dates_called)
    a.call_on(True)
    print(a.total_num_flags)
    print(a.dates_called)

if __name__ == "__main__":
    test_equality()
    test_include_on_deck()
    test_call_on()