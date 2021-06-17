""" Test pattern parsers
"""

import ioformat


# Build keyword-value dicts from block_dcts
def test__keyword_value_dct_parser():
    """ test
    """

    keyval_str_1 = """
    (
        val1 = 100
        val2 = 100.0
    )
    """
    keyval_str_2 = """
        val1 = true
        val2 = True
        val3 = false
        val4 = False
        val5 = none
        val6 = None
    """
    keyval_block_dct = {
        'key1': keyval_str_1,
        'key2': keyval_str_2
    }

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

    dct = ioformat.ptt.keyword_dcts_from_blocks(
        keyval_block_dct)
    assert ref_dct == dct  # lazy assert


# Complex block parsers
def test__keyword_value_block_parser():
    """ test ioformat.ptt.keyword_dct_from_paren_blocks
        test ioformat.ptt.keyword_dct_from_block
        test ioformat.ptt.values_from_block
    """

    block = """
    key1 = (
        subkey1 = val1-1
        subkey2 = val1-2
    )
    key2 = (
        subkey1 = val2-1
        subkey2 = val2-2
    )
    key3 = (
        100 200 300
    )
    """

    ref_dct = {
        'key1': {
            'subkey1': 'val1-1',
            'subkey2': 'val1-2'
        },
        'key2': {
            'subkey1': 'val2-1',
            'subkey2': 'val2-2'
        },
        'key3': (100, 200, 300)
    }

    dct = ioformat.ptt.keyword_dct_from_paren_blocks(block)
    assert ref_dct == dct


# Simple Block parsers
def test__end_block_parsers():
    """ test ioformat.ptt.named_end_blocks
        test ioformat.ptt.named_end_block_ptt
        test ioformat.ptt.end_block
        test ioformat.ptt.end_block_ptt
    """

    end_block = (
        'section name1\n'
        '<SECTION TEXT 1>\n'
        'end section\n'
        '\n'
        'section name2\n'
        '<SECTION TEXT 2>\n'
        'end section'
    )

    # name end block
    blocks = ioformat.ptt.named_end_blocks(
        end_block, 'section', footer='section')
    assert blocks == {
        'name1': '\n<SECTION TEXT 1>\n',
        'name2': '\n<SECTION TEXT 2>\n'}

    blocks = ioformat.ptt.named_end_blocks(
        end_block, 'section', footer='stop')  # footer incorrect
    assert blocks is None

    # end block
    block = ioformat.ptt.end_block(
        end_block, 'section', name='name1', footer='section')
    assert block == ('name1', '\n<SECTION TEXT 1>\n')

    block = ioformat.ptt.end_block(
        end_block, 'section', name='name3', footer='section')
    assert block is None


def test__symb_block_parsers():
    """ test ioformat.ptt.symb_block
        test ioformat.ptt.symb_block_ptt
    """

    symb_block_1 = (
        '$section1\n'
        '<SECTION TEXT 1>\n'
        '$end'
    )

    symb_block_2 = (
        '%section2\n'
        '<SECTION TEXT 2>\n'
        '%end'
    )

    block = ioformat.ptt.symb_block(
        symb_block_1, '$', 'section')
    assert block == ('section', '1\n<SECTION TEXT 1>\n')

    block = ioformat.ptt.symb_block(
        symb_block_2, '$', 'section')
    assert block is None

    block = ioformat.ptt.symb_block(
        symb_block_1, '%', 'section')
    assert block is None

    block = ioformat.ptt.symb_block(
        symb_block_2, '%', 'section')
    assert block == ('section', '2\n<SECTION TEXT 2>\n')


def test__paren_block_parsers():
    """ test ioformat.ptt.paren_blocks
        test ioformat.ptt.paren_block_ptt
    """

    paren_block = (
        'key1 = ( <SECTION TEXT1> )\n'
        'key2 = (\n'
        '    <SECTION TEXT2> )\n'
        'key3 = (\n'
        '    <SECTION TEXT3>\n'
        ')'
    )

    blocks = ioformat.ptt.paren_blocks(
        paren_block, key=None)
    assert blocks == (
        ('key1', ' <SECTION TEXT1> '),
        ('key2', '\n    <SECTION TEXT2> '),
        ('key3', '\n    <SECTION TEXT3>\n'))

    blocks = ioformat.ptt.paren_blocks(
        paren_block, key='key2')
    assert blocks == (('key2', '\n    <SECTION TEXT2> '),)


# Simple line parsers
def test__idx_line_parser():
    """ test ioformat.ptt.idx_lst_from_line
    """

    idx_block = (
        '1\n'
        '2,5\n'
        '7-9\n'
        '10,13-15\n'
        '17-19,22\n'
        '24-26,28-30'
    )

    lines = idx_block.strip().splitlines()
    assert ioformat.ptt.idx_lst_from_line(lines[0]) == (1,)
    assert ioformat.ptt.idx_lst_from_line(lines[1]) == (2, 5)
    assert ioformat.ptt.idx_lst_from_line(lines[2]) == (7, 8, 9)
    assert ioformat.ptt.idx_lst_from_line(lines[3]) == (10, 13, 14, 15)
    assert ioformat.ptt.idx_lst_from_line(lines[4]) == (17, 18, 19, 22)
    assert ioformat.ptt.idx_lst_from_line(lines[5]) == (24, 25, 26, 28, 29, 30)


if __name__ == '__main__':
    test__keyword_value_dct_parser()
    test__keyword_value_block_parser()
    test__end_block_parsers()
    test__symb_block_parsers()
    test__paren_block_parsers()
    test__idx_line_parser()
