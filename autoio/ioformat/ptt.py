""" Library of patterns to simplify the parsing of input files
"""

import sys
import os
import ast
import ioformat
import autoparse.find as apf
import autoparse.pattern as app


# General Patterns that will be helpful
KEYWORD_KEYVALUE_PATTERN = (
    app.capturing(app.one_or_more(app.NONSPACE)) +
    app.zero_or_more(app.SPACE) +
    '=' +
    app.zero_or_more(app.SPACE) +
    app.capturing(app.LINE_FILL)
)
FULL_BLOCK_PTT = app.capturing(app.one_or_more(app.WILDCARD, greedy=False))


# Patterns and block
def paren_block(header, string):
    """ A patter for a certain block
    """
    return apf.first_capture(paren_ptt(header), string)


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


def paren_ptt(string):
    """ Read the string that has the global model information
    """
    return (string + app.SPACE + app.escape('=') + app.SPACE +
            app.escape('(') +
            app.capturing(app.one_or_more(app.WILDCARD, greedy=False)) +
            app.escape(')'))


def named_end_block_ptt(header, footer=None):
    """ Read the string that has the global model information

        {header} {name}
          DATA
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


def keyword_pattern(string):
    """ Generates the key pattern string
    """
    value = (string +
             app.zero_or_more(app.SPACE) +
             '=' +
             app.zero_or_more(app.SPACE) +
             app.capturing(app.one_or_more(app.NONSPACE)))
    return set_value_type(value)


def parse_idxs(idx_str):

    """ parse idx string
    """

    # remove whitespace
    idx_str = idx_str.strip()

    # handle just single digit
    if idx_str.isdigit():
        idxs = [int(idx_str)]
    
    # Split by the commas
    idxs = []
    for string in idx_str.split(','):
        if string.isdigit():
            idxs.append(int(string))
        elif '-' in idx_str:
            [idx_begin, idx_end] = string.split('-')
            idxs.extend(list(range(int(idx_begin), int(idx_end)+1)))

    return tuple(idxs)


# Build a keyword dictionary
def format_tsk_keywords(keyword_lst):
    """ format keywords string
    """
    keyword_dct = {}
    for keyword in keyword_lst:
        [key, val] = keyword.split('=')
        keyword_dct[key] = set_value_type(val)

    return keyword_dct


def keyword_dcts_from_lst(secs_dct):
    """ a
        (
            (section_name, section_str),
            
    """

    if secs_dct is not None:
        for key, val in secs_dct.items():
            secs_dct[key] = keyword_dct_from_string(val)

    return secs_dct


def keyword_dct_from_string(section_str):
    """ Take a section with keywords defined and build
        a dictionary for the keywords
    """

    if section_str is not None:
        key_dct = {}
        section_str = ioformat.remove_whitespace(section_str)
        for line in section_str.splitlines():
            print('line')
            key_val = apf.first_capture(KEYWORD_KEYVALUE_PATTERN, line)
            formtd_key, formtd_val = format_param_vals(key_val)
            key_dct[formtd_key] = formtd_val
    else:
        key_dct = None

    return key_dct


def keyword_lst(section_str):
    """ build lst
    """

    _keyword_lst = []
    section_str = ioformat.remove_whitespace(section_str)
    for line in section_str.splitlines():
        _keyword_lst.append(line)

    return tuple(_keyword_lst)


def build_vals_lst(section_str):
    """ build lst
    """
    val_lst = []
    section_str = ioformat.remove_whitespace(section_str)
    for line in section_str.splitlines():
        val_lst.extend((float(val) for val in line.split()))

    return val_lst


# Formats the values associated with various keywords
def format_param_vals(pvals):
    """ format param vals string
    """
    [keyword, value] = pvals

    frmtd_keyword = keyword.strip().lower()

    value = value.strip()
    # Format values if it is a list (of string(s), boolean(s), int(s))
    if all(sym in value for sym in ('[[', ']]')):
        value = value.replace('D', '').replace('d', '')
        value = ast.literal_eval(value)
        frmtd_value = []
        for sub_lst in value:
            assert all(isinstance(val, int) for val in sub_lst)
            frmtd_value.append(['D{}'.format(val) for val in sub_lst])
    elif all(sym in value for sym in ('[', ']')):
        value = value.replace('[', '').replace(']', '')
        value = value.split(',')
        frmtd_value = []
        # Set string in list to boolean or integer if needed
        for elm in value:
            elm = elm.strip()
            if ':' in elm:
                elm_lst = elm.split(':')
                frmtd_value.append([float(elm_lst[0]), elm_lst[1]])
            else:
                frmtd_value.append(set_value_type(elm))
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

    return frmtd_value
