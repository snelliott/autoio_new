""" test autoparse
"""

import autoparse


PATTERNS = (
    autoparse.pattern.LOWERCASE_LETTER,
    autoparse.pattern.UPPERCASE_LETTER,
    autoparse.pattern.LETTER,
    autoparse.pattern.DIGIT,
)
STRING = ' ___A_a_ * & b ___c_ C 1d 2 __e_ D__'
STRING2 = (
    'A*_ 1 a z>\n'
    'B$- 2 b y~\n'
    'C%+ 3 c x,'
)

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


def test__first_capture():
    """ test autoparse.find.first_capture
    """
    cap = autoparse.find.first_capture('(cl)', XYZ_STRING)
    assert cap is None
    cap = autoparse.find.first_capture('(cl)', XYZ_STRING, case=False)
    assert cap == 'Cl'


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


def test__split():
    """ test find.split
        test find.split_words
        test find.split_lines
    """

    pattern = '___c_'
    assert autoparse.find.split(pattern, STRING, case=True) == (
        ' ___A_a_ * & b ', ' C 1d 2 __e_ D__')
    assert autoparse.find.split_words(STRING) == (
        '___A_a_', '*', '&', 'b', '___c_', 'C', '1d', '2', '__e_', 'D__')
    assert autoparse.find.split_lines(STRING2) == (
        'A*_ 1 a z>', 'B$- 2 b y~', 'C%+ 3 c x,')


def test__simple_finders():
    """ test find.starts_with
    """

    pattern = autoparse.pattern.escape('A*_')
    assert autoparse.find.starts_with(pattern, STRING2, case=True)

    pattern = autoparse.pattern.escape('x,')
    assert autoparse.find.ends_with(pattern, STRING2, case=True)

    pattern = autoparse.pattern.escape('C%+')
    ptt_matcher = autoparse.find.matcher(pattern, case=True)
    assert ptt_matcher(STRING2)

    pattern = (
        'charge:' +
        autoparse.pattern.capturing(autoparse.pattern.NUMBER))
    assert autoparse.find.all_captures(pattern, XYZ_STRING, case=True) is None

    pattern = None
    assert autoparse.find.all_captures(pattern, XYZ_STRING, case=True) is None

    pattern = (
        'charge: ' +
        autoparse.pattern.capturing(autoparse.pattern.NUMBER))
    assert autoparse.find.all_captures(pattern, XYZ_STRING) == ('0',)


def test__advanced_finders():
    """ test find.first_matching_pattern
        test find.first_matching_pattern_all_captures
        test find.first_matching_pattern_first_capture
        test find.first_matching_pattern_last_capture
    """

    assert autoparse.find.first_matching_pattern(PATTERNS, 'A') == (
        autoparse.pattern.UPPERCASE_LETTER)
    assert autoparse.find.first_matching_pattern(PATTERNS, 'a') == (
        autoparse.pattern.LOWERCASE_LETTER)
    assert autoparse.find.first_matching_pattern(PATTERNS, '5') == (
        autoparse.pattern.DIGIT)

    patterns = list(map(autoparse.pattern.capturing, PATTERNS))
    assert (
        autoparse.find.first_matching_pattern_all_captures(patterns, STRING)
        == ('a', 'b', 'c', 'd', 'e')
    )

    patterns = list(map(autoparse.pattern.capturing, PATTERNS))
    assert (
        autoparse.find.first_matching_pattern_first_capture(patterns, STRING)
        == 'a'
    )

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
    val = autoparse.cast(cap)
    assert val is None

    mcap = autoparse.find.first_capture(mult_pattern, XYZ_STRING)
    mval = autoparse.cast(mcap)
    assert mval == 1


def test__singles():
    """ test conv.singles
    """
    pattern = autoparse.pattern.capturing(autoparse.pattern.FLOAT)
    caps = autoparse.find.all_captures(pattern, XYZ_STRING)
    vals = autoparse.cast(caps)
    assert vals == (
        1.584823, -0.748487, -0.427122, 0.61922, 0.190166, -0.271639,
        -0.635731, -0.183914, -0.180364, -1.602333, 0.736678, -0.026051,
        0.916321, 1.229946, -0.227127, -0.8823, -1.224388, -0.229636
    )


def test__multi():
    """ test conv.multi
    """
    mcap = autoparse.find.first_capture(XYZ_LINE_PATTERN, XYZ_STRING)
    mval = autoparse.cast(mcap)
    assert mval == ('F', 1.584823, -0.748487, -0.427122)

    mcap = autoparse.find.first_capture(BAD_XYZ_LINE_PATTERN, XYZ_STRING)
    mval = autoparse.cast(mcap)
    assert mval is None


def test__multis():
    """ test conv.multis
    """
    mcaps = autoparse.find.all_captures(XYZ_LINE_PATTERN, XYZ_STRING)
    mvals = autoparse.cast(mcaps)
    assert mvals == (('F', 1.584823, -0.748487, -0.427122),
                     ('C', 0.61922, 0.190166, -0.271639),
                     ('C', -0.635731, -0.183914, -0.180364),
                     ('Cl', -1.602333, 0.736678, -0.026051),
                     ('H', 0.916321, 1.229946, -0.227127),
                     ('H', -0.8823, -1.224388, -0.229636))
