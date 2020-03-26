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

class SexixResolver(ResolveUrl):
    name = 'sexix'
    domains = ['sexix.net']
    pattern = '(?://|\.)(sexix\.net)/video([-\w]+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {'User-Agent': common.RAND_UA}
        html = self.net.http_GET(web_url, headers=headers).content
            
        if html:
            iframe_url = re.search("""<iframe.+?src=["'](http://sexix\.net/v\.php\?(u=.+?))['"]""", html)
            if iframe_url:
                playlist_url = 'http://sexix.net/qaqqew/playlist.php?%s' % iframe_url.group(2)
                headers.update({'Referer': iframe_url.group(1)})
                _html = self.net.http_GET(playlist_url, headers=headers).content
                if _html:
                    sources = re.findall("""source file=["']([^"']+).+?label=["']([^"']+)""", _html)
                    if sources:
                        sources = [(i[1], i[0]) for i in sources]
                        try: sources.sort(key=lambda x: int(re.sub("\D", "", x[0])), reverse=True)
                        except: pass
                        headers.update({'Referer': web_url})
                        return helpers.pick_source(sources) + helpers.append_headers(headers)
                
        raise ResolverError('File not found')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='http://{host}/video{media_id}/')

    @classmethod
    def _is_enabled(cls):
        return True
