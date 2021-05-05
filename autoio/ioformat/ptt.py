""" Library of patterns to simplify the parsing of input files
"""

import ast
import autoparse.find as apf
import autoparse.pattern as app
import ioformat


# PATTERNS
KEYWORD_KEYVALUE_PATTERN = (
    app.capturing(app.one_or_more(app.NONSPACE)) +
    app.zero_or_more(app.SPACE) +
    '=' +
    app.zero_or_more(app.SPACE) +
    app.capturing(app.LINE_FILL)
)
FULL_BLOCK_PTT = app.capturing(app.one_or_more(app.WILDCARD, greedy=False))
# GEN_PTT = app.capturing(app.one_or_more(app.NONSPACE))
GEN_PTT = app.capturing(app.one_or_more(app.LINE_FILL))


def keyword_value_ptt(key=None):
    """ Build a regex pattern to search for a keyword and its value, defined as
            key = value
        :param key: string for a specific key to find
        :type key: str
        :rtype: str
    """
    keywrd = key if key is not None else app.one_or_more(app.NONSPACE)
    return (app.capturing(keywrd) +
            app.ZSPACES + app.escape('=') + app.ZSPACES +
            GEN_PTT)


def paren_block_ptt(key=None):
    """ Build a regex pattern to search for a keyword and its value, defined as
            key = (value)
        :param key: string for a specific key to find
        :type key: str
        :rtype: str
    """
    keywrd = key if key is not None else app.one_or_more(app.NONSPACE)
    return (app.capturing(keywrd) + app.SPACES + app.escape('=') + app.SPACES +
            app.escape('(') + FULL_BLOCK_PTT + app.escape(')'))


def named_end_block_ptt(header, footer=None):
    """ Build a regex pattern to search for blocks of end
            key = (value)
            {header} {name}
               **TEXT**
            end {footer}
    """

    # Set the top and bottom of the end block pattern
    top_ptt = (
        header + app.SPACES + app.capturing(app.one_or_more(app.NONSPACE)))

    bot_ptt = 'end'
    if footer is not None:
        bot_ptt += app.SPACES + footer

    return top_ptt + FULL_BLOCK_PTT + bot_ptt


def end_block_ptt(header, name=None, footer=None):
    """ Read the string that has the global model information
        can also capture with the name if needed...
        {header} {name}
          DATA
        end {footer}
    """

    # Set the top and bottom of the end block pattern
    top_ptt = header
    if name is not None:
        top_ptt += app.SPACES + app.capturing(name)

    bot_ptt = 'end'
    if footer is not None:
        bot_ptt += app.SPACES + footer

    return top_ptt + FULL_BLOCK_PTT + bot_ptt


# Simple Block Parsers
def paren_blocks(string, key=None):
    """ A pattern for a certain block
    """
    return apf.all_captures(paren_block_ptt(key=key), string)


def keyword_value_blocks(string, key=None):
    """ A pattern for a certain block
    """
    return apf.all_captures(keyword_value_ptt(key=key), string)


def named_end_blocks(string, header, footer=None):
    """ A pattern for a certian block
        rtype: dict[str: str]
    """
    caps = apf.all_captures(
        named_end_block_ptt(header, footer=footer), string)
    if caps is not None:
        caps = dict(zip((cap[0] for cap in caps), (cap[1] for cap in caps)))
    return caps


def end_block(string, header, name=None, footer=None):
    """ A pattern for a certain block
        rtype: str
    """
    _ptt = end_block_ptt(header, name=name, footer=footer)
    cap = apf.first_capture(_ptt, string)

    return cap if cap is not None else None


# Build keyword dictiaonries
def keyword_dcts_from_blocks(block_dct):
    """ Build a dict of dicts from string blocks that are stored in
        a dictionary.
        :param block_dct: dictionary of strings with a name for a key
        :type block_dct: dict[str: str]
        :rtype: dict[str: dict[str:str]]
    """

    new_block_dct = {}
    if block_dct is not None:
        for key, block in block_dct.items():

            key_dct = keyword_dct_from_paren_blocks(block)
            if key_dct is None:
                key_dct = keyword_dct_from_block(block)

            new_block_dct[key] = key_dct

    return new_block_dct


def keyword_dct_from_paren_blocks(block):
    """ Obtains the keyword-value pairs that are defined in blocks from parentheses
        Could be just a bunch of values or a set of keyword-value pairs
            # First check for keyword list or just vals
    """

    ret = {}

    pblocks = paren_blocks(block)
    if pblocks is not None:
        for pblock in pblocks:
            key_dct = keyword_dct_from_block(pblock[1])
            if key_dct is not None:
                ret[pblock[0]] = key_dct
            else:
                vals = values_from_block(pblock[1])
                if vals:
                    ret[pblock[0]] = vals
    else:
        ret = None

    return ret


