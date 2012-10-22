Py'nFact
========

Blog-oriented static web generator

* Features
  * Input format: Markdown
  * Output format: HTML 5
  * Jinja2 templates
  * `gettext` locale support

* Requirements
  * Python 3
  * Markdown.... Python implementation of Markdown.
  * PyRSS2Gen... A Python library for generating RSS 2.0 feeds.
  * pyatom...... A Python library for generating Atom 1.0 feeds.
  * Unidecode... ASCII transliterations of Unicode text
  * Jinja2...... A small but fast and easy to use stand-alone
                 template engine written in pure python.

Why this name?
--------------

*pyblog*, *pyblic*, *pyweblog* were taken.
Granted it will be used on the "web", the word "log" in Latin may be
translated as *INdicem FACTorum*, hence *InFact* or **'nFact** to be
easily pronounceable when adding the prefix *py-*.

First notes
-----------

This project is in development, so there are some features that are
not working yet, such as the *Disqus* capability. Other than that, the
only thing it lacks deploy it as a package.

Installation
------------

There isn't an installer by now.

First usage
-----------

Typing `python pynfact/cli.py init <site>` or `python pynfact/cli.py
new <site>` the site skeleton is generated with the static content (CSS
and Javascript), the `posts` directory, and the `templates`
directory, where the site main layout is in Jinja format. Also the
configuration file `config.yml` is generated.

Everything (build, serve) may be done with `pynfact/cli.py`, but a
`Makefile` easier to deal with. Type `make help` after the creating
the site for more hints, or edit the `Makefile` to suit your needs.

Configuration
-------------

Configuration relays only on `config.yml` file. Some of the valid
fields are:

 * `author`: Author of the personal blog

 * `disqus`: Uses comments engine  *disqus* if is set to "yes"

 * `locale`: Locale config. By default is set to "en\_US"

 * `lang`: Language of the generated site (hyphens,...) Default: "en"

 * `canonical_uri`: Blog URI: "http://...".

 * `max_entries`: Maximum number of entries by page in posts list

 * `extra_dirs`: List of directories that will be copied to the
                 deploy directory. It has to be a list.

Site generation
---------------

Type `python pynfact/cli.py build` (or `make build`) to build the
site. The static content will be dropped on `_build`.


Post creation
-------------

Every entry is stored in the directory `posts`, in Markdown format
and mandatory extension `.mkdn`. The metadata is the header of the
file and it has some mandatory fields such as "Title" and "Date".

An example of metadata header:

    Title: Post title
    Summary: A *simple* summary for this entry.
    Tags: tag1, tagtwo, tag three, Four
    Date: 2012/12/21 21:55 CEST
    Comments: No
    Private: No

### Metadata

Title and date are mandatory fields.

The summary is only shown in the main posts list.

Date may be in several formats, but in order to avoid ambiguity it
should be specified in "yyyy/mm/dd" or "yyyy-mm-dd" formats. Time and
timezone are also options. If not timezone, UTC assumed. If not time:
00:00 assumed.

The "Private" field is optional and set to "no" by default. Every entry
is public unless this tag is set to "yes".

Private pages are created just the same as public ones, but they are
not listed. If you want not to generate a page, just change its
extension to something different that `.mkdn`.

By default every entry allows comments. To block comments to any entry
just set the "Comments" tag to "No". This tag is also optional.

To block comments in every post, set the flag `disqus: no` in the
`config.yml` file. In this case, the comments tag in the metadata is
always ignored even if explicitly says "yes".

Pages
-----

Pages are Markdown files with `.mkdn` extension on the same level as
the configuration file. The only metadata they need is the Title. The
other ones are ignored.

Other than that are the same as regular posts.

Links to this pages are not automatic. You have to edit the template
code to add the link to your own pages. A nice place to add this links
could be the top navigation.

Tests
-----

Just for a minimal run test, `python pynfact/cli.py server [<port>]`
(or `make serve`).

License
-------

*Py'nFact* is distributed under 3-Clause BSD (New BSD License).
More information in `LICENSE` file.

