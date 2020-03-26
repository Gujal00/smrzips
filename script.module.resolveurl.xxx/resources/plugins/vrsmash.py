'''
    resolveurl XBMC Addon
    Copyright (C) 2016 Gujal

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
import re, urlparse
from resolveurl import common
from resolveurl.plugins.lib import helpers
from resolveurl.resolver import ResolveUrl, ResolverError

class VRSmashResolver(ResolveUrl):
    name = 'vrsmash'
    domains = ['vrsmash.com']
    pattern = '(?://|\.)(vrsmash\.com)/view/(\d+/[^/]+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        headers = {'User-Agent': common.RAND_UA}
        web_url = self.get_url(host, media_id)
        html = self.net.http_GET(web_url, headers=headers).content

        if html:
            try:
                headers.update({'Referer': web_url})
                file = re.search('''<source\s*src=['"]([^"']+)''', html, re.DOTALL).groups()[0]
                return urlparse.urljoin('https://www.vrsmash.com', file) + helpers.append_headers(headers)
            except:
                raise ResolverError('File not found')

        raise ResolverError('File not found')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://www.{host}/view/{media_id}')

    @classmethod
    def _is_enabled(cls):
        return True
