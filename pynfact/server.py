# -*- coding: utf-8 -*-
"""
    pynfact.server
    ~~~~~~~~~~~~~~

    Simple server for testing purposes.

    :copyright: (c) 2012, A. Romero
    :license: 3-clause license ("Modified BSD License")
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys
import os


class Server:
    """Simple server."""

    def __init__(self, host='127.0.0.1', port=4000, path='_build',
            verbose=True):
        """Constructor."""
        self.port = port
        self.host = host
        self.path = path
        self.verbose = verbose


    def serve(self):
        """Serves in a specific directory and waits until keyboard
           interrupt.
        """
        os.chdir(self.path)
        httpd = HTTPServer((self.host, self.port), SimpleHTTPRequestHandler)
        if self.verbose:
            print("Serving", self.host, self.port, "at", self.path)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            if self.verbose:
                sys.stderr.write("Interrupted")

