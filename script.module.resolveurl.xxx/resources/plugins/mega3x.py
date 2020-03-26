'''
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

import re
from resolveurl import common
from resolveurl.resolver import ResolveUrl, ResolverError
from resolveurl.plugins.lib import jsunpack, helpers

class Mega3xResolver(ResolveUrl):
    name = "mega3x"
    domains = ['mega3x.net']
    pattern = '(?://|\.)(?:www\.)?(mega3x.net)/(?:embed-)?([0-9a-zA-Z]+).html'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {'User-Agent': common.FF_USER_AGENT, 'Referer': web_url}
        html = self.net.http_GET(web_url, headers=headers).content
        js = re.compile('<script[^>]+>(eval.*?)</sc', re.DOTALL | re.IGNORECASE).search(html).group(1)
        if jsunpack.detect(js):
            html += jsunpack.unpack(js)
        if html:
            source = re.search(',"(http.*?mp4)"', html, re.I)
            if source:
                return source.group(1) + helpers.append_headers(headers)        
        raise ResolverError('Video not found')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://mega3x.net/embed-{media_id}.html')

    @classmethod
    def _is_enabled(cls):
        return True
