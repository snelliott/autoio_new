""" test autoparse
"""
import autoparse


BLOCK_STRING = '''start
    <contents 1>
end
start
    <contents 2>
end
start
    <contents 3>
end
'''
PATTERNS = (
    autoparse.pattern.LOWERCASE_LETTER,
    autoparse.pattern.UPPERCASE_LETTER,
    autoparse.pattern.LETTER,
    autoparse.pattern.DIGIT,
)
STRING = ' ___A_a_ * & b ___c_ C 1d 2 __e_ D__'


def test__variable_name():
    """ test autoparse.pattern.VARIABLE_NAME
    """
    string = '''
    name = "Bob"
    Age = 54
    has_W2 = True
    print(name, Age, has_W2)
    Bob 54 True
    1099_filed = False
    SyntaxError: invalid token'''
    pattern = autoparse.pattern.capturing(autoparse.pattern.VARIABLE_NAME)
    captures = autoparse.find.all_captures(pattern, string)
    assert captures == (
        'name', 'Bob', 'Age', 'has_W2', 'True', 'print', 'name', 'Age',
        'has_W2', 'Bob', 'True', '_filed', 'False', 'SyntaxError', 'invalid',
        'token'
    )


def test__remove_empty_lines():
    """ test autoparse.find.remove_empty_lines
    """
    string = ' dkjsdf alsdh\n\n\n\n    asdf09j123\n\ndsaf09uasdf'
    assert autoparse.find.remove_empty_lines(string) == (
        ' dkjsdf alsdh\n    asdf09j123\ndsaf09uasdf'
    )


def test__is_number():
    """ test autoparse.find.is_number
    """
    assert autoparse.find.is_number(' 5 ') is True
    assert autoparse.find.is_number(' 1e-5 ') is True
    assert autoparse.find.is_number(' 1e- 5 ') is False
    assert autoparse.find.is_number(' .1e-200     \n \t \n ') is True


def test__first_block():
    """ test autoparse.find.first_block
    """
    assert (autoparse.find.first_block('start', 'end', BLOCK_STRING) ==
            'start\n    <contents 1>\nend')


def test__last_block():
    """ test autoparse.find.last_block
    """
    assert (autoparse.find.last_block('start', 'end', BLOCK_STRING) ==
            'start\n    <contents 3>\nend')


def test__all_blocks():
    """ test autoparse.find.last_block
    """
    assert (autoparse.find.all_blocks('start', 'end', BLOCK_STRING) ==
            ('start\n    <contents 1>\nend',
             'start\n    <contents 2>\nend',
             'start\n    <contents 3>\nend',))


def test__first_matching_pattern():
    """ test autoparse.find.first_matching_pattern
    """
    assert autoparse.find.first_matching_pattern(PATTERNS, 'A') == (
        autoparse.pattern.UPPERCASE_LETTER)
    assert autoparse.find.first_matching_pattern(PATTERNS, 'a') == (
        autoparse.pattern.LOWERCASE_LETTER)
    assert autoparse.find.first_matching_pattern(PATTERNS, '5') == (
        autoparse.pattern.DIGIT)


def test__first_matching_pattern_all_captures():
    """ test find.first_matching_pattern_all_captures
    """
    patterns = list(map(autoparse.pattern.capturing, PATTERNS))
    assert (
        autoparse.find.first_matching_pattern_all_captures(patterns, STRING)
        == ('a', 'b', 'c', 'd', 'e')
    )


def test__first_matching_pattern_first_capture():
    """ test find.first_matching_pattern_first_capture
    """
    patterns = list(map(autoparse.pattern.capturing, PATTERNS))
    assert (
        autoparse.find.first_matching_pattern_first_capture(patterns, STRING)
        == 'a'
    )


def test__first_matching_pattern_last_capture():
    """ test find.first_matching_pattern_last_capture
    """
    patterns = list(map(autoparse.pattern.capturing, PATTERNS))
    assert (
        autoparse.find.first_matching_pattern_last_capture(patterns, STRING)
        == 'e'
    )


if __name__ == '__main__':
    # test__variable_name()
    # test__is_number()
    # test__first_block()
    # test__last_block()
    # test__all_blocks()
    # test__remove_empty_lines()
    # test__first_matching_pattern()
    test__first_matching_pattern_all_captures()
    test__first_matching_pattern_first_capture()
