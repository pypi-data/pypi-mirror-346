import logging
import requests
import sys
import ssl

from requests.adapters import HTTPAdapter
from requests.sessions import Session
from requests_toolbelt.utils import dump

try:
    import brotli
except ImportError:
    pass

try:
    import copyreg
except ImportError:
    import copy_reg as copyreg

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

from .exceptions import (
    CloudflareLoopProtection,
    CloudflareIUAMError
)

from .cloudflare import Cloudflare
from .user_agent import User_Agent

__version__ = '1.2.73'

class CipherSuiteAdapter(HTTPAdapter):
    __attrs__ = [
        'ssl_context',
        'max_retries',
        'config',
        '_pool_connections',
        '_pool_maxsize',
        '_pool_block',
        'source_address'
    ]

    def __init__(self, *args, **kwargs):
        self.ssl_context = kwargs.pop('ssl_context', None)
        self.cipherSuite = kwargs.pop('cipherSuite', None)
        self.source_address = kwargs.pop('source_address', None)
        self.server_hostname = kwargs.pop('server_hostname', None)
        self.ecdhCurve = kwargs.pop('ecdhCurve', 'prime256v1')

        if self.source_address:
            if isinstance(self.source_address, str):
                self.source_address = (self.source_address, 0)

            if not isinstance(self.source_address, tuple):
                raise TypeError(
                    "source_address must be IP address string or (ip, port) tuple"
                )

        if not self.ssl_context:
            self.ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            self.ssl_context.orig_wrap_socket = self.ssl_context.wrap_socket
            self.ssl_context.wrap_socket = self.wrap_socket

            if self.server_hostname:
                self.ssl_context.server_hostname = self.server_hostname

            self.ssl_context.set_ciphers(self.cipherSuite)
            self.ssl_context.set_ecdh_curve(self.ecdhCurve)
            self.ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
            self.ssl_context.maximum_version = ssl.TLSVersion.TLSv1_3

        super(CipherSuiteAdapter, self).__init__(**kwargs)

    def wrap_socket(self, *args, **kwargs):
        if hasattr(self.ssl_context, 'server_hostname') and self.ssl_context.server_hostname:
            kwargs['server_hostname'] = self.ssl_context.server_hostname
            self.ssl_context.check_hostname = False
        else:
            self.ssl_context.check_hostname = True
        return self.ssl_context.orig_wrap_socket(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.ssl_context
        kwargs['source_address'] = self.source_address
        return super(CipherSuiteAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        kwargs['ssl_context'] = self.ssl_context
        kwargs['source_address'] = self.source_address
        return super(CipherSuiteAdapter, self).proxy_manager_for(*args, **kwargs)

class TRSolverScraper(Session):
    def __init__(self, *args, **kwargs):
        self.debug = kwargs.pop('debug', False)
        self.disableCloudflareV1 = kwargs.pop('disableCloudflareV1', False)
        self.delay = kwargs.pop('delay', None)
        self.captcha = kwargs.pop('captcha', {})
        self.doubleDown = kwargs.pop('doubleDown', True)
        self.interpreter = kwargs.pop('interpreter', 'native')
        self.requestPreHook = kwargs.pop('requestPreHook', None)
        self.requestPostHook = kwargs.pop('requestPostHook', None)
        self.cipherSuite = kwargs.pop('cipherSuite', None)
        self.ecdhCurve = kwargs.pop('ecdhCurve', 'prime256v1')
        self.source_address = kwargs.pop('source_address', None)
        self.server_hostname = kwargs.pop('server_hostname', None)
        self.ssl_context = kwargs.pop('ssl_context', None)
        self.allow_brotli = kwargs.pop(
            'allow_brotli',
            True if 'brotli' in sys.modules.keys() else False
        )

        self.user_agent = User_Agent(
            allow_brotli=self.allow_brotli,
            browser=kwargs.pop('browser', None)
        )

        self._solveDepthCnt = 0
        self.solveDepth = kwargs.pop('solveDepth', 3)

        super(TRSolverScraper, self).__init__(*args, **kwargs)

        if 'requests' in self.headers['User-Agent']:
            self.headers = self.user_agent.headers
            if not self.cipherSuite:
                self.cipherSuite = self.user_agent.cipherSuite

        if isinstance(self.cipherSuite, list):
            self.cipherSuite = ':'.join(self.cipherSuite)

        self.mount(
            'https://',
            CipherSuiteAdapter(
                cipherSuite=self.cipherSuite,
                ecdhCurve=self.ecdhCurve,
                server_hostname=self.server_hostname,
                source_address=self.source_address,
                ssl_context=self.ssl_context
            )
        )

        copyreg.pickle(ssl.SSLContext, lambda obj: (obj.__class__, (obj.protocol,)))

    def __getstate__(self):
        return self.__dict__

    def perform_request(self, method, url, *args, **kwargs):
        return super(TRSolverScraper, self).request(method, url, *args, **kwargs)

    def simpleException(self, exception, msg):
        self._solveDepthCnt = 0
        sys.tracebacklimit = 0
        raise exception(msg)

    @staticmethod
    def debugRequest(req):
        try:
            print(dump.dump_all(req).decode('utf-8', errors='backslashreplace'))
        except ValueError as e:
            print(f"Debug Error: {getattr(e, 'message', e)}")

    def decodeBrotli(self, resp):
        if requests.packages.urllib3.__version__ < '1.25.1' and resp.headers.get('Content-Encoding') == 'br':
            if self.allow_brotli and resp._content:
                resp._content = brotli.decompress(resp.content)
            else:
                logging.warning(
                    f'You\'re running urllib3 {requests.packages.urllib3.__version__}, Brotli content detected, '
                    'Which requires manual decompression, '
                    'But option allow_brotli is set to False, '
                    'We will not continue to decompress.'
                )
        return resp

    def request(self, method, url, *args, **kwargs):
        if kwargs.get('proxies') and kwargs.get('proxies') != self.proxies:
            self.proxies = kwargs.get('proxies')

        if self.requestPreHook:
            (method, url, args, kwargs) = self.requestPreHook(
                self,
                method,
                url,
                *args,
                **kwargs
            )

        response = self.perform_request(method, url, *args, **kwargs)

        if self.requestPostHook:
            response = self.requestPostHook(self, response)

        return response

    @classmethod
    def create_scraper(cls, sess=None, **kwargs):
        scraper = cls(**kwargs)

        if sess:
            attrs = ['auth', 'cert', 'cookies', 'headers', 'hooks', 'params', 'proxies', 'data']
            for attr in attrs:
                val = getattr(sess, attr, None)
                if val:
                    setattr(scraper, attr, val)

        return scraper

    @classmethod
    def get_tokens(cls, url, **kwargs):
        scraper = cls.create_scraper(**kwargs)
        tokens = {}

        try:
            resp = scraper.get(url, **kwargs)
            if resp.ok:
                tokens = {
                    'cookies': resp.cookies.get_dict(),
                    'User-Agent': scraper.headers['User-Agent']
                }
        except Exception:
            pass

        return tokens

    @classmethod
    def get_cookie_string(cls, url, **kwargs):
        tokens = cls.get_tokens(url, **kwargs)
        return '; '.join(['='.join(pair) for pair in tokens.get('cookies', {}).items()])

create_scraper = TRSolverScraper.create_scraper
get_tokens = TRSolverScraper.get_tokens
get_cookie_string = TRSolverScraper.get_cookie_string 