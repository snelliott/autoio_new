""" z-matrix matrix block parsers
"""
import numpy
from autoparse import cast as _cast
import autoparse.find as apf
import autoparse.pattern as app

SYM_PATTERN = app.LETTER + app.maybe(app.LETTER)
KEY_PATTERN = app.UNSIGNED_INTEGER
NAME_PATTERN = app.VARIABLE_NAME
ENTRY_SEP_PATTERN = app.LINESPACE


def read(string,
         start_ptt=None,
         sym_ptt=SYM_PATTERN,
         key_ptt=KEY_PATTERN,
         name_ptt=NAME_PATTERN,
         entry_sep_ptt=ENTRY_SEP_PATTERN,
         last=True,
         case=False):
    """ read matrix from a string
    """
    line_ptts_ = [
        line_pattern(num, app.capturing(sym_ptt), app.capturing(key_ptt),
                     app.capturing(name_ptt), entry_sep_ptt)
        for num in range(4)]

    block_ptt_ = app.capturing(block_pattern(
        sym_ptt=sym_ptt, key_ptt=key_ptt, name_ptt=name_ptt,
        entry_sep_ptt=entry_sep_ptt))

    block_ptt_ = block_ptt_ if start_ptt is None else start_ptt + block_ptt_

    block_str = (apf.last_capture(block_ptt_, string, case=case) if last else
                 apf.first_capture(block_ptt_, string, case=case))

    lines = block_str.splitlines()
    nrows = len(lines)
    syms = []
    key_mat = numpy.empty((nrows, 3), dtype=numpy.object_)
    name_mat = numpy.empty((nrows, 3), dtype=numpy.object_)
    for row_idx, line in enumerate(lines):
        ncols = min(row_idx, 3)
        caps = _cast(apf.first_capture(line_ptts_[ncols], line, case=case))
        sym = caps if ncols == 0 else caps[0]
        keys = caps[1::2]
        names = caps[2::2]

        syms.append(sym)
        key_mat[row_idx, :ncols] = keys
        name_mat[row_idx, :ncols] = names

    syms = tuple(syms)
    key_mat = tuple(map(tuple, key_mat))
    name_mat = tuple(map(tuple, name_mat))
    return syms, key_mat, name_mat


def block_pattern(sym_ptt=SYM_PATTERN,
                  key_ptt=KEY_PATTERN,
                  name_ptt=NAME_PATTERN,
                  entry_sep_ptt=ENTRY_SEP_PATTERN):
    """ matrix pattern (assumes more than one atom)
    """
    line_ptts = [line_pattern(num, sym_ptt, key_ptt, name_ptt, entry_sep_ptt)
                 for num in range(4)]

    block_end_ptt = app.series(line_ptts[3], app.NEWLINE)

    block_ptt = app.one_of_these([
        app.NEWLINE.join(line_ptts[:3] + [block_end_ptt]),
        app.NEWLINE.join(line_ptts[:3]),
        app.NEWLINE.join(line_ptts[:2]),
    ])
    return block_ptt


def line_pattern(num,
                 sym_ptt=SYM_PATTERN,
                 key_ptt=KEY_PATTERN,
                 name_ptt=NAME_PATTERN,
                 entry_sep_ptt=ENTRY_SEP_PATTERN):
    """ matrix line pattern
    """
    assert num in range(0, 4)
    return app.LINE_START + app.padded(app.padded(entry_sep_ptt).join(
        [sym_ptt] + num * [key_ptt, name_ptt]))
