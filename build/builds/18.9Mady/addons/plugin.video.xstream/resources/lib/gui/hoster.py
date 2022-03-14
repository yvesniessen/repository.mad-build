# -*- coding: utf-8 -*-
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.config import cConfig
from resources.lib.player import cPlayer
from resources.lib.tools import logger
import xbmc, xbmcgui, xbmcplugin

# try:
#     import resolveurl as resolver
# except:
#     import urlresolver as resolver

class cHosterGui:
    SITE_NAME = 'cHosterGui'

    def __init__(self):
        self.maxHoster = int(cConfig().getSetting('maxHoster', 100))
        self.dialog = False

    # TODO: unify parts of play, download etc.
    def _getInfoAndResolve(self, siteResult):
        oGui = cGui()
        params = ParameterHandler()
        # get data
        mediaUrl = params.getValue('sMediaUrl')
        fileName = params.getValue('MovieTitle')
        try:
            try:
                import resolveurl as resolver
            except:
                import urlresolver as resolver
            # resolve
            if siteResult:
                mediaUrl = siteResult.get('streamUrl', False)
                mediaId = siteResult.get('streamID', False)
                if mediaUrl:
                    logger.info('resolve: ' + mediaUrl)
                    link = mediaUrl if siteResult['resolved'] else resolver.resolve(mediaUrl)
                elif mediaId:
                    logger.info('resolve: hoster: %s - mediaID: %s' % (siteResult['host'], mediaId))
                    link = resolver.HostedMediaFile(host=siteResult['host'].lower(), media_id=mediaId).resolve()
                else:
                    oGui.showError('xStream', 'kein Hosterlink übergeben', 5)
                    return False
            elif mediaUrl:
                logger.info('resolve: ' + mediaUrl)
                link = resolver.resolve(mediaUrl)
            else:
                oGui.showError('xStream', 'kein Hosterlink übergeben', 5)
                return False
        except resolver.resolver.ResolverError as e:
            logger.error('ResolverError: %s' % e)
            oGui.showError('xStream', 'Stream nicht mehr verfügbar oder Link fehlerhaft', 7)
            return False
        # resolver response
        if link is not False:
            data = {'title': fileName, 'season': params.getValue('season'), 'episode': params.getValue('episode'), 'showTitle': params.getValue('TVShowTitle'), 'thumb': params.getValue('thumb'), 'link': link}
            return data
        return False

    def play(self, siteResult=False):
        logger.info('attempt to play file')
        data = self._getInfoAndResolve(siteResult)
        if not data:
            return False
        if self.dialog:
            try:
                self.dialog.close()
            except:
                pass

        logger.info('play file link: ' + str(data['link']))
        list_item = xbmcgui.ListItem(path=data['link'])
        info = {'Title': data['title']}
        if data['thumb']:
            list_item.setArt(data['thumb'])
        if data['showTitle']:
            info['Episode'] = data['episode']
            info['Season'] = data['season']
            info['TVShowTitle'] = data['showTitle']
        list_item.setInfo(type="Video", infoLabels=info)
        list_item.setProperty('IsPlayable', 'true')
        if cGui().pluginHandle > 0:
            xbmcplugin.setResolvedUrl(cGui().pluginHandle, True, list_item)
        else:
            xbmc.Player().play(data['link'], list_item)
        return cPlayer().startPlayer()

    def addToPlaylist(self, siteResult=False):
        oGui = cGui()
        logger.info('attempt addToPlaylist')
        data = self._getInfoAndResolve(siteResult)
        if not data: return False
        logger.info('addToPlaylist file link: ' + str(data['link']))
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setMediaUrl(data['link'])
        oGuiElement.setTitle(data['title'])
        if data['thumb']:
            oGuiElement.setThumbnail(data['thumb'])
        if data['showTitle']:
            oGuiElement.setEpisode(data['episode'])
            oGuiElement.setSeason(data['season'])
            oGuiElement.setTVShowTitle(data['showTitle'])
        if self.dialog:
            self.dialog.close()
        oPlayer = cPlayer()
        oPlayer.addItemToPlaylist(oGuiElement)
        oGui.showInfo('Playlist', 'Stream wurde hinzugefügt', 5)
        return True

    def download(self, siteResult=False):
        from resources.lib.download import cDownload
        logger.info('attempt download')
        data = self._getInfoAndResolve(siteResult)
        if not data: return False
        logger.info('download file link: ' + data['link'])
        if self.dialog:
            self.dialog.close()
        oDownload = cDownload()
        oDownload.download(data['link'], data['title'])
        return True

    def sendToPyLoad(self, siteResult=False):
        from resources.lib.handler.pyLoadHandler import cPyLoadHandler
        logger.info('attempt download with pyLoad')
        data = self._getInfoAndResolve(siteResult)
        if not data: return False
        cPyLoadHandler().sendToPyLoad(data['title'], data['link'])
        return True

    def sendToJDownloader(self, sMediaUrl=False):
        from resources.lib.handler.jdownloaderHandler import cJDownloaderHandler
        params = ParameterHandler()
        if not sMediaUrl:
            sMediaUrl = params.getValue('sMediaUrl')
        if self.dialog:
            self.dialog.close()
        logger.info('call send to JDownloader: ' + sMediaUrl)
        cJDownloaderHandler().sendToJDownloader(sMediaUrl)

    def sendToJDownloader2(self, sMediaUrl=False):
        from resources.lib.handler.jdownloader2Handler import cJDownloader2Handler
        params = ParameterHandler()
        if not sMediaUrl:
            sMediaUrl = params.getValue('sMediaUrl')
        if self.dialog:
            self.dialog.close()
        logger.info('call send to JDownloader2: ' + sMediaUrl)
        cJDownloader2Handler().sendToJDownloader2(sMediaUrl)

    def sendToMyJDownloader(self, sMediaUrl=False, sMovieTitle='xStream'):
        from resources.lib.handler.myjdownloaderHandler import cMyJDownloaderHandler
        params = ParameterHandler()
        if not sMediaUrl:
            sMediaUrl = params.getValue('sMediaUrl')
        sMovieTitle = params.getValue('MovieTitle')
        if not sMovieTitle:
            sMovieTitle = params.getValue('Title')
        if not sMovieTitle:  # only temporary
            sMovieTitle = params.getValue('sMovieTitle')
        if not sMovieTitle:
            sMovieTitle = params.getValue('title')
        if self.dialog:
            self.dialog.close()
        logger.info('call send to My.JDownloader: ' + sMediaUrl)
        cMyJDownloaderHandler().sendToMyJDownloader(sMediaUrl, sMovieTitle)

    def __getPriorities(self, hosterList, filter=True):

        # Sort hosters based on their resolvers priority.
        try:
            import resolveurl as resolver
        except:
            import urlresolver as resolver
        ranking = []
        # handles multihosters but is about 10 times slower
        for hoster in hosterList:
            # accept hoster which is marked as resolveable by sitePlugin
            if hoster.get('resolveable', False):
                ranking.append([0, hoster])
                continue

            try:
                hmf = resolver.HostedMediaFile(url=hoster['link'])
            except:
                continue
            if not hmf.valid_url():
                hmf = resolver.HostedMediaFile(host=hoster['name'].lower(), media_id='dummy')

            if len(hmf.get_resolvers()):
                priority = False
                for resolver in hmf.get_resolvers():
                    # prefer individual priority
                    if not resolver.isUniversal():
                        priority = resolver._get_priority()
                        break
                    if not priority:
                        priority = resolver._get_priority()
                if priority:
                    ranking.append([priority, hoster])
            elif not filter:
                ranking.append([999, hoster])

        if any('quality' in hoster[1] for hoster in ranking):
            pref_quli = cConfig().getSetting('preferedQuality')
            if pref_quli != '5' and any(
                    'quality' in hoster[1] and int(hoster[1]['quality']) == int(pref_quli) for hoster in ranking):
                ranking = sorted(ranking, key=lambda hoster: int('quality' in hoster[1] and hoster[1]['quality']) == int(pref_quli), reverse=True)
            else:
                ranking = sorted(ranking, key=lambda hoster: 'quality' in hoster[1] and int(hoster[1]['quality']), reverse=True)
        hosterQueue = []
        for i, hoster in ranking:
            hosterQueue.append(hoster)
        return hosterQueue

    def stream(self, playMode, siteName, function, url):
        self.dialog = xbmcgui.DialogProgress()
        self.dialog.create('xStream', 'get stream/hoster')
        # load site as plugin and run the function
        self.dialog.update(5, 'import plugin...')
        plugin = __import__(siteName, globals(), locals())
        function = getattr(plugin, function)
        self.dialog.update(10, 'catch links...')
        if url:
            siteResult = function(url)
        else:
            siteResult = function()
        self.dialog.update(40)
        if not siteResult:
            self.dialog.close()
            cGui().showInfo('xStream', 'stream/hoster not available')
            return
        # if result is not a list, make in one
        if not type(siteResult) is list:
            temp = [siteResult]
            siteResult = temp
        # field "name" marks hosters
        if 'name' in siteResult[0]:
            functionName = siteResult[-1]
            del siteResult[-1]
            if not siteResult:
                self.dialog.close()
                cGui().showInfo('xStream', 'no hoster available')
                return

            self.dialog.update(60, 'prepare hosterlist..')
            if (playMode != 'jd') and (playMode != 'jd2') and (playMode != 'pyload') and cConfig().getSetting('presortHoster') == 'true' and (playMode != 'myjd'):
                # filter and sort hosters
                siteResult = self.__getPriorities(siteResult)
            if not siteResult:
                self.dialog.close()
                cGui().showInfo('xStream', 'no supported hoster available')
                return False
            self.dialog.update(90)
            # self.dialog.close()
            if len(siteResult) > self.maxHoster:
                siteResult = siteResult[:self.maxHoster - 1]
            if cConfig().getSetting('hosterSelect') == 'List':
                self.showHosterFolder(siteResult, siteName, functionName)
                return
            if len(siteResult) > 1:
                # choose hoster
                siteResult = self._chooseHoster(siteResult)
                if not siteResult:
                    return
            else:
                siteResult = siteResult[0]
            # get stream links
            logger.info(siteResult['link'])
            function = getattr(plugin, functionName)
            siteResult = function(siteResult['link'])
            # if result is not a list, make in one
            if not type(siteResult) is list:
                temp = [siteResult]
                siteResult = temp
        # choose part
        if len(siteResult) > 1:
            siteResult = self._choosePart(siteResult)
            if not siteResult:
                logger.info('no part selected')
                return
        else:
            siteResult = siteResult[0]

        self.dialog = xbmcgui.DialogProgress()
        self.dialog.create('xStream', ' ')
        self.dialog.update(95, 'start opening stream..')
        if playMode == 'play':
            self.play(siteResult)
        elif playMode == 'download':
            self.download(siteResult)
        elif playMode == 'enqueue':
            self.addToPlaylist(siteResult)
        elif playMode == 'jd':
            self.sendToJDownloader(siteResult['streamUrl'])
        elif playMode == 'jd2':
            self.sendToJDownloader2(siteResult['streamUrl'])
        elif playMode == 'myjd':
            self.sendToMyJDownloader(siteResult['streamUrl'])
        elif playMode == 'pyload':
            self.sendToPyLoad(siteResult)

    def streamAuto(self, playMode, siteName, function):
        logger.info('auto stream initiated')
        self.dialog = xbmcgui.DialogProgress()
        self.dialog.create('xStream', 'get stream/hoster')
        # load site as plugin and run the function
        self.dialog.update(5, 'import plugin...')
        plugin = __import__(siteName, globals(), locals())
        function = getattr(plugin, function)
        self.dialog.update(10, 'catch links...')
        siteResult = function()
        if not siteResult:
            self.dialog.close()
            cGui().showInfo('xStream', 'stream/hoster not available')
            return False
        # if result is not a list, make in one
        if not type(siteResult) is list:
            temp = [siteResult]
            siteResult = temp
        # field "name" marks hosters
        if 'name' in siteResult[0]:
            self.dialog.update(90, 'prepare hosterlist..')
            functionName = siteResult[-1]
            del siteResult[-1]
            hosters = self.__getPriorities(siteResult)
            if not hosters:
                self.dialog.close()
                cGui().showInfo('xStream', 'no supported hoster available')
                return False
            if len(siteResult) > self.maxHoster:
                siteResult = siteResult[:self.maxHoster - 1]
            check = False
            self.dialog.create('xStream', 'try hosters...')
            total = len(hosters)
            for count, hoster in enumerate(hosters):
                if self.dialog.iscanceled() or xbmc.Monitor().abortRequested() or check: return
                percent = (count + 1) * 100 // total
                try:
                    logger.info('try hoster %s' % hoster['name'])
                    self.dialog.create('xStream', 'try hosters...')
                    self.dialog.update(percent, 'try hoster %s' % hoster['name'])
                    # get stream links
                    function = getattr(plugin, functionName)
                    siteResult = function(hoster['link'])
                    check = self.__autoEnqueue(siteResult, playMode)
                    if check:
                        return True
                except:
                    self.dialog.update(percent, 'hoster %s failed' % hoster['name'])
                    logger.error('playback with hoster %s failed' % hoster['name'])
        # field "resolved" marks streamlinks
        elif 'resolved' in siteResult[0]:
            for stream in siteResult:
                try:
                    if self.__autoEnqueue(siteResult, playMode):
                        self.dialog.close()
                        return True
                except:
                    pass

    def _chooseHoster(self, siteResult):
        dialog = xbmcgui.Dialog()
        titles = []
        for result in siteResult:
            if 'displayedName' in result:
                titles.append(str(result['displayedName']))
            else:
                titles.append(str(result['name']))
        index = dialog.select('Hoster wählen', titles)
        if index > -1:
            siteResult = siteResult[index]
            return siteResult
        else:
            logger.info('no hoster selected')
            return False

    def _choosePart(self, siteResult):
        self.dialog = xbmcgui.Dialog()
        titles = []
        for result in siteResult:
            titles.append(str(result['title']))
        index = self.dialog.select('Part wählen', titles)
        if index > -1:
            siteResult = siteResult[index]
            return siteResult
        else:
            return False

    def showHosterFolder(self, siteResult, siteName, functionName):
        oGui = cGui()
        total = len(siteResult)
        params = ParameterHandler()
        for hoster in siteResult:
            if 'displayedName' in hoster:
                name = hoster['displayedName']
            else:
                name = hoster['name']
            oGuiElement = cGuiElement(name, siteName, functionName)
            oGuiElement.setThumbnail(str(params.getValue('thumb')))
            params.setParam('url', hoster['link'])
            params.setParam('isHoster', 'true')
            oGui.addFolder(oGuiElement, params, iTotal=total, isHoster=True)
        oGui.setEndOfDirectory()

    def __autoEnqueue(self, partList, playMode):
        # choose part
        if not partList:
            return False
        for i in range(len(partList) - 1, -1, -1):
            try:
                if playMode == 'play' and i == 0:
                    if not self.play(partList[i]):
                        return False
                elif playMode == 'download':
                    self.download(partList[i])
                elif playMode == 'enqueue' or (playMode == 'play' and i > 0):
                    self.addToPlaylist(partList[i])
            except:
                return False
        logger.info('autoEnqueue successful')
        return True


class Hoster:
    def __init__(self, name, link):
        self.name = name
        self.link = link
