'''
    resolveurl XBMC Addon
    Copyright (C) 2017

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

class HentaiHeavenResolver(ResolveUrl):
    name = 'hentaihaven'
    domains = ['hentaihaven.org']
    pattern = '(?://|\.)(hentaihaven\.org)/([\w\-]+)'
    
    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {'User-Agent': common.RAND_UA}
        html = self.net.http_GET(web_url, headers=headers).content
        
        if html:
            if 'sucuri_cloudproxy_js' in html:
                cookie = self.sucuri(html)
                headers.update({'Referer': web_url, 'Cookie': cookie})
                html = self.net.http_GET(web_url, headers=headers).content
                    
            sources = re.findall('''<source\s*.+?label=['"](\w+)['"]\s*src=['"]([^'"]+)''', html)
            sources = [(i[0], i[1]) for i in sources if not i[1] == "dead_link"]
            if sources:
                try: sources.sort(key=lambda x: int(re.sub("\D", "", x[0])), reverse=True)
                except: pass
                return helpers.pick_source(sources) + helpers.append_headers(headers)

        raise ResolverError('File not found')
        
    def sucuri(self, html):
        try:
            import base64
            self.cookie = None
            s = re.compile("S\s*=\s*'([^']+)").findall(html)[0]
            s = base64.b64decode(s)
            s = s.replace(' ', '')
            s = re.sub('String\.fromCharCode\(([^)]+)\)', r'chr(\1)', s)
            s = re.sub('\.slice\((\d+),(\d+)\)', r'[\1:\2]', s)
            s = re.sub('\.charAt\(([^)]+)\)', r'[\1]', s)
            s = re.sub('\.substr\((\d+),(\d+)\)', r'[\1:\1+\2]', s)
            s = re.sub(';location.reload\(\);', '', s)
            s = re.sub(r'\n', '', s)
            s = re.sub(r'document\.cookie', 'cookie', s)

            cookie = '' ; exec(s)
            self.cookie = re.compile('([^=]+)=(.*)').findall(cookie)[0]
            self.cookie = '%s=%s' % (self.cookie[0], self.cookie[1])

            return self.cookie
        except:
            raise ResolverError('Could not decode sucuri')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='http://{host}/{media_id}')

    @classmethod
    def _is_enabled(cls):
        return True
