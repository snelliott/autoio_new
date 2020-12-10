""" gradient and hessian readers
"""
import numpy
import autoread as ar
import autoparse.pattern as app
import autoparse.find as apf


def gradient(output_string):
    """ read gradient from the output string
    """

    # Grab a block of text containing the gradient
    block_ptt = ('Molecular gradient' +
                 app.capturing(app.one_or_more(app.WILDCARD, greedy=False)) +
                 'Molecular gradient norm')
    block = apf.last_capture(block_ptt, output_string)

    # Trim the block to start it at the gradient lines
    blank_count = 0
    for i, line in enumerate(block.splitlines()):
        if line.strip() == '':
            blank_count += 1
            if blank_count == 3:
                grad_start = i
                break
    trim_block = '\n'.join(block.splitlines()[grad_start:])

    # Grab the gradient from the trimmed block string
    grad = ar.matrix.read(
        trim_block,
        line_start_ptt=app.LINESPACES.join([
            app.LETTER,
            app.escape('#') + app.UNSIGNED_INTEGER,
            app.maybe(app.UNSIGNED_INTEGER)]))
    print(grad)
    assert numpy.shape(grad)[1] == 3
    return grad
# def hessian(output_string):
#     """ read hessian from the output string
#     """
#     try:
#         comp_ptt = app.one_of_these(['X', 'Y', 'Z']) + app.UNSIGNED_INTEGER
#         mat = ar.matrix.read(
#             output_string,
#             start_ptt=(app.escape('The second derivative matrix:') +
#                        app.lpadded(app.NEWLINE)),
#             block_start_ptt=(app.series(comp_ptt, app.LINESPACES) +
#                              app.padded(app.NEWLINE)),
#             line_start_ptt=comp_ptt,
#             tril=True)
#     except TypeError:
#         comp_ptt = app.UNSIGNED_INTEGER
#         mat = ar.matrix.read(
#             output_string,
#             val_ptt=app.EXPONENTIAL_FLOAT_D,
#             start_ptt=(
#                 app.escape('Force constants in Cartesian coordinates:') +
#                 app.lpadded(app.NEWLINE)),
#             block_start_ptt=(app.series(comp_ptt, app.LINESPACES) +
#                              app.padded(app.NEWLINE)),
#             line_start_ptt=comp_ptt,
#             tril=True)
#
#         mat = [[_cast(apf.replace('d', 'e', dst, case=False)) for dst in row]
#                for row in mat]
#
#     mat = tuple(map(tuple, mat))
#     return mat
