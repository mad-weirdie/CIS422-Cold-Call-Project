"""
Set of tests for the student class
"""

from student import Student

a = Student(
    "First", "Last", "950000000", "student@uoregon.edu", "first", "0")
b = Student(
    "First", "Last", "950000000", "student@uoregon.edu", "first", "0")
c = Student(
    "First", "Last", "950000000", "student@uoregon.edu", "first", "1")
d = Student(
    "Newname", "Last", "950000000", "student@uoregon.edu", "first", "1")
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