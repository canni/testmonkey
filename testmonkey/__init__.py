# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from contextlib import closing
from multiprocessing import Pipe
from threading import Thread
try:
    from http import server as BaseHTTPServer
except ImportError:  # pragma: no cover
    import BaseHTTPServer


class MonkeyServer(Thread):
    def __init__(self, request_handler_class):
        self.request_handler_class = request_handler_class
        self._parent, self._child = Pipe()
        super(MonkeyServer, self).__init__()

    def run(self):
        httpd = BaseHTTPServer.HTTPServer(('localhost', 0), self.request_handler_class)
        httpd.timeout = 0.01
        with closing(self._child) as conn:
            conn.send(httpd.server_address)

            while not self._child.poll(0.01):
                httpd.handle_request()

            conn.recv()
            httpd.server_close()

    def __enter__(self):
        self.start()
        return self._parent.recv()

    def __exit__(self, exc_type, exc_val, exc_tb):
        with closing(self._parent) as conn:
            conn.send('stop')
            self.join()
