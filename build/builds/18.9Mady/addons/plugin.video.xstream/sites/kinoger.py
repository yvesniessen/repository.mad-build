# -*- coding: utf-8 -*-
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.tools import logger, cParser
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.config import cConfig
try:
    from itertools import izip_longest as ziplist
except ImportError:
    from itertools import zip_longest as ziplist
import base64, random

SITE_IDENTIFIER = 'kinoger'
SITE_NAME = 'Kinoger'
SITE_ICON = 'kinoger.png'
SITE_SETTINGS = '<setting default="kinoger.com" enable="!eq(-2,false)" id="kinoger-domain" label="30051" type="labelenum" values="kinoger.com|kinoger.to" />'
URL_MAIN = 'https://' + cConfig().getSetting('kinoger-domain')
URL_SERIE = URL_MAIN + '/stream/serie/'


def load():
    logger.info('Load %s' % SITE_NAME)
    params = ParameterHandler()
    params.setParam('sUrl', URL_MAIN)
    cGui().addFolder(cGuiElement('Filme & Serien', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_SERIE)
    cGui().addFolder(cGuiElement('Genre', SITE_IDENTIFIER, 'showGenre'))
    cGui().addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showEntries'), params)
    cGui().addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    cGui().setEndOfDirectory()


def showGenre():
    params = ParameterHandler()
    sHtmlContent = cRequestHandler(URL_MAIN).request()
    pattern = '<li[^>]class="links"><a href="([^"]+).*?/>([^<]+)</a>'
    isMatch, aResult = cParser.parse(sHtmlContent, pattern)
    if not isMatch:
        cGui().showInfo()
        return

    for sUrl, sName in aResult:
        params.setParam('sUrl', URL_MAIN + sUrl)
        cGui().addFolder(cGuiElement(sName, SITE_IDENTIFIER, 'showEntries'), params)
    cGui().setEndOfDirectory()


def showEntries(entryUrl=False, sGui=False, sSearchText=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    if not entryUrl: entryUrl = params.getValue('sUrl')
    oRequest = cRequestHandler(entryUrl, ignoreErrors=(sGui is not False))
    if sSearchText:
        oRequest.addParameters('story', sSearchText)
        oRequest.addParameters('do', 'search')
        oRequest.addParameters('subaction', 'search')
        oRequest.addParameters('x', '0')
        oRequest.addParameters('y', '0')
        oRequest.addParameters('titleonly', '3')
        oRequest.addParameters('submit', 'submit')
    else:
        oRequest.addParameters('dlenewssortby', 'date')
        oRequest.addParameters('dledirection', 'desc')
        oRequest.addParameters('set_new_sort', 'dle_sort_main')
        oRequest.addParameters('set_direction_sort', 'dle_direction_main')
    sHtmlContent = oRequest.request()
    pattern = 'class="title.*?href="([^"]+)">([^<]+).*?src="([^"]+)(.*?)</span>'
    isMatch, aResult = cParser().parse(sHtmlContent, pattern)
    if not isMatch:
        if not sGui: oGui.showInfo()
        return

    total = len(aResult)
    for sUrl, sName, sThumbnail, sDummy in aResult:
        if sSearchText and not cParser().search(sSearchText, sName):
            continue
        isTvshow = True if 'staffel' in sName.lower() or 'serie' in entryUrl or ';">S0' in sDummy else False
        isYear, sYear = cParser.parse(sName, '(.*?)\((\d*)\)')
        for name, year in sYear:
            sName = name
            sYear = year
            break
        isDesc, sDesc = cParser.parseSingleResult(sDummy, '</b>([^<]+)')
        isDuration, sDuration = cParser.parseSingleResult(sDummy, '(?:Laufzeit|Spielzeit).*?(\d[^<]+)')
        if ':' in sDuration:
            sDuration = time2minutes(sDuration)
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showSeasons' if isTvshow else 'showHosters')
        oGuiElement.setThumbnail(sThumbnail)
        if isYear:
            oGuiElement.setYear(sYear)
        if isDesc:
            oGuiElement.setDescription(sDesc)
        if isDuration:
            oGuiElement.addItemValue('duration', sDuration)
        oGuiElement.setMediaType('tvshow' if isTvshow else 'movie')
        params.setParam('sThumbnail', sThumbnail)
        params.setParam('TVShowTitle', sName)
        params.setParam('entryUrl', sUrl)
        oGui.addFolder(oGuiElement, params, isTvshow, total)
    if not sGui:
        isMatchNextPage, sNextUrl = cParser().parseSingleResult(sHtmlContent, '<a[^>]href="([^"]+)">vorw')
        if isMatchNextPage:
            params.setParam('sUrl', sNextUrl)
            oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
        oGui.setView('tvshows' if 'staffel' in sName.lower() else 'movies')
        oGui.setEndOfDirectory()


def showSeasons():
    params = ParameterHandler()
    entryUrl = params.getValue('entryUrl')
    sThumbnail = params.getValue('sThumbnail')
    sTVShowTitle = params.getValue('TVShowTitle')
    sHtmlContent = cRequestHandler(entryUrl).request()
    L11 = []
    isMatchsst, sstsContainer = cParser.parseSingleResult(sHtmlContent, 'sst.show.*?</script>')
    if isMatchsst:
        sstsContainer = sstsContainer.replace('[', '<').replace(']', '>')
        isMatchsst, L11 = cParser.parse(sstsContainer, "<'([^>]+)")
        if isMatchsst:
            total = len(L11)
    L22 = []
    isMatchollhd, ollhdsContainer = cParser.parseSingleResult(sHtmlContent, 'ollhd.show.*?</script>')
    if isMatchollhd:
        ollhdsContainer = ollhdsContainer.replace('[', '<').replace(']', '>')
        isMatchollhd, L22 = cParser.parse(ollhdsContainer, "<'([^>]+)")
        if isMatchollhd:
            total = len(L22)
    L33 = []
    isMatchpw, pwsContainer = cParser.parseSingleResult(sHtmlContent, 'pw.show.*?</script>')
    if isMatchpw:
        pwsContainer = pwsContainer.replace('[', '<').replace(']', '>')
        isMatchpw, L33 = cParser.parse(pwsContainer, "<'([^>]+)")
        if isMatchpw:
            total = len(L33)
    isMatchgo, gosContainer = cParser.parseSingleResult(sHtmlContent, 'go.show.*?</script>')
    if isMatchgo:
        gosContainer = gosContainer.replace('[', '<').replace(']', '>')
        isMatchgo, L44 = cParser.parse(gosContainer, "<'([^>]+)")
        if isMatchgo:
            total = len(L44)

    isDesc, sDesc = cParser.parseSingleResult(sHtmlContent, '</b>([^"]+)<br><br>')
    for i in range(0, total):
        try:
            params.setParam('L11', L11[i])
        except Exception:
            pass
        try:
            params.setParam('L22', L22[i])
        except Exception:
            pass
        try:
            params.setParam('L33', L33[i])
        except Exception:
            pass
        try:
            params.setParam('L44', L44[i])
        except Exception:
            pass
        i = i + 1
        oGuiElement = cGuiElement('Staffel ' + str(i), SITE_IDENTIFIER, 'showEpisodes')
        oGuiElement.setMediaType('season')
        oGuiElement.setTVShowTitle(sTVShowTitle)
        oGuiElement.setSeason(i)
        oGuiElement.setThumbnail(sThumbnail)
        if isDesc:
            oGuiElement.setDescription(sDesc)
        params.setParam('sDesc', sDesc)
        params.setParam('sSeasonNr', i)
        cGui().addFolder(oGuiElement, params, True, total)
        cGui().setView('seasons')
    cGui().setEndOfDirectory()


def showEpisodes():
    params = ParameterHandler()
    sSeasonNr = params.getValue('sSeasonNr')
    sThumbnail = params.getValue('sThumbnail')
    sTVShowTitle = params.getValue('TVShowTitle')
    sDesc = params.getValue('sDesc')
    L11 = []
    if params.exist('L11'):
        L11 = params.getValue('L11')
        isMatch1, L11 = cParser.parse(L11, "(http[^']+)")
    L22 = []
    if params.exist('L22'):
        L22 = params.getValue('L22')
        isMatch, L22 = cParser.parse(L22, "(http[^']+)")
    L33 = []
    if params.exist('L33'):
        L33 = params.getValue('L33')
        isMatch3, L33 = cParser.parse(L33, "(http[^']+)")
    L44 = []
    if params.exist('L44'):
        L44 = params.getValue('L44')
        isMatch4, L44 = cParser.parse(L44, "(http[^']+)")
    liste = ziplist(L11, L22, L33, L44)
    i = 0
    for sUrl in liste:
        i = i + 1
        oGuiElement = cGuiElement('Episode ' + str(i), SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setTVShowTitle(sTVShowTitle)
        oGuiElement.setSeason(sSeasonNr)
        oGuiElement.setEpisode(i)
        oGuiElement.setMediaType('episode')
        if sDesc:
            oGuiElement.setDescription(sDesc)
        if sThumbnail:
            oGuiElement.setThumbnail(sThumbnail)
        params.setParam('sLinks', sUrl)
        cGui().addFolder(oGuiElement, params, False)
    cGui().setView('episodes')
    cGui().setEndOfDirectory()


def showHosters():
    hosters = []
    params = ParameterHandler()
    if params.exist('sLinks'):
        sUrl = params.getValue('sLinks')
        isMatch, aResult = cParser().parse(sUrl, "(http[^']+)")
    else:
        sUrl = params.getValue('entryUrl')
        sHtmlContent = cRequestHandler(sUrl, ignoreErrors=True).request()
        pattern = "show[^>]\d,[^>][^>]'([^']+)"
        isMatch, aResult = cParser().parse(sHtmlContent, pattern)
    if isMatch:
        for sUrl in aResult:
            try:
                if 'sst' in sUrl:
                    oRequest = cRequestHandler(sUrl, ignoreErrors=True)
                    oRequest.addHeaderEntry('Referer', URL_MAIN)
                    sHtmlContent = oRequest.request()
                    if sHtmlContent == '': continue
                    isMatch, sContainer = cParser.parse(sHtmlContent, 'file(?:":"|:")([^"]+)')
                    if isMatch:
                        isMatch, aResult = cParser.parse(sContainer[0], '(?:(\d+p)[^>])?((?:http|//)[^",]+)')
                        if isMatch:
                            for sQualy, sUrl2 in aResult:
                                if not sQualy:
                                    sQualy = Qualy(sUrl2)
                                if ' or ' in sUrl2:
                                    sUrl2 = sUrl2.split(' or ')[0]
                                hoster = {'link': sUrl2, 'name': sQualy + ' ' + cParser.urlparse(sUrl), 'resolveable': True}
                                hosters.append(hoster)
                elif 'protonvideo' in sUrl:
                    oRequest = cRequestHandler('https://api.svh-api.ch/api/v4/player', ignoreErrors=True, jspost=True)
                    oRequest.addParameters('idi', sUrl.split('/')[4])
                    oRequest.addParameters('token', aes(sUrl.split('/')[4]))
                    sHtmlContent = oRequest.request()
                    isMatch, sContainer = cParser.parse(sHtmlContent, 'file(?:":"|:")([^"]+)')
                    if isMatch:
                        isMatch, aResult = cParser.parse(sContainer[0], '(?:(\d+p)[^>])?((?:http|//)[^",]+)')
                        if isMatch:
                            for sQualy, sUrl2 in aResult:
                                hoster = {'link': sUrl2, 'name': sQualy + ' ' + cParser.urlparse(sUrl), 'resolveable': True}
                                hosters.append(hoster)

                elif 'kinoger' in sUrl:
                    if '/e/' in sUrl:
                        from resources.lib import jsunpacker
                        oRequest = cRequestHandler(sUrl.replace('/e/', '/play/'), ignoreErrors=True)
                        oRequest.addHeaderEntry('Referer', sUrl)
                        sHtmlContent = oRequest.request()
                        if sHtmlContent == '': continue
                        if 'p,a,c,k,e,d' in sHtmlContent:
                            sHtmlContent = jsunpacker.unpack(sHtmlContent)
                            pattern = 'sources\s*:\s*\[{file:\s*"([^"]+)'
                            isMatch, sUrl2 = cParser.parse(sHtmlContent, pattern)
                            oRequest = cRequestHandler(sUrl2[0], ignoreErrors=True)
                            oRequest.addHeaderEntry('Referer', 'https://kinoger.pw/')
                            oRequest.addHeaderEntry('Origin', 'https://kinoger.pw')
                            sHtmlContent = oRequest.request()
                            pattern = 'RESOLUTION=\d+x(\d+).*?(http[^"]+)#'
                            isMatch, aResult = cParser.parse(sHtmlContent, pattern)
                            for sQualy, sUrl in aResult:
                                hoster = {'link': sUrl, 'name': sQualy + ' Kinoger', 'resolveable': True}
                                hosters.append(hoster)
                    else:   # u'https://kinoger.re/v/elz45t-z8ymj7p8'
                        mediaId = sUrl.split("/")[-1:][0]
                        apiurl = 'https://kinoger.re/api/source/' + mediaId
                        oRequest = cRequestHandler(apiurl)
                        oRequest.addHeaderEntry('Referer', sUrl)
                        oRequest.addParameters('r', 'https://kinoger.com/')
                        oRequest.addParameters('d', 'kinoger.re')
                        sHtmlContent = oRequest.request()
                        pattern = '{"file":"(.+?)","label.+?([0-9px]+)"'
                        isMatch, aResult = cParser.parse(sHtmlContent, pattern)
                        for sUrl, sQualy in aResult:
                            hoster = {'link': sUrl, 'name': sQualy + ' Kinoger', 'resolveable': True}
                            hosters.append(hoster)

                elif 'start.u' in sUrl:
                    import json
                    t = sUrl.split('/')
                    token = encodeUrl(t[4] + ':' + t[5])
                    url2 = 'http://start.u-stream.in/ustGet.php?id=' + t[5] + '&token=' + token
                    oRequest = cRequestHandler(url2, ignoreErrors=True)
                    oRequest.addHeaderEntry('Referer', sUrl)
                    content = oRequest.request()
                    t = json.loads(content)
                    if 'url' in t and t['url']:
                        for u in t['url']:
                            a = decodeStr(u)
                            hoster = {'link': a, 'name': Qualy2(a) + cParser.urlparse(sUrl), 'resolveable': True}
                            hosters.append(hoster)
                else:
                    hoster = {'link': sUrl + 'DIREKT', 'name': cParser.urlparse(sUrl)}
                    hosters.append(hoster)
            except:
                pass
        if hosters:
            hosters.append('getHosterUrl')
        return hosters


def Qualy(q):
    if '360p' in q:
        return '360p'
    elif '480p' in q:
        return '480p'
    elif '720p' in q:
        return '720p'
    else:
        return '1080p'


def Qualy2(q):
    if '480-' in q:
        return '480p '
    elif '720-' in q:
        return '720p '
    elif '1080-' in q:
        return '1080p '
    else:
        return '360p '


def getHosterUrl(sUrl=False):
    if sUrl.startswith('//'):
        sUrl = 'https:' + sUrl
    if sUrl.endswith('DIREKT'):
        return [{'streamUrl': sUrl[:-6], 'resolved': False}]
    else:
        return [{'streamUrl': sUrl, 'resolved': True}]


def showSearch():
    sSearchText = cGui().showKeyBoard()
    if not sSearchText: return
    _search(False, sSearchText)
    cGui().setEndOfDirectory()


def _search(oGui, sSearchText):
    showEntries(URL_MAIN, oGui, sSearchText)


def toString(number, base):
    string = '0123456789abcdefghijklmnopqrstuvwxyz'
    if number < base:
        return string[number]
    else:
        return toString(number // base, base) + string[number % base]


def keys(s):
    if s == '1': return ('54A80Ibc3VBdefWGTSFg1X7hEYNijZU', 'kQl2mCnDoMpOq9rHsPt6uLvawRxJyKz')
    elif s == '2': return ('4YMHUe5OFZ7L2PEJ8fgKAh1RGiIj0kV', 'aTlNmCn3oBpDqSr9sbtWu6vcwdxXyQz')
    elif s == '3': return ('AN4YZVHTJEOeLS2fGaFghiKWjQMbIkl', 'Xmc1d3nCo7p5qBrUsDt9u8vRw6x0yPz')
    elif s == '4': return ('V6YD2ZNWaTefXgObhS3UcRAP4dIiJjK', 'k7l5mLnCoEpMqGrBsFtQuHv1w0x9y8z')
    elif s == '5': return ('OGAFaN985MDHTbYW7ceQfdIgZhJiXj3', 'kSl6mRn2oCpKqErPsUt1u0v4wLxByVz')
    elif s == '6': return ('cZXK8O3BS5NRedFPfLAg2U6hIiDj7VT', 'k9lQmJnWoGp1q0rCsatHuYvbw4xMyEz')
    elif s == '7': return ('UZQXTPHcVS7deEfWDgRMLh9iIa1Y0j2', 'klb3m8nOoBpNqKr5s6tJuAvCwGxFy4z')
    elif s == '8': return ('AZI4WCcKOdNJGF3YEa2eHfgb8hMiLjD', 'kUlPmBnSoVp5q7r6s9t1uTv0wQxRyXz')
    elif s == '9': return ('OWZYcP3adUNSbeCfJVghTQDRIiKjBkG', 'X5lMmFnAoLp1q7r6s0tHu2vEw9x4y8z')
    else: return ('', '')


def decodeStr(e):
    d = ''
    t0, t1 = keys(e[-1])
    e = e[:-1]
    for i in range(len(e)):
        for ii in range(len(t0)):
            if e[i] in t0[ii]:
                d = d + t1[ii]
            elif e[i] in t1[ii]:
                d = d + t0[ii]
    return cParser.unquotePlus(base64.b64decode(d[::-1] + '==').decode())


def encodeStr(e):
    d = ''
    k = str(random.randint(2, 7))
    t0, t1 = keys(k)
    e = cParser.quotePlus(e)
    e = base64.b64encode(e.encode())
    e = e.decode().replace('=', '')[::-1]
    for i in range(len(e)):
        for ii in range(len(t0)):
            if e[i] in t0[ii]:
                d = d + t1[ii]
            elif e[i] in t1[ii]:
                d = d + t0[ii]
    return d + k


def encodeUrl(e):
    n = ''
    a = random.randint(2, 9)
    t0, t1 = keys(str(a))
    t = a + 5
    for r in range(len(e)):
        n += toString(ord(e[r]), t)
        n += '!'
    n = base64.b64encode(n[:-1].encode()).decode().replace('=', '')
    e = ''
    for i in range(len(n)):
        for ii in range(len(t0)):
            if n[i] in t0[ii]:
                e = e + t1[ii]
            elif n[i] in t1[ii]:
                e = e + t0[ii]
    return encodeStr(e + str(a))


def aes(txt):
    import pyaes, base64
    from binascii import unhexlify
    key = unhexlify('0123456789abcdef0123456789abcdef')
    iv = unhexlify('abcdef9876543210abcdef9876543210')
    aes = pyaes.Encrypter(pyaes.AESModeOfOperationCBC(key, iv))
    return base64.b64encode(aes.feed(txt) + aes.feed()).decode()


def time2minutes(time):
    if type(time) == bytes:
        time = time.decode()
    t = time.split(":")
    minutes = float(t[0])*60 + float(t[1]) + float(t[2]) *0.05/3
    minutes = str(minutes).split(".")[0] if '.' in str(minutes) else str(minutes)
    return  minutes