def keyword_dct_from_block(block):
    """ Take a section with keywords defined and build
        a dictionary for the keywords
        assumes a block that is a list of key-val pairs
    """

    key_dct = None

    if block is not None:
        block = ioformat.remove_whitespace(block)
        key_val_blocks = keyword_value_blocks(block)
        if key_val_blocks is not None:
            key_dct = {}
            for key, val in key_val_blocks:
                formtd_key, formtd_val = format_keyword_values(key, val)
                key_dct[formtd_key] = formtd_val

    return key_dct


# Build various objects containing keyword and value information
def values_from_block(block):
    """ Takes a multiline string that consists solely of floats and
        converts this block into a list of numbers
        could call set_value_type for generality I guess
        prob just do a capture of nums (floats, int, etc)
    """
    caps = apf.all_captures(app.NUMBER, block)
    if caps:
        vals = tuple(float(cap) for cap in caps)
    else:
        vals = None

    return vals


def idx_lst_from_line(line):
    """ Build a list of indices from a block of tests
    """

    idxs = []
    for string in line.strip().split(','):
        if string.isdigit():
            idxs.append(int(string))
        elif '-' in line:
            [idx_begin, idx_end] = string.split('-')
            idxs.extend(list(range(int(idx_begin), int(idx_end)+1)))

    return tuple(idxs)


# Formats the values associated with various keywords
def format_tsk_keywords(keyword_lst):
    """ format keywords string
    """
    keyword_dct = {}
    for keyword in keyword_lst:
        [key, val] = keyword.split('=')
        keyword_dct[key] = set_value_type(val)

    return keyword_dct


def format_keyword_values(keyword, value):
    """ Takes a keyword-value pair in string formats and then returns
        the pair with their types matching the internal Python version.
        Convert string to string, boolean, int, float, etc
        :param key_val_pair:  keyword and its
        :type key_val_pair: (str, str)
        :rtype: (type(str), type(str))
    """

    # [keyword, value] = key_val_pair

    # Format the keyword
    frmtd_keyword = set_value_type(keyword.strip().lower())

    # Format values if it is a list (of string(s), boolean(s), int(s))
    # Additional functionality is used to handle when values are lists
    value = value.strip()
    if all(sym in value for sym in ('[[', ']]')):
        value = value.replace('D', '').replace('d', '')
        value = ast.literal_eval(value)
        frmtd_value = ()
        for sub_lst in value:
            assert all(isinstance(val, int) for val in sub_lst)
            frmtd_value += (
                tuple('D{}'.format(val) for val in sub_lst),
            )
    elif all(sym in value for sym in ('[', ']')):
        value = value.replace('[', '').replace(']', '')
        value = value.split(',')
        frmtd_value = ()
        # Set string in list to boolean or integer if needed
        for elm in value:
            elm = elm.strip()
            if ':' in elm:
                elm_lst = elm.split(':')
                frmtd_value += ((float(elm_lst[0]), elm_lst[1]),)
            else:
                frmtd_value += (set_value_type(elm),)
    else:
        # Format values if it has singular value
        frmtd_value = set_value_type(value)

    return frmtd_keyword, frmtd_value


def set_value_type(value):
    """ set type of value
        right now we handle True/False boolean, int, float, and string
    """

    if value.lower() == 'true':
        frmtd_value = True
    elif value.lower() == 'false':
        frmtd_value = False
    elif value.lower() == 'none':
        frmtd_value = None
    elif value.isdigit():
        frmtd_value = int(value)
    elif 'e' in value:
        try:
            frmtd_value = float(value)
        except ValueError:
            frmtd_value = value
    elif '.' in value:
        if value.replace('.', '').replace('-', '').isdigit():
            frmtd_value = float(value)
    else:
        frmtd_value = value

