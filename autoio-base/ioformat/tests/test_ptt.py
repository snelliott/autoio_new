""" Test pattern parsers
"""

import ioformat

KEYVAL_STR_1 = """
(
    val1 = 100
    val2 = 100.0
)
"""
KEYVAL_STR_2 = """
    val1 = true
    val2 = True
    val3 = false
    val4 = False
    val5 = none
    val6 = None
"""
KEYVAL_BLOCK_DCT = {
    'key1': KEYVAL_STR_1,
    'key2': KEYVAL_STR_2
}

END_BLOCK = """
section name1
<SECTION TEXT 1>
end section

section name2
<SECTION TEXT 2>
end section
"""

SYMB_BLOCK_1 = """
$section1
<SECTION TEXT 1>
$end
"""

SYMB_BLOCK_2 = """
%section2
<SECTION TEXT 2>
%end
"""

PAREN_BLOCK = """
key1 = ( <SECTION TEXT1> )
key2 = (
    <SECTION TEXT2> )
key3 = (
    <SECTION TEXT3>
)
"""

IDX_BLOCK = """
1
2,5
7-9
10,13-15
17-19,22
24-26,28-30
"""


def test__keyword_value_parsers():
    """ test
    """

    ref_dct = {
        'key1': {'val1': 100,
                 'val2': 100.0},
        'key2': {'val1': True,
                 'val2': True,
                 'val3': False,
                 'val4': False,
                 'val5': None,
                 'val6': None}
    }

    dct = ioformat.ptt.keyword_dcts_from_blocks(KEYVAL_BLOCK_DCT)

    # lazy assert
    assert ref_dct == dct


def test__end_block_parsers():
    """ test a name block parser
    """

    blocks = ioformat.ptt.named_end_blocks(
        END_BLOCK, 'section', footer='section')
    assert blocks == {
        'name1': '\n<SECTION TEXT 1>\n',
        'name2': '\n<SECTION TEXT 2>\n'}

    blocks = ioformat.ptt.named_end_blocks(
        END_BLOCK, 'section', footer='stop')  # footer incorrect
    assert blocks is None

    block = ioformat.ptt.end_block(
        END_BLOCK, 'section', name='name1', footer='section')
    assert block == ('name1', '\n<SECTION TEXT 1>\n')

    block = ioformat.ptt.end_block(
        END_BLOCK, 'section', name='name3', footer='section')
    assert block is None


def test__symb_block_parsers():
    """ test a name block parser
    """

    block = ioformat.ptt.symb_block(
        SYMB_BLOCK_1, '$', 'section')
    assert block == ('section', '1\n<SECTION TEXT 1>\n')

    block = ioformat.ptt.symb_block(
        SYMB_BLOCK_2, '$', 'section')
    assert block is None

    block = ioformat.ptt.symb_block(
        SYMB_BLOCK_1, '%', 'section')
    assert block is None

    block = ioformat.ptt.symb_block(
        SYMB_BLOCK_2, '%', 'section')
    assert block == ('section', '2\n<SECTION TEXT 2>\n')


def test__paren_block_parsers():
    """ test paren block parser
    """

    blocks = ioformat.ptt.paren_blocks(
        PAREN_BLOCK, key=None)
    assert blocks == (
        ('key1', ' <SECTION TEXT1> '),
        ('key2', '\n    <SECTION TEXT2> '),
        ('key3', '\n    <SECTION TEXT3>\n'))

    blocks = ioformat.ptt.paren_blocks(
        PAREN_BLOCK, key='key2')
    assert blocks == (('key2', '\n    <SECTION TEXT2> '),)


def test__idx_line_parser():
    """ test
    """

    lines = IDX_BLOCK.strip().splitlines()
    assert ioformat.ptt.idx_lst_from_line(lines[0]) == (1,)
    assert ioformat.ptt.idx_lst_from_line(lines[1]) == (2, 5)
    assert ioformat.ptt.idx_lst_from_line(lines[2]) == (7, 8, 9)
    assert ioformat.ptt.idx_lst_from_line(lines[3]) == (10, 13, 14, 15)
    assert ioformat.ptt.idx_lst_from_line(lines[4]) == (17, 18, 19, 22)
    assert ioformat.ptt.idx_lst_from_line(lines[5]) == (24, 25, 26, 28, 29, 30)


if __name__ == '__main__':
    test__keyword_value_parsers()
    test__end_block_parsers()
    test__symb_block_parsers()
    test__paren_block_parsers()
    test__idx_line_parser()
