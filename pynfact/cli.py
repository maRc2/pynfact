#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ft=python:fenc=utf-8:tw=72:fdm=indent:nowrap
"""
    pynfact.cli
    ~~~~~~~~~~~

    The Command line interface.

    :copyright: (c) 2012, A. Romero
    :license: 3-clause license ("Modified BSD License")
"""
import os
import sys
import shutil
from yamler import Yamler#
from server import Server#
from builder import Builder#


def main():
    if len(sys.argv) >= 2:
        action = sys.argv[1]
    else:
        action = "help"

    if action == "init" or action == "new":
        real_path = os.path.dirname(os.path.realpath(__file__))
        src = os.path.join(real_path, 'initnew')
        dst = 'pynfact_blog' if len(sys.argv) < 3 else sys.argv[2]

        # create new blog structure with the default values
        try:
            shutil.copytree(src, dst)
        except OSError as exc:
            sys.stderr.write("Py'nFact: Tsk, tsk! Blog structure already exists.\n")

    elif action == "help":
        print("  $ pynfact init [<site>]  Creates new empty site")
        print("  $ pynfact build          Builds site")
        print("  $ pynfact serve          Testing server")
        print("  $ pynfact help           Displays this awesome help")

    elif action == "serve":
        port = 4000 if len(sys.argv) < 3 else int(sys.argv[2])
        server = Server(port=port, verbose=True)
        server.serve()

    elif action == "build":
        config_file = 'config.yml' if len(sys.argv) < 3 else sys.argv[2]
        config = Yamler(config_file)

        # Get config
        author = config.retrieve('author', "Nobody")
        site_name = config.retrieve('site_name', author)
        lang = config.retrieve('lang', 'en')
        locale = config.retrieve('locale', 'en_US')
        encoding = config.retrieve('encoding', 'utf-8')
        base_uri = config.retrieve('base_uri', '').strip('/')
        max_entries = config.retrieve('max_entries', 1)
        datefmt_long = config.retrieve('datefmt_long', '%c')
        datefmt_short = config.retrieve('datefmt_short', '%Y-%m-%d')
        datefmt_mini  = config.retrieve('datefmt_mini', '%Y-%m-%d')
        disqus = True if config.retrieve('disqus') else False
        canonical_uri = config.retrieve('canonical_uri').rstrip('/')
        extra_dirs = config.retrieve('extra_dirs')
        feed_format = config.retrieve('feed_format')
        site_description = config.retrieve('site_description')

        # Prepare builder
        template_values = { 'blog': { 'lang': lang, 'encoding': encoding,
            'site_name' : site_name, 'base_uri': base_uri,
            'author': author, 'disqus': disqus } }
        deploy_dir = '_build'

        # Build
        b = Builder(canonical_uri, base_uri, deploy_dir,
                template_values, locale, encoding, max_entries,
                datefmt_long, datefmt_short, datefmt_mini,
                extra_dirs, site_name=site_name,
                site_description=site_description, site_author=author,
                feed_format=feed_format, infile_ext='.mkdn',
                verbose=True)
        b.gen_site()


## MAIN?
if __name__ == "__main__":
    main()

