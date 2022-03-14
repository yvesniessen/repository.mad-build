# -*- coding: utf-8 -*-

#2021-07-03

# Temp. Sammelsurium

import json, os, re
import unicodedata
import requests
from resources.lib.control import urlparse, dataPath, showparentdiritems, currentWindowId, getInfoLabel, sleep, getSetting
from six.moves import urllib_error, urllib_request, urllib_parse
from operator import itemgetter
from functools import cmp_to_key
from resources.lib import log_utils

def cmp(x, y):
    """
    Replacement for built-in function cmp that was removed in Python 3

    Compare the two objects x and y and return an integer according to
    the outcome. The return value is negative if x < y, zero if x == y
    and strictly positive if x > y.

    https://portingguide.readthedocs.io/en/latest/comparisons.html#the-cmp-function
    """

    return (x > y) - (x < y)

def multikeysort(items, columns):
    # a = multikeysort(b, ['-column1', 'column2']) # - revers / b z.B. self.list
    comparers = [
        ((itemgetter(col[1:].strip()), -1) if col.startswith('-') else (itemgetter(col.strip()), 1))
        for col in columns
    ]
    def comparer(left, right):
        comparer_iter = (
            cmp(fn(left), fn(right)) * mult
            for fn, mult in comparers
        )
        return next((result for result in comparer_iter if result), 0)
    return sorted(items, key=cmp_to_key(comparer))


def getAliases(imdb, type):
    V2_API_KEY = getSetting('api.trakt').strip()
    headers = {'Content-Type': 'application/json', 'trakt-api-key': V2_API_KEY, 'trakt-api-version': '2'}
    aliasesUrl = 'https://api.trakt.tv/{0}/{1}/aliases'.format(type, imdb)
    result = requests.get(aliasesUrl, headers=headers)
    if result.status_code == 200:
        result = json.loads(result.content)
        localtitle = [i['title'] for i in result if i['country'] in ['de']]
        localtitle = localtitle[0] if any(localtitle) else None
        return [i['title'] for i in result if i['country'] in ['de', 'us', 'en', 'at', '']], localtitle
    else:
        return [], ''

def aliases_to_array(aliases, filter=None):
    try:
        if not filter:
            filter = []
        if isinstance(filter, type(u"")):
            filter = [filter]
        return [x.get('title') for x in aliases if not filter or x.get('country') in filter]
    except:
        return []

def getsearch(title):
    if title is None:
        return
    title = title.lower()
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
  # title = re.sub('\\\|/|-|–|:|;|\*|\?|"|\'|<|>|\|', '', title).lower()
    title = re.sub('[\\\\/\\-–:;*?"\'<>|]', '', title).lower()
    title = re.sub('\s+', ' ', title)
    return title

def get_titles_for_search(localtitle, title, aliases):
    titles = []
    try:
        if "country':" in str(aliases): aliases = aliases_to_array(aliases)
        if localtitle != '':
            localtitle = localtitle.lower()
            titles.append(localtitle)
            titles.append(getsearch(localtitle))
        if title != '':
            title = title.lower()
            if localtitle != title:
                titles.append(title)
                titles.append(getsearch(title))
        for i in aliases:
            try:
                if str(i).lower() != title and str(i).lower() != localtitle and i != '':
                    titles.append(str(i).lower())
                    titles.append(getsearch(str(i)))
            except:
                pass
        #titles = [str(i) for i in titles if all(ord(c) < 128 for c in i)]
        titles = [item for i, item in enumerate(titles) if item not in titles[:i]]
        titles = more_titles(titles)
        return titles
    except:
        return titles

#TODO
# def title_article(titles):
#     try:
#         articles_en = ['the']  # ['the', 'a', 'an']
#         articles_de = ['die', 'der']  # ['der', 'die', 'das']
#         for title in titles:
#             match = re.match('^((\w+)\s+)', title.lower())
#             if match and match.group(2) in articles_en:
#                 for i in articles_de:
#                     title = title.replace(title[:3], i)
#                     if title not in titles: titles.append(title)
#         return titles
#     except:
#         return titles


def more_titles(titles):
    for i in titles:
        temp = _titleclean(i)
        if temp and temp not in titles:
            titles.append(temp)
    return titles

