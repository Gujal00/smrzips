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
import re
from resolveurl import common
from resolveurl.plugins.lib import helpers
from resolveurl.resolver import ResolveUrl, ResolverError

class PornDigResolver(ResolveUrl):
    name = 'porndig'
    domains = ['porndig.com']
    pattern = '(?://|\.)(porndig\.com)/videos/(\d+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {'User-Agent': common.RAND_UA}
        html = self.net.http_GET(web_url, headers=headers).content
            
        if html:
            try:
                iframe_url = re.search("""<iframe.+?src=["'](https://videos\.porndig\.com/player/index/[\d/]+)""", html).groups()[0]
                
                return helpers.get_media_url(iframe_url).replace(' ', '%20')
            
            except:
                raise ResolverError('File not found')
                
        raise ResolverError('File not found')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://www.{host}/videos/{media_id}/')

    @classmethod
    def _is_enabled(cls):
        return True
