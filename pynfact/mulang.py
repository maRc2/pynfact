# vim: ft=python:fenc=utf-8:tw=72:fdm=indent:nowrap
# -*- coding: utf-8 -*-
"""
    pynfact.mulang
    ~~~~~~~~~~~~~~

    Markdown translation to HTML and metadata 'getter'.

    :copyright: (c) 2012, A. Romero
    :license: 3-clause license ("Modified BSD License")
"""
import codecs
import markdown


class Mulang:
    """Generates HTML code from MarkUp LANGuage (mulang) source."""

    def __init__(self, input_data, encoding='utf-8',
            output_format='html5'):
        """
        Initializer

        :param input_data: File from where the data is taken
        :type input_data: str
        :param encoding: Encoding the input file is in
        :type encoding: str
        :param output_format: Output HTML version
        :type output: str
        """
        self.input_data = input_data
        self.encoding = encoding
        self.md = markdown.Markdown(
                extensions=['extra', 'toc', 'codehilite', 'html_tidy', 'meta'],
                encoding=encoding,
                safe_mode=False,
                output_format=output_format)


    def html(self, verbose=True):
        """Generates HTML from Markdown data.

        :param verbose: Tells what this is doing
        :type verbose: bool
        """
        input_file = codecs.open(self.input_data, mode="r", \
                encoding=self.encoding)
        text = input_file.read()
        input_file.close()
        html = self.md.convert(text)

        if verbose:
            print('Parsed', self.input_data)

        return html


    def metadata(self):
        """Gets metadata in the markdown file.

        .. todo: Get the meta without generating HTML again
        """
        input_file = codecs.open(self.input_data, mode="r", \
                encoding=self.encoding)
        text = input_file.read()
        input_file.close()
        html = self.md.convert(text)

        return self.md.Meta