def _titleclean(title):
    try:
        if 'IV' == title.rsplit(' ',1)[1]:
            title.replace(' IV', ' 4')
        elif 'VI' == title.rsplit(' ',1)[1]:
            title.replace(' VI', ' 6')
        elif 'V' == title.rsplit(' ',1)[1]:
            title.replace(' V', ' 5')
        elif 'III' == title.rsplit(' ',1)[1]:
            title.replace(' III', ' 3')
        elif 'II' == title.rsplit(' ',1)[1]:
            title.replace(' II', ' 2')
        # elif 'I' == title.rsplit(' ',1)[1]:
        #     title.replace('I', '1')
        elif '2' == title.rsplit(' ',1)[1]:
            title.replace(' 2', ' II')
        elif '3' == title.rsplit(' ',1)[1]:
            title.replace(' 3', ' III')
        elif '4' == title.rsplit(' ',1)[1]:
            title.replace(' 4', ' IV')
        elif '5' == title.rsplit(' ',1)[1]:
            title.replace(' 5', ' V')
        elif '6' == title.rsplit(' ',1)[1]:
            title.replace(' 6', ' VI')
        return title
    except:
        pass




def check_302(url, headers={}):
    try:
        while True:
            host = urlparse(url).netloc
            headers.update({'Host': host})
            r = requests.get(url, allow_redirects=False, headers=headers, timeout=7)
            if 300 <= r.status_code <= 400:
                url = r.headers['Location']
            elif 400 <= r.status_code:
                return
            elif 200 == r.status_code:
                return url
            elif 300 > r.status_code:
                return url
            else:
                break
        return
    except:
        return


def test_stream(stream_url):
    """
    Returns True if the stream_url gets a non-failure http status (i.e. <400) back from the server
    otherwise return False

    Intended to catch stream urls returned by resolvers that would fail to playback
    """
    # parse_qsl doesn't work because it splits elements by ';' which can be in a non-quoted UA
    try:
        headers = dict([item.split('=') for item in (stream_url.split('|')[1]).split('&')])
    except:
        headers = {}
    for header in headers:
        headers[header] = urllib_parse.unquote_plus(headers[header])
    log_utils.log('Setting Headers on UrlOpen: %s' % headers, log_utils.LOGDEBUG)

    import ssl
    try:
        #- streamurl mit ungültigen Zertifikat abweisen
        ssl_context = ssl.create_default_context()
        #ssl_context.check_hostname = False         
        #ssl_context.verify_mode = ssl.CERT_NONE        
        opener = urllib_request.build_opener(urllib_request.HTTPSHandler(context=ssl_context))
        urllib_request.install_opener(opener)
    except:
        pass

    try:
        msg = ''
        request = urllib_request.Request(stream_url.split('|')[0], headers=headers)
        # only do a HEAD request. gujal
        request.get_method = lambda: 'HEAD'
        #  set urlopen timeout to 15 seconds
        http_code = urllib_request.urlopen(request, timeout=15).getcode()
    except urllib_error.HTTPError as e:
        if isinstance(e, urllib_error.HTTPError):
            http_code = e.code
            if http_code == 405:
                http_code = 200
        else:
            http_code = 600
    except urllib_error.URLError as e:
        http_code = 500
        if hasattr(e, 'reason'):
            # treat an unhandled url type as success
            if 'unknown url type' in str(e.reason).lower():
                return True
            elif 'certificate verify failed' in str(e.reason).lower():
                return True
            else:
                msg = e.reason
        if not msg:
            msg = str(e)

    except Exception as e:
        http_code = 601
        msg = str(e)
        if msg == "''":
            http_code = 504

    # added this log line for now so that we can catch any logs on streams that are rejected due to test_stream failures
    # we can remove it once we are sure this works reliably
    if int(http_code) >= 400 and int(http_code) != 504:
        log_utils.log('Stream UrlOpen Failed: Url: %s \n HTTP Code: %s Msg: %s' % (stream_url, http_code, msg), log_utils.LOGWARNING)

    return int(http_code) < 400 or int(http_code) == 504

#TODO
def m3u8_check(stream_url):
    if not '.m3u8' in (stream_url.split('|')[0]).lower(): return stream_url
    try:
        headers = dict([item.split('=') for item in (stream_url.split('|')[1]).split('&')])
    except:
        headers = {}
    for header in headers:
        headers[header] = urllib_parse.unquote_plus(headers[header])
    req = urllib_request.Request(stream_url.split('|')[0], headers=headers)
    try:
        line = (urllib_request.urlopen(req).readlines())
        if re.search('\.m4.', str(line)): return
        # if '.m4s' in str(line):
        #     return
        # elif 'http' in str(line):
        #     return stream_url
        else:
            return stream_url # new_m3u8(req, stream_url.split('|')[0])

    except urllib_error.URLError as e:
        if hasattr(e, 'reason')and 'certificate verify failed' in str(e.reason).lower():
            return stream_url
        return

