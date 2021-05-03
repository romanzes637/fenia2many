import os
import re
import time


class BaseObject(object):
    def __init__(self, path):
        self.path = path

    def header(self, cls='default'):
        header = \
            '/*--------------------------------*- C++ -*----------------------------------*\\\n' \
            '                                  OpenFENIA                                    \n' \
            '\*---------------------------------------------------------------------------*/\n' \
            'FeniaFile\n' \
            '{{\n' \
            '    version     2.0;\n' \
            '    format      ascii;\n' \
            '    class       {};\n' \
            '    location    "{}";\n' \
            '    object      {};\n' \
            '}}\n' \
            '// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n'.format(
                cls, os.path.dirname(self.path), os.path.basename(self.path))
        return header

    @staticmethod
    def footer():
        footer = '// ************************************************************************* //\n'
        return footer

    def is_exists(self):
        return os.path.exists(os.path.relpath(self.path))

    def read_data(self, clear_data=True):
        """
        Read data from self.path. Skip header. Remove footer.
        :param bool clear_data: data file doesn't have comments
        :return: list data
        """
        # Skip header
        n_header_lines = 0
        with open(os.path.relpath(self.path)) as f:
            is_fenia_file = False
            for line in f:
                stripped_line = line.strip()
                if stripped_line in ['FeniaFile', 'FoamFile', 'FemFile']:
                    is_fenia_file = True
                if is_fenia_file and stripped_line == '}':
                    is_fenia_file = False
                    n_header_lines += 2  # this line + header bottom line
                    break
                n_header_lines += 1
        # Read data
        data = list()
        if clear_data:
            data_with_footer = list()
            with open(os.path.relpath(self.path)) as f:
                for i in range(n_header_lines):  # skip header
                    next(f)
                for line in f:
                    stripped_line = line.strip()
                    tokens = re.split('[\s(){};]', stripped_line)
                    filtered_tokens = filter(None, tokens)
                    data_with_footer.extend(filtered_tokens)
            data = data_with_footer[:-3]  # remove footer
        else:
            with open(os.path.relpath(self.path)) as f:
                for i in range(n_header_lines):  # skip header
                    next(f)
                is_multi_line_comment = False
                for line in f:
                    stripped_line = line.strip()
                    if stripped_line.startswith('/*'):
                        is_multi_line_comment = True
                    if stripped_line.endswith('*/'):
                        is_multi_line_comment = False
                        continue
                    if not stripped_line.startswith('//') and not is_multi_line_comment:
                        tokens = re.split('[\s(){};]', stripped_line)
                        if '//' in tokens:  # line comment at the end of line
                            index = tokens.index('//')
                            sliced_tokens = tokens[:index]
                            filtered_tokens = filter(None, sliced_tokens)
                        else:
                            filtered_tokens = filter(None, tokens)
                        data.extend(filtered_tokens)
        return data

    def write(self):
        with open(self.path, 'w') as f:
            f.write(self.header())
            f.write(self.footer())