####""" Library of patterns to simplify the parsing of input files
#"""
#
#import ast
#import autoparse.find as apf
#import autoparse.pattern as app
#import ioformat
#
#
## PATTERNS
#KEYWORD_KEYVALUE_PATTERN = (
#    app.capturing(app.one_or_more(app.NONSPACE)) +
#    app.zero_or_more(app.SPACE) +
#    '=' +
#    app.zero_or_more(app.SPACE) +
#    app.capturing(app.LINE_FILL)
#)
#FULL_BLOCK_PTT = app.capturing(app.one_or_more(app.WILDCARD, greedy=False))
#<<<<<<< HEAD
## GEN_PTT = app.capturing(app.one_or_more(app.NONSPACE))
#GEN_PTT = app.capturing(app.one_or_more(app.LINE_FILL))
#
#
#def keyword_value_ptt(key=None):
#    """ Build a regex pattern to search for a keyword and its value, defined as
#            key = value
#
#        :param key: string for a specific key to find
#        :type key: str
#        :rtype: str
#    """
#    keywrd = key if key is not None else app.one_or_more(app.NONSPACE)
#    return (app.capturing(keywrd) +
#            app.ZSPACES + app.escape('=') + app.ZSPACES +
#            GEN_PTT)
#
#
#def paren_block_ptt(key=None):
#    """ Build a regex pattern to search for a keyword and its value, defined as
#            key = (value)
#
#        :param key: string for a specific key to find
#        :type key: str
#        :rtype: str
#=======
#
#
## Patterns and block
#def paren_block(header, string):
#    """ A patter for a certain block
#    """
#    return apf.first_capture(paren_ptt(header), string)
#
#
#def named_end_blocks(string, header, footer=None):
#    """ A pattern for a certian block
#        rtype: dict[str: str]
#    """ 
#    caps = apf.all_captures(
#        named_end_block_ptt(header, footer=footer), string)
#    if caps is not None:
#        caps = dict(zip((cap[0] for cap in caps), (cap[1] for cap in caps)))
#    return caps
#
#
#def end_block(string, header, name=None, footer=None):
#    """ A pattern for a certain block
#        rtype: str
#    """
#    _ptt = end_block_ptt(header, name=name, footer=footer)
#    cap = apf.first_capture(_ptt, string)
#
#    return cap if cap is not None else None
#
#
#def paren_ptt(string):
#    """ Read the string that has the global model information
#>>>>>>> update autorun and ioformat and mess,varecof writes
#    """
#    keywrd = key if key is not None else app.one_or_more(app.NONSPACE)
#    return (app.capturing(keywrd) + app.SPACES + app.escape('=') + app.SPACES +
#            app.escape('(') + FULL_BLOCK_PTT + app.escape(')'))
#
#
#def named_end_block_ptt(header, footer=None):
#<<<<<<< HEAD
#    """ Build a regex pattern to search for blocks of end
#            key = (value)
#
#            {header} {name}
#               **TEXT**
#            end {footer}
#    """
#
#    # Set the top and bottom of the end block pattern
#    top_ptt = (
#        header + app.SPACES + app.capturing(app.one_or_more(app.NONSPACE)))
#
#=======
#    """ Read the string that has the global model information
#
#        {header} {name}
#          DATA
#        end {footer}
#    """
#    
#    # Set the top and bottom of the end block pattern
#    top_ptt = (
#        header + app.SPACES + app.capturing(app.one_or_more(app.NONSPACE)))
#
#>>>>>>> update autorun and ioformat and mess,varecof writes
#    bot_ptt = 'end'
#    if footer is not None:
#        bot_ptt += app.SPACES + footer
#
#    return top_ptt + FULL_BLOCK_PTT + bot_ptt
#<<<<<<< HEAD
#
#
#def end_block_ptt(header, name=None, footer=None):
#    """ Read the string that has the global model information
#
#        can also capture with the name if needed...
#
#        {header} {name}
#          DATA
#        end {footer}
#    """
#=======
#>>>>>>> update autorun and ioformat and mess,varecof writes
#
#    # Set the top and bottom of the end block pattern
#    top_ptt = header
#    if name is not None:
#        top_ptt += app.SPACES + app.capturing(name)
#
#<<<<<<< HEAD
#    bot_ptt = 'end'
#    if footer is not None:
#        bot_ptt += app.SPACES + footer
#
#    return top_ptt + FULL_BLOCK_PTT + bot_ptt
#
#
## Simple Block Parsers
#def paren_blocks(string, key=None):
#    """ A patter for a certain block
#    """
#    return apf.all_captures(paren_block_ptt(key=key), string)
#
#
#def keyword_value_blocks(string, key=None):
#    """ A patter for a certain block
#    """
#    return apf.all_captures(keyword_value_ptt(key=key), string)
#
#
#def named_end_blocks(string, header, footer=None):
#    """ A pattern for a certian block
#        rtype: dict[str: str]
#    """
#    caps = apf.all_captures(
#        named_end_block_ptt(header, footer=footer), string)
#    if caps is not None:
#        caps = dict(zip((cap[0] for cap in caps), (cap[1] for cap in caps)))
#    return caps
#=======
#def end_block_ptt(header, name=None, footer=None):
#    """ Read the string that has the global model information
#
#        {header} {name}
#          DATA
#        end {footer}
#    """
#    
#    # Set the top and bottom of the end block pattern
#    top_ptt = header
#    if name is not None:
#        top_ptt += app.SPACES + app.capturing(name)
#
#    bot_ptt = 'end'
#    if footer is not None:
#        bot_ptt += app.SPACES + footer
#
#    return top_ptt + FULL_BLOCK_PTT + bot_ptt
#>>>>>>> update autorun and ioformat and mess,varecof writes
#
#
#def end_block(string, header, name=None, footer=None):
#    """ A pattern for a certain block
#        rtype: str
#    """
#    _ptt = end_block_ptt(header, name=name, footer=footer)
#    cap = apf.first_capture(_ptt, string)
#
#    return cap if cap is not None else None
#
#
## Build keyword dictiaonries
#def keyword_dcts_from_blocks(block_dct):
#    """ Build a dict of dicts from string blocks that are stored in
#        a dictionary.
#
#        :param block_dct: dictionary of strings with a name for a key
#        :type block_dct: dict[str: str]
#        :rtype: dict[str: dict[str:str]]
#    """
#
#    new_block_dct = {}
#    if block_dct is not None:
#        for key, block in block_dct.items():
#
#            key_dct = keyword_dct_from_paren_blocks(block)
#            if key_dct is None:
#                key_dct = keyword_dct_from_block(block)
#
#            new_block_dct[key] = key_dct
#
#<<<<<<< HEAD
#    return new_block_dct
#=======
#def parse_idxs(idx_str):
#>>>>>>> update autorun and ioformat and mess,varecof writes
#
#
#def keyword_dct_from_paren_blocks(block):
#    """ Obtains the keyword-value pairs that are defined in blocks from parentheses
#        Could be just a bunch of values or a set of keyword-value pairs
#
#            # First check for keyword list or just vals
#    """
#
#<<<<<<< HEAD
#    ret = {}
#
#    pblocks = paren_blocks(block)
#    if pblocks is not None:
#        for pblock in pblocks:
#            key_dct = keyword_dct_from_block(pblock[1])
#            if key_dct is not None:
#                ret[pblock[0]] = key_dct
#            else:
#                vals = values_from_block(pblock[1])
#                if vals:
#                    ret[pblock[0]] = vals
#    else:
#        ret = None
#
#    return ret
#
#
#def keyword_dct_from_block(block):
#=======
#    # remove whitespace
#    idx_str = idx_str.strip()
#
#    # handle just single digit
#    if idx_str.isdigit():
#        idxs = [int(idx_str)]
#    
#    # Split by the commas
#    idxs = []
#    for string in idx_str.split(','):
#        if string.isdigit():
#            idxs.append(int(string))
#        elif '-' in idx_str:
#            [idx_begin, idx_end] = string.split('-')
#            idxs.extend(list(range(int(idx_begin), int(idx_end)+1)))
#
#    return tuple(idxs)
#
#
## Build a keyword dictionary
#def format_tsk_keywords(keyword_lst):
#    """ format keywords string
#    """
#    keyword_dct = {}
#    for keyword in keyword_lst:
#        [key, val] = keyword.split('=')
#        keyword_dct[key] = set_value_type(val)
#
#    return keyword_dct
#
#
#def keyword_dcts_from_lst(secs_dct):
#    """ a
#        (
#            (section_name, section_str),
#            
#    """
#
#    if secs_dct is not None:
#        for key, val in secs_dct.items():
#            secs_dct[key] = keyword_dct_from_string(val)
#
#    return secs_dct
#
#
#def keyword_dct_from_string(section_str):
#>>>>>>> update autorun and ioformat and mess,varecof writes
#    """ Take a section with keywords defined and build
#        a dictionary for the keywords
#
#        assumes a block that is a list of key-val pairs
#    """
#
#<<<<<<< HEAD
#    key_dct = None
#
#    if block is not None:
#        block = ioformat.remove_whitespace(block)
#        key_val_blocks = keyword_value_blocks(block)
#        if key_val_blocks is not None:
#            key_dct = {}
#            for key, val in key_val_blocks:
#                formtd_key, formtd_val = format_keyword_values(key, val)
#                key_dct[formtd_key] = formtd_val
#
#    return key_dct
#
#
## Build various objects containing keyword and value information
#def values_from_block(block):
#    """ Takes a multiline string that consists solely of floats and
#        converts this block into a list of numbers
#=======
#    if section_str is not None:
#        key_dct = {}
#        section_str = ioformat.remove_whitespace(section_str)
#        for line in section_str.splitlines():
#            print('line')
#            key_val = apf.first_capture(KEYWORD_KEYVALUE_PATTERN, line)
#            formtd_key, formtd_val = format_param_vals(key_val)
#            key_dct[formtd_key] = formtd_val
#    else:
#        key_dct = None
#
#    return key_dct
#>>>>>>> update autorun and ioformat and mess,varecof writes
#
#        could call set_value_type for generality I guess
#
#<<<<<<< HEAD
#        prob just do a capture of nums (floats, int, etc)
#=======
#def keyword_lst(section_str):
#    """ build lst
#>>>>>>> update autorun and ioformat and mess,varecof writes
#    """
#    caps = apf.all_captures(app.NUMBER, block)
#    if caps:
#        vals = tuple(float(cap) for cap in caps)
#    else:
#        vals = None
#
#<<<<<<< HEAD
#    return vals
#=======
#    _keyword_lst = []
#    section_str = ioformat.remove_whitespace(section_str)
#    for line in section_str.splitlines():
#        _keyword_lst.append(line)
#
#    return tuple(_keyword_lst)
#>>>>>>> update autorun and ioformat and mess,varecof writes
#
#
#def idx_lst_from_line(line):
#    """ Build a list of indices from a block of tests
#    """
#
#    idxs = []
#    for string in line.strip().split(','):
#        if string.isdigit():
#            idxs.append(int(string))
#        elif '-' in line:
#            [idx_begin, idx_end] = string.split('-')
#            idxs.extend(list(range(int(idx_begin), int(idx_end)+1)))
#
#    return tuple(idxs)
#
#
## Formats the values associated with various keywords
#<<<<<<< HEAD
#def format_tsk_keywords(keyword_lst):
#    """ format keywords string
#=======
#def format_param_vals(pvals):
#    """ format param vals string
#>>>>>>> update autorun and ioformat and mess,varecof writes
#    """
#    keyword_dct = {}
#    for keyword in keyword_lst:
#        [key, val] = keyword.split('=')
#        keyword_dct[key] = set_value_type(val)
#
#    return keyword_dct
#
#
#def format_keyword_values(keyword, value):
#    """ Takes a keyword-value pair in string formats and then returns
#        the pair with their types matching the internal Python version.
#
#        Convert string to string, boolean, int, float, etc
#
#        :param key_val_pair:  keyword and its
#        :type key_val_pair: (str, str)
#        :rtype: (type(str), type(str))
#    """
#
#    # [keyword, value] = key_val_pair
#
#    # Format the keyword
#    frmtd_keyword = set_value_type(keyword.strip().lower())
#
#    # Format values if it is a list (of string(s), boolean(s), int(s))
#    # Additional functionality is used to handle when values are lists
#    value = value.strip()
#    if all(sym in value for sym in ('[[', ']]')):
#        value = value.replace('D', '').replace('d', '')
#        value = ast.literal_eval(value)
#        frmtd_value = ()
#        for sub_lst in value:
#            assert all(isinstance(val, int) for val in sub_lst)
#            frmtd_value += (
#                tuple('D{}'.format(val) for val in sub_lst),
#            )
#    elif all(sym in value for sym in ('[', ']')):
#        value = value.replace('[', '').replace(']', '')
#        value = value.split(',')
#        frmtd_value = ()
#        # Set string in list to boolean or integer if needed
#        for elm in value:
#            elm = elm.strip()
#            if ':' in elm:
#                elm_lst = elm.split(':')
#                frmtd_value += ((float(elm_lst[0]), elm_lst[1]),)
#            else:
#                frmtd_value += (set_value_type(elm),)
#    else:
#        # Format values if it has singular value
#        frmtd_value = set_value_type(value)
#
#    return frmtd_keyword, frmtd_value
#
#
#def set_value_type(value):
#    """ set type of value
#        right now we handle True/False boolean, int, float, and string
#    """
#
#    if value.lower() == 'true':
#        frmtd_value = True
#    elif value.lower() == 'false':
#        frmtd_value = False
#    elif value.lower() == 'none':
#        frmtd_value = None
#    elif value.isdigit():
#        frmtd_value = int(value)
#    elif 'e' in value:
#        try:
#            frmtd_value = float(value)
#        except ValueError:
#            frmtd_value = value
#    elif '.' in value:
#        if value.replace('.', '').replace('-', '').isdigit():
#            frmtd_value = float(value)
#    else:
#        frmtd_value = value
#
#    return frmtd_value