#TODO
def new_m3u8(req, url):
    import xbmcvfs
    new_m3u8_file = os.path.join(dataPath, 'temp.m3u8')
    loc_playlist = os.path.join(dataPath, 'myPlaylist.m3u')
    # scheme, netloc, path, query, frag = parse.urlsplit(url)
    http_scheme = urllib_parse.urlparse(url).scheme
    host = urllib_parse.urlparse(url).netloc
    url_path = os.path.split(url)[0] + '/'
    url_file = os.path.split(url)[1]
    base_url = '%s://%s' % (http_scheme, host)

    data = ''
    for line in urllib_request.urlopen(req).readlines():
        line = line.strip()
        #a = line.decode("utf-8")
        line = convert(line, http_scheme, base_url, url_path)
        if line:
            data = data + ('{0}\n'.format(line))
    #print(data)
    m3u8 = xbmcvfs.File(new_m3u8_file, 'w')
    m3u8.write(data)
    m3u8.close()
    if not xbmcvfs.exists(loc_playlist):
        #L = "#EXTM3U \n#EXT-X-VERSION:3\n#EXT-X-STREAM-INF:PROGRAM-ID=1\n%s\n"] % str(new_m3u8_file)
        #L = "#EXTM3U \n#EXTINF:0,temp.m3u8\nfile:///%s\n" % str(new_m3u8_file)
        L = "#EXTM3U \n#EXT-X-VERSION:3\n#EXT-X-STREAM-INF:PROGRAM-ID=1\n%s\n" % str(new_m3u8_file)
        loc_playlist = xbmcvfs.File(loc_playlist, 'w')
        loc_playlist.write(L)
        #loc_playlist.write(str(new_m3u8_file))
        loc_playlist.close()
    return new_m3u8_file #loc_playlist new_m3u8_file


def convert(line, http_scheme, base_url, url_path):
    if line.startswith('#EXT-X-MAP'):
        pattern = '''URI=(?:'|")(.+?)(?:'|")'''
        URI = re.search(pattern, line).group(1)
        if URI.startswith('//'): URI =  '%s:%s' % (http_scheme, URI)
        elif URI.startswith('/'): URI =  base_url + URI
        elif URI.startswith('http'): return URI
        else: URI =  url_path + URI
        return '#EXT-X-MAP:URI="%s"' % URI
    elif line.startswith('#'): return line
    elif line.startswith('http'): return line
    elif line.startswith('//'): return '%s:%s' % (http_scheme, line)
    elif line.startswith('/'): return base_url + line
    else: return url_path + line


def normalize(title):
    from sys import version_info
    try:
       if version_info[0] > 2: return title
       else:
        try: return title.decode('ascii').encode("utf-8")
        except: return str(''.join(c for c in unicodedata.normalize('NFKD', unicode(title.decode('utf-8'))) if unicodedata.category(c) != 'Mn'))
    except:
        return title

# def normalize(title):
#     import codecs
#     try:
#         return codecs.decode(title, 'UTF-8')
#     except:
#         return title


## setzt Auswahl nach letzte als gesehen markierte Episode / Staffel
def setPosition(pos, _name, content='movies'): # org.: episodes

    isdebug = True if getSetting('status.debug') == 'true' else False
    win = currentWindowId  # win = xbmcgui.Window(xbmcgui.getCurrentWindowId())
    pos = int(pos)
    pos_sp = pos if showparentdiritems() else pos - 1
    count = 0

    for count in range(1, 15):
        ccont = getInfoLabel("Container.Content")
        if ccont == content: break
        sleep(100)

    if isdebug:
        log_utils.log(_name + ' - Container.Content (1) - soll: %s ist: %s  count: %s' % (content, getInfoLabel("Container.Content"), count), log_utils.LOGINFO)
        log_utils.log(_name + ' - System.CurrentControlID - old: %s ' % getInfoLabel("System.CurrentControlID"), log_utils.LOGINFO)
        log_utils.log(_name + ' - pos: %s - check: %s' % (pos, int(getInfoLabel("Container().CurrentItem"))), log_utils.LOGINFO)

    # setze Position
    for count in range(1, 15):
        try:
            cid = getInfoLabel("System.CurrentControlID")
            ctrl = win.getControl(int(cid))
        except:
            sleep(200)
            continue

        ctrl.selectItem(pos_sp)
        sleep(100)
        check = int(getInfoLabel("Container().CurrentItem"))  # % cid)) # Container().CurrentItem
        if pos == check: break

    if isdebug:
        log_utils.log(_name + ' - pos: %s - check: %s - count: %s' % (pos, int(getInfoLabel("Container().CurrentItem")),count), log_utils.LOGINFO)
        log_utils.log(_name + ' - System.CurrentControlID:  %s' % getInfoLabel("System.CurrentControlID"), log_utils.LOGINFO)


def getParams(_params):
    for key, value in _params.items():
        try:
            exec("%s = %s" % (key, value))
        except:
            exec ("%s = '%s'" % (key, value))

