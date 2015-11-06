# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import requests
import unittest
try:
    from http import server as BaseHTTPServer
except ImportError:
    import BaseHTTPServer

from testmonkey import MonkeyServer


class TestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

        self.wfile.write(b'test GET data')

    def do_POST(self):
        self.send_response(405)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

        self.wfile.write(b'test POST data')


class TestServer(unittest.TestCase):
    def test_get(self):
        with MonkeyServer(TestHandler) as (addr, port):
            url = 'http://{}:{}'.format(addr, port)
            response = requests.get(url)

            self.assertEqual(200, response.status_code)
            self.assertEqual('text/html', response.headers['Content-Type'])
            self.assertEqual(b'test GET data', response.content)

    def test_post(self):
        with MonkeyServer(TestHandler) as (addr, port):
            url = 'http://{}:{}'.format(addr, port)
            response = requests.post(url)

            self.assertEqual(405, response.status_code)
            self.assertEqual('text/html', response.headers['Content-Type'])
            self.assertEqual(b'test POST data', response.content)


if __name__ == '__main__':
    unittest.main()
