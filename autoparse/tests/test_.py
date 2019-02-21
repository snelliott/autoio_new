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

XYZ_STRING = """6
charge: 0, mult: 1
F    1.584823  -0.748487  -0.427122
C    0.619220   0.190166  -0.271639
C   -0.635731  -0.183914  -0.180364
Cl  -1.602333   0.736678  -0.026051
H    0.916321   1.229946  -0.227127
H   -0.882300  -1.224388  -0.229636
"""

ATOM_SYMBOL_PATTERN = (
    autoparse.pattern.LETTER +
    autoparse.pattern.maybe(autoparse.pattern.LETTER)
)
NUMBER_PATTERN = autoparse.pattern.FLOAT
XYZ_LINE_PATTERN = autoparse.pattern.LINESPACES.join([
    autoparse.pattern.capturing(ATOM_SYMBOL_PATTERN),
    autoparse.pattern.capturing(NUMBER_PATTERN),
    autoparse.pattern.capturing(NUMBER_PATTERN),
    autoparse.pattern.capturing(NUMBER_PATTERN),
])
BAD_XYZ_LINE_PATTERN = autoparse.pattern.LINESPACES.join([
    autoparse.pattern.capturing('BAD'),
    autoparse.pattern.capturing(NUMBER_PATTERN),
    autoparse.pattern.capturing(NUMBER_PATTERN),
    autoparse.pattern.capturing(NUMBER_PATTERN),
])


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


def test__single():
    """ test conv.single
    """
    bad_mult_pattern = autoparse.pattern.LINESPACES.join([
        autoparse.pattern.escape('multiplicity:'),
        autoparse.pattern.capturing(autoparse.pattern.UNSIGNED_INTEGER),
    ])
    mult_pattern = autoparse.pattern.LINESPACES.join([
        autoparse.pattern.escape('mult:'),
        autoparse.pattern.capturing(autoparse.pattern.UNSIGNED_INTEGER),
    ])
    cap = autoparse.find.first_capture(bad_mult_pattern, XYZ_STRING)
    val = autoparse.conv.single(cap, dtype=int)
    assert val is None

    mcap = autoparse.find.first_capture(mult_pattern, XYZ_STRING)
    mval = autoparse.conv.single(mcap, dtype=int)
    assert mval == 1


def test__singles():
    """ test conv.singles
    """
    pattern = autoparse.pattern.capturing(autoparse.pattern.FLOAT)
    caps = autoparse.find.all_captures(pattern, XYZ_STRING)
    vals = autoparse.conv.singles(caps, dtype=float)
    assert vals == (
        1.584823, -0.748487, -0.427122, 0.61922, 0.190166, -0.271639,
        -0.635731, -0.183914, -0.180364, -1.602333, 0.736678, -0.026051,
        0.916321, 1.229946, -0.227127, -0.8823, -1.224388, -0.229636
    )


def test__multi():
    """ test conv.multi
    """
    mcap = autoparse.find.first_capture(XYZ_LINE_PATTERN, XYZ_STRING)
    mval = autoparse.conv.multi(mcap, dtypes=(str, float, float, float))
    assert mval == ('F', 1.584823, -0.748487, -0.427122)

    mcap = autoparse.find.first_capture(BAD_XYZ_LINE_PATTERN, XYZ_STRING)
    mval = autoparse.conv.multi(mcap, dtypes=(str, float, float, float))
    assert mval is None


def test__multis():
    """ test conv.multis
    """
    mcaps = autoparse.find.all_captures(XYZ_LINE_PATTERN, XYZ_STRING)
    mvals = autoparse.conv.multis(mcaps, dtypes=(str, float, float, float))
    assert mvals == (('F', 1.584823, -0.748487, -0.427122),
                     ('C', 0.61922, 0.190166, -0.271639),
                     ('C', -0.635731, -0.183914, -0.180364),
                     ('Cl', -1.602333, 0.736678, -0.026051),
                     ('H', 0.916321, 1.229946, -0.227127),
                     ('H', -0.8823, -1.224388, -0.229636))


if __name__ == '__main__':
    # test__variable_name()
    # test__is_number()
    # test__first_block()
    # test__last_block()
    # test__all_blocks()
    # test__remove_empty_lines()
    # test__first_matching_pattern()
    # test__first_matching_pattern_all_captures()
    # test__first_matching_pattern_first_capture()
    test__single()
    test__singles()
    test__multi()
    test__multis()
