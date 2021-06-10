""" Output collection module
"""

from io import StringIO
import sys


class Capturing(list):
    """ Class captures standard output from function or modlue
    """

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


if __name__ == '__main__':
    with Capturing() as output:
        print('hello world')
    print('displays on screen')
    with Capturing(output) as output:  # note constructor argument
        print('hello world2')
    print('done')
    print('output:', output)
