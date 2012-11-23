# vim: ft=python:fenc=utf-8:tw=72:fdm=indent:nowrap
# -*- coding: utf-8 -*-
"""
    pynfact.builder
    ~~~~~~~~~~~~~~~

    Builds the content.

    Only markdown files will be taken, but a markdown file are
    identified by its extension, which for this application is
    ``.mkdn``. I'm trying to avoid ``.md`` for ambiguity reasons.

    :copyright: (c) 2012, A. Romero
    :license: 3-clause license ("Modified BSD License")
"""
from jinja2 import Environment, FileSystemLoader, Markup
import PyRSS2Gen as RSS2
from pyatom import AtomFeed
import codecs
import gettext
import locale
from math import ceil
from datetime import datetime
from struri import slugify, link_to, strip_html_tags#
from meta import Meta#
from mulang import Mulang#
import shutil
import os


class Builder:
    """Site building process manager.
    
    .. todo:: Remove redundant code using a universal method for
              retrieve and gather the data; and use subclasses.

    .. todo:: Manage better with timezones. Make sure if there is no
              timezone the default is always UTC, for posts info, and
              both feeds pub. dates.

    .. todo:: Fix the way the variables are passed on the init. Grouping
              by lists or dictionaries could simplify much the
              constructor.

              i.e.:

              uri [ 'canonical': 'http://where.my_site.is/', 'base': '' ]
              wlocale = [ 'locale': "utf-8", 'encoding': "en_US" ]
              date_fmts = [ 'long': "%c", 'short': '%Y-%M-%D', 'mini': "%B, %Y",
              site = [ 'name': "My Blog", 'description': "Nice description.",
                       'author': "Me", 'max_entries': "10", 'feed_fmt': "atom"]

              def __init__(self, uri, wlocale, site, date_fmts,
                           template_values, extra_dirs, infile_ext,
                           verbose=True):
    """

    def __init__(self, canonical_uri, base_uri='', deploy_dir='_build',
            template_values=dict(), wlocale='en_US', encoding='utf-8',
            max_entries=10, date_format_entries='%c',
            date_format_list='%Y-%m-%d', date_format_home='%Y-%m-%d',
            extra_dirs=None, site_name='', site_description='Feed',
            site_author='', feed_format='atom', infile_ext='.mkdn',
            verbose=True):
        """Constructor.

        :param template_values: Common values in all templates
        :type template_values: dict
        :param wlocale: Working locale; locale of the generated site
        :type wlocale: str
        """
        self.max_entries = max_entries
        self.template_values = template_values
        self.wlocale = wlocale
        self.encoding = encoding
        self.base_uri = base_uri
        self.deploy_dir = os.path.join(deploy_dir, base_uri)
        self.date_format_list = date_format_list
        self.date_format_entries = date_format_entries
        self.date_format_home = date_format_home
        self.canonical_uri = canonical_uri
        self.site_name = site_name
        self.site_author = site_author
        self.feed_format = feed_format
        self.site_description = site_description
        self.extra_dirs = extra_dirs
        self.infile_ext = infile_ext
        self.verbose = verbose

        # Set locale for the site.
        self.old_locale = locale.getlocale()
        self.current_locale = locale.setlocale(locale.LC_ALL,
                self.wlocale)

        # Constants-like (I don't like this approach)
        #source dirs.
        self_dir = os.path.dirname(os.path.realpath(__file__))
        self.locale_dir = os.path.join(self_dir, 'locale')
        self.builtin_templates_dir = os.path.join(self_dir, 'templates')

        #dest. dirs.
        self.home_cont_dir = 'page'      # home paginator
        self.tags_dir = 'tags'           # one dir. per tag

        #src. & dest. dirs.
        self.pages_dir = '.'             # other pages such as 'About'
        self.entries_dir = 'posts'       # where posts are
        self.static_dir = 'static'       # CSS and JS
        self.templates_dir = 'templates' # Layout base template


    def __del__(self):
        """Destructor."""
        # Restores locale
        return locale.setlocale(locale.LC_ALL, self.old_locale)


    def render_template(self, template, output_data, values):
        """Renders a template using Jinja2.

        :param template: Template to use
        :type template: str
        :param output_data: File where the data is saved
        :type output_data: str
        :return: Generated HTML of the output data
        :rtype: str
        """
        trans = gettext.translation('default', self.locale_dir,
                [self.current_locale]) # locale has to be set!
        env = Environment(extensions=['jinja2.ext.i18n'],
                loader=FileSystemLoader([self.templates_dir,
                    self.builtin_templates_dir]))
        env.install_gettext_translations(trans)
        env.globals['slugify'] = slugify # <- adds `slugify` to Jinja2
        env.globals['strip_html_tags'] = strip_html_tags
        template = env.get_template(template)
        html = template.render(**values)
        output_file = codecs.open(output_data, mode="w",
                encoding=self.encoding)
        output_file.write(html)

        return html


    def entry_link_prefix(self, entry):
        """Compute entrie final path."""
        meta = Meta(Mulang(os.path.join(self.entries_dir, entry),
            self.encoding).metadata())
        date = meta.date('%Y-%m-%d')
        date_arr = date.split('-')
        path = os.path.join(str(self.entries_dir),
                            str(date_arr[0]),
                            str(date_arr[1]),
                            str(date_arr[2]))
        return path


    def gen_entry(self, infile, date_format='%c'):
        """Generate a HTML entry from its Mardkdown counterpart.

        :param infile: Markdown file to parse
        :type infile: str
        :param date_format: Date format for entry
        :type date_format: str
        :return: Generated HTML
        :rtype: str
        """
        inpath = os.path.join(self.entries_dir, infile)
        ml = Mulang(inpath, self.encoding)
        meta = Meta(ml.metadata())
        content_html = ml.html(verbose=self.verbose)

        timezone = meta.date('%z')
        if timezone:
            # to html5 timezone conv.
            timezone = timezone[:3] + ':' + timezone[3:]
        datehtml = meta.date('%Y-%m-%dT%H:%M') + timezone

        values = self.template_values.copy()
        values['entry'] = { #append
                  'title': meta.title(),
                  'raw_title': strip_html_tags(meta.title()),
                  'private': meta.private(),
                  'comments': meta.comments(),
                  'date': meta.date(date_format),
                  'datehtml': datehtml,
                  'tags': meta.tag_list(),
                  'content': content_html }
        outfile = link_to(slugify(strip_html_tags(meta.title())),
                os.path.join(self.deploy_dir,
                    self.entry_link_prefix(infile)))
        return self.render_template('entry.html.j2', outfile, values)


    def gen_entries(self, date_format='%c'):
        """Generate all entries.

        :param date_format: Date format for entry
        :type date_format: str
        """
        for filename in os.listdir(self.entries_dir):
            if os.path.splitext(filename)[1] == self.infile_ext:
                self.gen_entry(filename, date_format=date_format)


    def gen_home(self, max_entries_per_page=10, date_format='%Y-%m-%d'):
        """Generate home page, and subpages.

        :param max_entries: Max. entries per page
        :type max_entries: int
        :param date_format: Date format for home page
        :type date_format: str
        """
        entries = list()
        total_entries = 0
        for filename in os.listdir(self.entries_dir):
            if os.path.splitext(filename)[1] == self.infile_ext:
                inpath = os.path.join(self.entries_dir, filename)
                meta = Meta(Mulang(inpath, self.encoding).metadata())

                private = meta.private()
                title = meta.title()
                summary = meta.summary()
                date = meta.date(date_format)
                date_idx = meta.date('%Y-%m-%d %H:%M:%S')
                uri = link_to(slugify(strip_html_tags(title)),
                        self.entry_link_prefix(filename),
                        makedirs=False, justdir=True)

                # Generate archive
                if not private:
                    total_entries += 1
                    val = { 'title': title, 'summary': summary,
                            'date': date, 'date_idx': date_idx,
                            'uri': uri }
                    entries.append(val)

        # Sort chronologically descent
        entries = sorted(entries, key=lambda k: k['date_idx'],
                reverse=True)

        total_pages = ceil(total_entries / max_entries_per_page)
        values = self.template_values.copy()

        # FIXME :: Merge this scenario with the following loop
        #Generate 'index.html' even when there are no posts
        if total_entries == 0:
            outfile = link_to('', self.deploy_dir)
            self.render_template('entries.html.j2', outfile, values)

        # Home page (and subsequent ones)
        for cur_page in range(1, total_pages + 1):
            min_page = (cur_page - 1) * max_entries_per_page
            max_page = cur_page * max_entries_per_page

            values['entries'] = entries[min_page:max_page]
            values['cur_page'], values['total_pages'] = cur_page, total_pages

            if cur_page == 1:
                # the home page, the "index.html" of the site
                outfile = link_to('', self.deploy_dir)
            else:
                # subsequent pages other that the first
                outfile = link_to(str(cur_page),
                        os.path.join(self.deploy_dir,
                            self.home_cont_dir))
            self.render_template('entries.html.j2', outfile, values)
            values['entries'] = {} # reset the entries dict.


    def gen_archive(self, date_format='%c'):
        """Generate complete archive.

        :param date_format: Date format for entry
        :type date_format: str
        """
        archive = dict()
        for filename in os.listdir(self.entries_dir):
            if os.path.splitext(filename)[1] == self.infile_ext:
                post = os.path.join(self.entries_dir, filename)
                meta = Meta(Mulang(post, self.encoding).metadata())

                private = meta.private()
                title = meta.title()
                #summary = meta.summary()
                date = meta.date(date_format)
                date_info = meta.date_info()
                date_idx = meta.date('%Y-%m-%d')
                comments = meta.comments()
                uri = link_to(slugify(title),
                        self.entry_link_prefix(filename),
                        makedirs=False, justdir=True)

                # Generate archive
                if not private:
                    val = { 'uri': uri, 'title': title, 'date': date,
                            'date_idx': date_idx,
                            'comments': comments }
                    d = datetime.strptime(meta.date('%Y-%m-%d'), '%Y-%m-%d')
                    idx_year  = d.strftime('%Y')
                    idx_month = d.strftime('<%m> %B')#%m is to sort chronologically
                    if idx_year in archive:
                        if idx_month in archive[idx_year]:
                            archive[idx_year][idx_month].append(val)
                        else:
                            archive[idx_year][idx_month] = [val]
                        #sort entries
                        archive[idx_year][idx_month] = sorted(archive[idx_year][idx_month], key=lambda k: k['date_idx'])
                    else:
                        archive[idx_year] = dict()
                        archive[idx_year][idx_month] = [val]

        values = self.template_values.copy()
        values['archive'] = archive
        outfile = link_to('archive.html', self.deploy_dir)
        return self.render_template('archive.html.j2', outfile, values)


    def gen_tags(self, date_format='%c'):
        """Generate tags pages.

        :param date_format: Date format for entry
        :type date_format: str
        """
        entries_by_tag = dict()
        for filename in os.listdir(self.entries_dir):
            if os.path.splitext(filename)[1] == self.infile_ext:
                post = os.path.join(self.entries_dir, filename)
                meta = Meta(Mulang(post, self.encoding).metadata())

                private = meta.private()
                title = meta.title()
                summary = meta.summary()
                tag_list = meta.tag_list()
                date = meta.date(date_format)
                date_idx = meta.date('%Y-%m-%d')
                uri = link_to(slugify(title),
                        self.entry_link_prefix(filename),
                        makedirs=False, justdir=True)

                # Generate archive
                if not private:
                    val = { 'uri': uri, 'title': title, 'date': date,
                            'date_idx': date_idx }
                    for tag in tag_list:
                        if tag in entries_by_tag:
                            entries_by_tag[tag].append(val)
                        else:
                            entries_by_tag[tag] = [val]

        # One page for each tag
        values = self.template_values.copy()
        for tag in entries_by_tag:
            values['tag_name'] = tag
            values['entries'] = entries_by_tag[tag]
            #sort entries
            values['entries'] = sorted(values['entries'], key=lambda k:
                    k['date_idx'], reverse=True)
            outfile = link_to(tag, os.path.join(self.deploy_dir, self.tags_dir))
            self.render_template('tag.html.j2', outfile, values)


    def gen_tag_cloud(self):
        """Generate tags cloud page."""
        entries_by_tag = dict()
        for filename in os.listdir(self.entries_dir):
            if os.path.splitext(filename)[1] == self.infile_ext:
                post = os.path.join(self.entries_dir, filename)
                meta = Meta(Mulang(post, self.encoding).metadata())
                private = meta.private()
                title = meta.title()
                tag_list = meta.tag_list()

                # Generate archive
                if not private:
                    val = { 'title': title }
                    for tag in tag_list:
                        if tag in entries_by_tag:
                            entries_by_tag[tag].append(val)
                        else:
                            entries_by_tag[tag] = [val]

        # multipliers seq. for tag size in function of times repeated
        tagcloud_seq = [ 0, 14, 21, 27, 32, 38, 42, 45, 47, 48 ]

        # One page for each tag
        values = self.template_values.copy()
        values['tags'] = []
        for tag in entries_by_tag:
            if tag:
                tagname, tagfreq =  tag, len(entries_by_tag[tag])
                mult = 100 + int(tagcloud_set.last \
                        if tagfreq > len(tagcloud_seq) \
                        else tagcloud_seq[tagfreq - 1])
                values['tags'].append({ tagname: mult })

        outfile = link_to('', os.path.join(self.deploy_dir, self.tags_dir))
        self.render_template('tagcloud.html.j2', outfile, values)


    def gen_page(self, infile):
        """Generate a HTNL page from its Mardkdown counterpart.

        :param infile: Markdown file to parse
        :type infile: str
        :return: Generated HTML
        :rtype: str
        """
        inpath = os.path.join(self.pages_dir, infile)
        ml = Mulang(inpath, self.encoding)
        meta = Meta(ml.metadata())
        content_html = ml.html(verbose=self.verbose)
        values = self.template_values.copy()
        values['page'] = { #append
                'title': meta.title(),
                'raw_title': strip_html_tags(meta.title()),
                'content': content_html }

        outfile = link_to(infile, os.path.join(self.deploy_dir,
            self.pages_dir))
        return self.render_template('page.html.j2', outfile, values)


    def gen_pages(self):
        """Generate all pages."""
        for filename in os.listdir(self.pages_dir):
            if os.path.splitext(filename)[1] == self.infile_ext:
                self.gen_page(filename)


    def gen_feed(self, feed="atom"):
        if feed == "rss":
            self.gen_feed_rss()
        else:
            self.gen_feed_atom()


    def gen_feed_atom(self, outfile='atom.xml'):
        """Generate blog Atom feed.
        """
        feed = AtomFeed(title=self.site_name if self.site_name \
                                             else self.canonical_uri,
                        subtitle=self.site_description if self.site_description
                                                       else 'Feed',
                        feed_url=os.path.join(self.canonical_uri, self.base_uri, outfile),
                        url=os.path.join(self.canonical_uri, self.base_uri),
                        author=self.site_author)

        entries = list()
        for filename in os.listdir(self.entries_dir):
            if os.path.splitext(filename)[1] == self.infile_ext:
                infile = os.path.join(self.entries_dir, filename)
                ml = Mulang(infile, self.encoding)
                meta = Meta(ml.metadata())
                author = self.site_name if not meta.author() \
                                        else meta.author()
                content_html = ml.html(verbose=False)
                private = meta.private()
                title = meta.title()
                date_idx = meta.date('%Y-%m-%d %H:%M:%S')
                timezone = 'UTC' if not meta.date('%Z') else meta.date('%Z')
                date_iso8601 = meta.date('%Y-%m-%dT%H:%M') + timezone
                updated = datetime.strptime(date_iso8601, \
                        '%Y-%m-%dT%H:%M%Z')
                uri = link_to(slugify(title),
                        self.entry_link_prefix(filename),
                        makedirs=False, justdir=True)
                full_uri = os.path.join(self.canonical_uri,
                        self.base_uri, uri)

                if not private:
                    val = { 'title': strip_html_tags(title),
                            'content_html': content_html,
                            'author': author,
                            'full_uri': full_uri,
                            'date_idx': date_idx,
                            'updated': updated }
                    entries.append(val)

        # sort chronologically descent
        entries = sorted(entries, key=lambda k: k['date_idx'],
                reverse=True)
        for entry in entries:
            feed.add(title = entry['title'],
                     content = entry['content_html'],
                     author = entry['author'],
                     url = entry['full_uri'],
                     updated = entry['updated'])

        output_file = codecs.open(os.path.join(self.deploy_dir, \
            outfile), mode='w', encoding=self.encoding)
        output_file.write(feed.to_string())


    def gen_feed_rss(self, outfile='feed.xml'):
        """Generate blog feed.

        .. todo: Why I cannot do this without changing the locale?
        """
        # This doesn't work in another locale, will be restored
        locale.setlocale(locale.LC_ALL, "en_US")

        entries = list()
        for filename in os.listdir(self.entries_dir):
            if os.path.splitext(filename)[1] == self.infile_ext:
                infile = os.path.join(self.entries_dir, filename)
                ml = Mulang(infile, self.encoding)
                meta = Meta(ml.metadata())
                content_html = ml.html(verbose=False)
                private = meta.private()
                title = meta.title()
                summary = meta.summary()
                date_idx = meta.date('%Y-%m-%d %H:%M:%S')
                # Date+time in RFC-822 format. fixing lack of timezone
                # when there's none (UTC by default).
                timezone = '+0000' if not meta.date('%z') \
                                   else meta.date('%z')
                pub_date = meta.date('%a, %d %b %Y %H:%M:%S') + \
                        " " + timezone
                uri = link_to(slugify(title),
                        self.entry_link_prefix(filename),
                        makedirs=False, justdir=True)
                full_uri = os.path.join(self.canonical_uri,
                        self.base_uri, uri)
                if not private:
                    val = { 'title': strip_html_tags(title),
                            'content_html': content_html,
                            #'summary': summary,
                            'full_uri': full_uri,
                            'date_idx': date_idx,
                            'pub_date': pub_date }
                    entries.append(val)

        # sort chronologically descent
        entries = sorted(entries, key=lambda k: k['date_idx'],
                reverse=True)
        for entry in entries:
            entries.append(
                    RSS2.RSSItem(
                        title = entry['title'],
                        link = entry['full_uri'],
                        #description = entry['summary'],
                        description = entry['content_html'],
                        guid = RSS2.Guid(entry['full_uri']),
                        pubDate = entry['pub_date']))

        rss = RSS2.RSS2(
                title = self.site_name if self.site_name \
                                       else self.canonical_uri,
                description = "RSS",
                link = self.canonical_uri,
                lastBuildDate = datetime.now(),
                items = entries
                )

        rss.write_xml(open(os.path.join(self.deploy_dir, outfile), 'w'),
                self.encoding)
        # Restore locale
        locale.setlocale(locale.LC_ALL, self.wlocale)


    def gen_static(self):
        """Generates (copies) static directory."""
        src = self.static_dir
        dst = os.path.join(self.deploy_dir, self.static_dir)
        if os.path.exists(src):
            shutil.rmtree(dst, ignore_errors=True)
            shutil.copytree(src, dst)


    def gen_media(self):
        """Generates media directories if they exist."""
        if self.extra_dirs:
            for extra_dir in self.extra_dirs:
                src = extra_dir
                dst = os.path.join(self.deploy_dir, extra_dir)
                if os.path.exists(src):
                    shutil.rmtree(dst, ignore_errors=True)
                    shutil.copytree(src, dst)
                    if self.verbose:
                        print('Copied directory', src)


    def gen_site(self):
        """Generate all content!.
        """
        self.gen_entries(self.date_format_entries)
        self.gen_pages()
        self.gen_archive(self.date_format_list)
        self.gen_tags(self.date_format_list)
        self.gen_tag_cloud()
        self.gen_home(self.max_entries, self.date_format_home)
        self.gen_feed(self.feed_format)
        self.gen_static()
        self.gen_media()

