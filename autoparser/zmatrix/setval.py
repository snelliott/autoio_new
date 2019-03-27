""" parse information from the setval block of a z-matrix
"""
from autoparse import cast as _cast
import autoparse.pattern as app
import autoparse.find as apf

NAME_PATTERN = app.VARIABLE_NAME
SETTO_PATTERN = app.escape('=')
VALUE_PATTERN = app.one_of_these([app.FLOAT, app.INTEGER])
DELIM_PATTERN = app.padded(app.NEWLINE)


def read(string,
         head_ptt=None,
         name_ptt=NAME_PATTERN,
         val_ptt=VALUE_PATTERN,
         set_ptt=SETTO_PATTERN,
         prefix_ptt=None,
         suffix_ptt=None,
         delim_ptt=DELIM_PATTERN):
    """ read setvalues from a string
    """
    entry_ptt_ = entry_pattern(
        name_ptt=app.capturing(name_ptt),
        val_ptt=app.capturing(val_ptt),
        set_ptt=set_ptt, prefix_ptt=prefix_ptt, suffix_ptt=suffix_ptt)
    block_ptt = block_pattern(
        name_ptt=name_ptt, val_ptt=val_ptt, set_ptt=set_ptt,
        prefix_ptt=prefix_ptt, suffix_ptt=suffix_ptt, delim_ptt=delim_ptt)
    block_ptt_ = app.capturing(block_ptt)

    if head_ptt is not None:
        block_ptt_ = head_ptt + block_ptt_

    block_str = apf.last_capture(block_ptt_, string)
    caps = apf.all_captures(entry_ptt_, block_str)
    names, vals = zip(*_cast(caps))
    return names, vals


def block_pattern(name_ptt=NAME_PATTERN,
                  val_ptt=VALUE_PATTERN,
                  set_ptt=SETTO_PATTERN,
                  prefix_ptt=None,
                  suffix_ptt=None,
                  delim_ptt=DELIM_PATTERN):
    """ a single setvalue entry
    """
    entry_ptt = entry_pattern(
        name_ptt=name_ptt,
        val_ptt=val_ptt,
        set_ptt=set_ptt,
        prefix_ptt=prefix_ptt,
        suffix_ptt=suffix_ptt,
    )
    block_ptt = app.series(entry_ptt, app.padded(delim_ptt))
    return block_ptt


def entry_pattern(name_ptt=NAME_PATTERN,
                  val_ptt=VALUE_PATTERN,
                  set_ptt=SETTO_PATTERN,
                  prefix_ptt=None,
                  suffix_ptt=None):
    """ a single setvalue entry
    """
    parts = [name_ptt, set_ptt, val_ptt]

    if prefix_ptt is not None:
        parts.insert(0, prefix_ptt)

    if suffix_ptt is not None:
        parts.append(suffix_ptt)

    ptt = app.padded(app.LINESPACES.join(parts))
    return ptt


if __name__ == '__main__':
    STR1 = """
    A2        =   96.7725720000
    D3        =  129.3669950000
    R1        =    1.4470582953
    R2        =    0.9760730000
"""

    STR2 = """
                       ----------------------------
                       !   Optimized Parameters   !
                       ! (Angstroms and Degrees)  !
 ----------------------                            ----------------------
 !      Name          Value   Derivative information (Atomic Units)     !
 ------------------------------------------------------------------------
 !       R1          1.4057   -DE/DX =    0.0                           !
 !       R2          0.9761   -DE/DX =    0.0628                        !
 !       A2         96.7726   -DE/DX =    0.0552                        !
 !       D3        129.367    -DE/DX =    0.0019                        !
 ------------------------------------------------------------------------
 GradGradGradGradGradGradGradGradGradGradGradGradGradGradGradGradGradGrad
"""

    STR3 = """
R1  = 2.73454  
R2  = 1.84451   A2  = 96.7726  
R3  = 1.84451   A3  = 96.7726   D3  = 129.367        
"""

    VALS1 = read(STR1)
    print(VALS1)

    VALS2 = read(
        STR2,
        name_ptt=NAME_PATTERN,
        val_ptt=VALUE_PATTERN,
        set_ptt='',
        prefix_ptt=app.escape('!'),
        suffix_ptt=app.LINESPACES.join([
            app.escape('-DE/DX ='), app.FLOAT, app.escape('!')]))
    print(VALS2)

    VALS3 = read(
        STR3,
        delim_ptt=app.one_of_these(['', app.NEWLINE]))
    print(VALS3)
