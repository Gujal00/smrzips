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
import re, json
from resolveurl import common
from resolveurl.plugins.lib import helpers
from resolveurl.resolver import ResolveUrl, ResolverError

class FourTubeResolver(ResolveUrl):
    name = '4tube'
    domains = ['4tube.com']
    pattern = '(?://|\.)(4tube\.com)/(?:videos|embed)/(\d+)'
    
    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {'User-Agent': common.RAND_UA}
        html = self.net.http_GET(web_url, headers=headers).content
        
        if html:
            try:
                pattern = r"""ajax\(url,opts\);}}\)\(([\d]+),[\d]+,\[([\d,]+)\]\);"""
                url_id, quals = re.findall(pattern, html)[0]
                quals = quals.replace(',','+')
                headers.update({'Referer': web_url,  'Origin': host})
                post_url = 'https://tkn.kodicdn.com/0000000%s/desktop/%s' % (url_id, quals)
                html = self.net.http_POST(post_url, headers=headers, form_data='').content
                if html:
                    sources = helpers.scrape_sources(html, patterns=["""['"](?P<label>\d+)['"]:{[\w":,]+token['"]:['"](?P<url>[^'"]+)"""])
                    if sources: return helpers.pick_source(sources) + helpers.append_headers(headers)
            except: 
                raise ResolverError('File not found')
        
        raise ResolverError('File not found')
        
    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://www.{host}/js/player/web/{media_id}.js?hl=en')

    @classmethod
    def _is_enabled(cls):
        return True
