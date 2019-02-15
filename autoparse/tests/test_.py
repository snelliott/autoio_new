""" test autoparse
"""
import autoparse

STRING = """
>>> name = "Bob"
>>> Age = 54
>>> has_W2 = True
>>> print(name, Age, has_W2)
Bob 54 True
>>> 1099_filed = False
SyntaxError: invalid token
"""


def test__variable_name():
    """ test autoparse.pattern.VARIABLE_NAME
    """
    pattern = autoparse.pattern.capturing(autoparse.pattern.VARIABLE_NAME)
    captures = autoparse.find.all_captures(pattern, STRING)
    assert captures == (
        'name', 'Bob', 'Age', 'has_W2', 'True', 'print', 'name', 'Age',
        'has_W2', 'Bob', 'True', '_filed', 'False', 'SyntaxError', 'invalid',
        'token'
    )


if __name__ == '__main__':
    test__variable_name()
