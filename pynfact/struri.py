# vim: ft=python:fenc=utf-8:tw=72:fdm=indent:nowrap
# -*- coding: utf-8 -*-
"""
    pynfact.struri
    ~~~~~~~~~~~~~~

    URI strings manipulation functions.

    :copyright: (c) 2012, A. Romero
    :license: 3-clause license ("Modified BSD License")
"""
import unidecode
import re
import os


def slugify(unslugged):
    """Slugs a string or a a list, nothing more.
    """
    if type(unslugged) == list:
        rlist = list()
        for unslug in unslugged:
            rlist.append(unidecode.unidecode(unslug).lower())
            # TODO :: Apply `re.sub(...` to all members of the list
        return rlist
    elif type(unslugged) == str:
        unslugged = unidecode.unidecode(unslugged).lower()
        return re.sub(r'\W+','-',unslugged)


def link_to(name, prefix='', makedirs=True, justdir=False):
    """Makes a link relative path in terms of the build.

    :param name: Filename with slugified name (extension will be removed)
    :type name: str
    :param prefix: Prefix directory to preppend the file (valid dir. names)
    :type prefix: str
    :param makedirs: If true make all needed dirs
    :type makedirs: bool
    :param justdir: If true return only the link dir
    :type justdir: bool
    :return: Link path to a 'index.html' page
    :rtype: str
    """
    dirname = os.path.splitext(name)[0]
    path = os.path.join(prefix, slugify(dirname), 'index.html')
    if makedirs:
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
    return os.path.dirname(path) if justdir else path


def strip_html_tags(text):
    """Strips HTML tags in string.
    """
    return re.sub('<[^<]+?>', '', text)

