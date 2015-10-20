#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2015 emijrp <emijrp@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
import sys
import time
import urllib2

def main():
    youtubedl = './youtube-dl' # path to youtube-dl script, needed to download the videos obviosly
    os.system('%s -U' % youtubedl)
    url = 'http://archivo.juventudes.org/directora'
    print 'Retrieving', url
    try:
        req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
        html = unicode(urllib2.urlopen(req).read(), 'utf-8')
    except:
        sys.exit()
    
    directors = re.finditer(ur'<span class="field-content"><a href="(?P<url>[^<>]*?)">(?P<name>[^<>]*?)</a>', html)
    for director in directors:
        time.sleep(3)
        directorname = director.group('name')
        directorurl = director.group('url')
        print '\n', '#'*50, '\n', directorname, 'http://archivo.juventudes.org' + directorurl, '\n', '#'*50
        
        url2 = 'http://archivo.juventudes.org' + directorurl
        try:
            req2 = urllib2.Request(url2, headers={ 'User-Agent': 'Mozilla/5.0' })
            html2 = unicode(urllib2.urlopen(req2).read(), 'utf-8')
        except:
            print 'ERROR:', directorname, url2
        
        if ' ' in directorname:
            directordir = '%s, %s' % (directorname.split(' ')[-1], ' '.join(directorname.split(' ')[0:-1]))
        else:
            directordir = directorname
        if not os.path.exists(directordir):
            os.makedirs(directordir)
        
        documentaries = re.finditer(ur'<h2 class="title"><a href="(?P<url>[^<>]*?)" title="[^<>]*?">(?P<name>[^<>]*?)</a></h2>', html2)
        for documentary in documentaries:
            time.sleep(1)
            documentaryname = documentary.group('name')
            documentaryurl = documentary.group('url')
            print documentaryname, 'http://archivo.juventudes.org' + documentaryurl
            
            url3 = 'http://archivo.juventudes.org' + documentaryurl
            try:
                req3 = urllib2.Request(url3, headers={ 'User-Agent': 'Mozilla/5.0' })
                html3 = unicode(urllib2.urlopen(req3).read(), 'utf-8')
            except:
                print 'ERROR:', documentaryname, url3
            
            documentaryname_ = re.sub(ur'(?im)[/]', ur' ', documentaryname)
            
            content = '<h1 class="title">' + html3.split('<h1 class="title">')[1].split('<div class="terms">')[0]
            content = content.strip()
            content = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="es" xml:lang="es" xmlns:og="http://opengraphprotocol.org/schema/">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body>
%s
</div></div></div>
</body>
</html>""" % (content)
            f = open('%s/%s (%s).html' % (directordir, documentaryname_, directorname), 'w')
            f.write(content.encode('utf-8'))
            f.close()
            
            #get urls
            videourls = []
            videourls += re.findall(ur'(?im)(https?://(?:www\.)?youtube\.com/watch\?v=(?:[^<>\'" ]+))', content)
            videourls += re.findall(ur'(?im)(https?://(?:www\.)?youtube\.com/embed/(?:[^<>\'"\? ]+))', content)
            videourls += re.findall(ur'(?im)(https?://(?:www\.)?vimeo\.com/\d+)', content)
            videourls += re.findall(ur'(?im)(https?://(?:www\.)?dailymotion\.com/[^<>\'" ]+)', content)
            
            print videourls
            
            #download videos
            for videourl in videourls:
                pass
                os.system("python %s %s --write-description --all-subs -i -c -o '%s/%%(title)s (%s)-%%(id)s.%%(ext)s'" % (youtubedl, videourl, directordir, directorname))

if __name__ == '__main__':
    main()
