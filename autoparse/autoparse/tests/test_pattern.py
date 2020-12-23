""" test autoparse
"""

import autoparse


STRING1 = '''
name = "Bob"
Age = 54
has_W2 = True
print(name, Age, has_W2)
Bob 54 True
1099_filed = False
SyntaxError: invalid token'''

STRING2 = (
    'q1a2z3\n'
    'e1a2r3\n'
)
STRING3 = '11111ybnfkw2l40-1'


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


def test__position_checks():
    """ test autoparse.pattern.preceded_by
        test autoparse.pattern.not_preceded_by
        test autoparse.pattern.followed_by
        test autoparse.pattern.not_followed_by
    """

    pattern = (
        autoparse.pattern.preceded_by('q1') +
        autoparse.pattern.capturing(autoparse.pattern.NONNEWLINE)
    )
    assert autoparse.find.first_capture(pattern, STRING2) == 'a'

    pattern = (
        autoparse.pattern.not_preceded_by('q') +
        autoparse.pattern.capturing(autoparse.pattern.NONNEWLINE)
    )
    print(autoparse.find.first_capture(pattern, STRING3))
    # autoparse.pattern.followed_by(pattern)
    # autoparse.pattern.not_followed_by(pattern)


def test__padded():
    """ test autoparse.pattern.lpadded
        test autoparse.pattern.rpadded
        test autoparse.pattern.padded
    """

    pattern = 'AAA'
    assert autoparse.pattern.lpadded(pattern) == '(?:[ \\t])*AAA'
    assert autoparse.pattern.rpadded(pattern) == 'AAA(?:[ \\t])*'
    assert autoparse.pattern.padded(pattern) == '(?:[ \\t])*AAA(?:[ \\t])*'


if __name__ == '__main__':
    test__variable_name()
    test__position_checks()
    test__padded()
