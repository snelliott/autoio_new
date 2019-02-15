""" test autoparse
"""
import autoparse

STRING1 = """
>>> name = "Bob"
>>> Age = 54
>>> has_W2 = True
>>> print(name, Age, has_W2)
Bob 54 True
>>> 1099_filed = False
SyntaxError: invalid token
"""

STRING2 = """

d

   dflkjs 1309

df kkk


"""


def test__variable_name():
    """ test autoparse.pattern.VARIABLE_NAME
    """
    pattern = autoparse.pattern.capturing(autoparse.pattern.VARIABLE_NAME)
    captures = autoparse.find.all_captures(pattern, STRING1)
    assert captures == (
        'name', 'Bob', 'Age', 'has_W2', 'True', 'print', 'name', 'Age',
        'has_W2', 'Bob', 'True', '_filed', 'False', 'SyntaxError', 'invalid',
        'token'
    )


def test__remove_empty_lines():
    """ test autoparse.find.remove_empty_lines
    """
    assert autoparse.find.remove_empty_lines(STRING2) == (
        'd\n   dflkjs 1309\ndf kkk\n'
    )


def test__is_number():
    """ test autoparse.find.is_number
    """
    assert autoparse.find.is_number(' 5 ') is True
    assert autoparse.find.is_number(' 1e-5 ') is True
    assert autoparse.find.is_number(' 1e- 5 ') is False
    assert autoparse.find.is_number(' .1e-200     \n \t \n ') is True


if __name__ == '__main__':
    test__variable_name()
    test__remove_empty_lines()
    test__is_number()
