# vim: ft=python:fenc=utf-8:tw=72:fdm=indent:nowrap
# -*- coding: utf-8 -*-
"""
    pynfact.meta
    ~~~~~~~~~~~~

    Meta information retrival from markdown post file.

    Meta fields are set in English, Catalan, Galician, Spanish and
    Portuguese although there cannot be any accent in the field names,
    so "título" has to be "titulo" in order to work properly.

    There may be accents in field values (UTF-8 by default) but not in
    field names.

    :copyright: (c) 2012, A. Romero
    :license: 3-clause license ("Modified BSD License")
"""
from dateutil.parser import parse
import re
import datetime
import markdown #only for summary in safe mode


class Meta:
    """Meta information retriver.

    .. todo: Use a more Pythonic code
    """

    def __init__(self, meta):
        """Intializer.

        :param meta: Meta information
        :type meta: list
        """
        self.meta = meta


    def author(self):
        """Gets the author as a string from post meta information.

        :return: Author field
        :rtype: str
        """
        authors = self.meta.get('authors') or self.meta.get('author') or \
                  self.meta.get('autores') or self.meta.get('autors') or \
                  self.meta.get('autor')
        return ', '.join(authors) if authors else ''


    def title(self):
        """Gets post title as a string from post meta information.

        :return: Title field
        :rtype: str
        """
        title = self.meta.get('title') or self.meta.get('titulo')  or \
                self.meta.get('entry') or self.meta.get('entrada') or \
                self.meta.get('titol') or self.meta.get('post')
        #return ''.join(title) if title else ''
        fmttitle = markdown.markdown(' '.join(title) if title else '',
                safe_mode=False) #use this carefully
        return re.sub(r'</*(p|br)[^>]*?>', '', fmttitle)


    def summary(self):
        """Gets post summary as a string from post meta information.

        :return: Summary field
        :rtype: str
        """
        summary = self.meta.get('summary') or self.meta.get('resumo') or \
                  self.meta.get('resumen') or self.meta.get('resum')
        fmtsummary = markdown.markdown(' '.join(summary) if summary else '',
                safe_mode=False) #use this carefully
        return re.sub(r'</*(p|br)[^>]*?>', '', fmtsummary)


    def date_info(self):
        """Gets post date as a datetime object.

        :return: Date field
        :rtype: datetime
        """
        date = self.meta.get('date') or self.meta.get('data') or \
               self.meta.get('fecha')
        return parse(''.join(date)) if date else ''


    def date(self, date_format='%c'):
        """Gets post date as a string.

        :param date_format: Date locale
        :type date_format: str
        :return: Date field
        :rtype: str
        """
        return self.date_info().strftime(date_format) \
               if self.date_info() else ''


    def comments(self):
        """Gets comments status.

        :return: True if entry has comments, or False otherwise
        :rtype: bool
        """
        comments = self.meta.get('comments')    or \
                   self.meta.get('comentarios') or \
                   self.meta.get('comentaris')  or ['']
        com_bool = False if comments[0].lower() == "no" or \
                            comments[0].lower() == "non"  or \
                            comments[0].lower() == "não"    \
                         else True
        return com_bool


    def private(self):
        """Gets private status.

        :return: True if entry is private, or False otherwise
        :rtype: bool
        """
        private = self.meta.get('private') or \
                  self.meta.get('privado') or self.meta.get('privat') \
                  or ['']
        piv_bool = True if private[0].lower() == "yes" or \
                           private[0].lower() == "si"  or \
                           private[0].lower() == "sí"  or \
                           private[0].lower() == "sim"    \
                        else False
        return piv_bool


    def tag_list(self):
        """Gets the tags as a list from post meta information.

        :return: List of tags
        :rtype: list
        """
        tag_list = self.meta.get('tags') or self.meta.get('etiquetas') or \
                   self.meta.get('etiquetes') or ['']
        tag_list = [x.strip() for x in tag_list[0].split(',') if x.strip()]
        return tag_list if tag_list else []


    def tags(self):
        """Gets the tags as a list from post meta information.

        :return: List of tags
        :rtype: str
        """
        return ', '.join(tag_list(self.meta)) if tag_list(self.meta) else ''

