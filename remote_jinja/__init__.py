from html import unescape
from jinja2 import Template
import requests
from time import time
from requests.adapters import HTTPAdapter

class localCache():
    """
    localCache class stores data in a dictionary in memory, it is recommended to use a caching server such as redis instead.
    To set the caching server, set rt.cache = <your cache instance>
    """

    def __init__(self, default_timeout=300):
        self._cache = {}
        self.default_timeout = default_timeout

    def _normalize_timeout(self, timeout):
        if timeout is None:
            timeout = self.default_timeout
        if timeout > 0:
            timeout = time() + timeout
        return timeout

    def get(self, key):
        try:
            expires, value = self._cache[key]
            if expires == 0 or expires > time():
                return value
        except (KeyError):
            return None

    def set(self, key, value, timeout=None):
        expires = self._normalize_timeout(timeout)
        self._cache[key] = (expires, value)
        return True


class RemoteTemplate():
    """
    RemoteTemplate class holds all the parameters andd funtion for rendering a jinja template from a remote website.
    
        self.cache = localCache() # This should be substituted with a cache server like redis
        self.default_refresh = True # This should be set to False in production
        self.default_timeout = 300 # This should be set for a longer period of time in production
    
    """

    def __init__(self):
        self.cache = localCache()
        self.default_refresh = True
        self.default_timeout = 300
        self.block_start_string='{[%'
        self.block_end_string='%]}'
        self.variable_start_string='{['
        self.variable_end_string=']}'

    def _request_page(self, url):
        # load bage as browser in the event of bot detection
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36','Content-Type': 'text/html', 'Content-Encoding': 'gzip'}
        # retry page 5 times
        s = requests.Session()
        s.mount(url, HTTPAdapter(max_retries=5))
        try:
            response = s.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Cannot fetch remote template for url {url} Exception: {e}")

        return s.get(url, headers=headers)

    def _clean_html(self, html_text):
        return unescape(html_text.encode("latin1").decode("utf-8"))

    def _normalize_refresh(self, refresh):
        if refresh == None:
            refresh = self.default_refresh
        return refresh

    def _load_page(self, url, refresh_template=None):
        refresh = self._normalize_refresh(refresh_template)
        key = f"remote-cache-{url}"
        data = None
        data = self.cache.get(key)
        if refresh or not data:
            page = self._request_page(url)
            data = page.text
            self.cache.set(key, data, timeout=self.default_timeout)
        return data

    def _render_remote(self, url,
            block_start_string=None,
            block_end_string=None,
            variable_start_string=None, 
            variable_end_string=None,
            refresh_template=None,
            *args, **kwargs):
        """
        Central function fetching remote template and compiling it with jinja.
        Specific params can be altered in order 
        params:
        url='https://yourwebsite.com/template'
        block_start_string='{[%'
        block_end_string='%]}'
        variable_start_string='{['
        variable_end_string=']}'
        refresh_template=request.args.get("refresh") # Refresh if URL contains param "refresh"
        """
        html_text = self._load_page(url, refresh_template)
        clean_html_text = self._clean_html(html_text)
        tm = Template(
            clean_html_text,
            block_start_string=(block_start_string or self.block_start_string),
            block_end_string=(block_end_string or self.block_end_string),
            variable_start_string=(variable_start_string or self.variable_start_string), 
            variable_end_string=(variable_end_string or self.variable_end_string))
        return tm.render(*args, **kwargs)


rt = RemoteTemplate()
render_remote = rt._render_remote