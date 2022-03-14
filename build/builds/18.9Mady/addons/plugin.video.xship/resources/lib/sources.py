# -*- coding: UTF-8 -*-

# 2022-01-09

import sys
import re,json,random,time
from resources.lib import workers, log_utils, utils, control
from resources.lib.control import py2_decode, py2_encode, quote_plus, parse_qsl
import resolveurl as resolver

from functools import reduce

# für self.sysmeta - zur späteren verwendung als meta
_params = dict(parse_qsl(sys.argv[2].replace('?',''))) if len(sys.argv) > 1 else dict()

class sources:
    def __init__(self):
        self.getConstants()
        self.sources = []
        self.current = int(time.time())
        if 'sysmeta' in _params: self.sysmeta = _params['sysmeta'] # string zur späteren verwendung als meta
        self.watcher = False

    def get(self, params):
        data = json.loads(params['sysmeta'])
        self.mediatype = data.get('mediatype')
        self.aliases = data.get('aliases') if 'aliases' in data else []

        title = py2_encode(data.get('title'))
        originaltitle = py2_encode(data.get('originaltitle')) if 'originaltitle' in data else title
        year = data.get('year') if 'year' in data else None
        imdb = data.get('imdb_id') if 'imdb_id' in data else data.get('imdbnumber') if 'imdbnumber' in data else None
        if not imdb and 'imdb' in data: imdb = data.get('imdb')
        tmdb = data.get('tmdb_id') if 'tmdb_id' in data else None
        #if tmdb and not imdb: print 'hallo' #TODO
        season = data.get('season') if 'season' in data else 0
        episode = data.get('episode') if 'episode' in data else 0
        premiered = data.get('premiered') if 'premiered' in data else None
        meta = params['sysmeta']
        select = data.get('select') if 'select' in data else None
        return title, year, imdb, season, episode, originaltitle, premiered, meta, select

    def play(self, params):
        title, year, imdb, season, episode, originaltitle, premiered, meta, select = self.get(params)
        try:
            url = None
            #Liste der gefundenen Streams
            items = self.getSources(title, year, imdb, season, episode, originaltitle, premiered)

            select = control.getSetting('hosts.mode') if select == None else select
            select = '1' if control.getSetting('downloads') == 'true' and not (control.getSetting('download.movie.path') == '' or control.getSetting('download.tv.path') == '') else select

            # TODO überprüfen wofür mal gedacht
            if control.window.getProperty('PseudoTVRunning') == 'True':
                return control.resolveUrl(int(sys.argv[1]), True, control.item(path=str(self.sourcesDirect(items))))

            if len(items) > 0:
                # Auswahl Verzeichnis
                if select == '1' and 'plugin' in control.infoLabel('Container.PluginName'):
                    control.window.clearProperty(self.itemsProperty)
                    control.window.setProperty(self.itemsProperty, json.dumps(items))
                    
                    control.window.clearProperty(self.metaProperty)
                    control.window.setProperty(self.metaProperty, meta)
                    control.sleep(200)
                    return control.execute('Container.Update(%s?action=addItem&title=%s)' % (sys.argv[0], quote_plus(title)))
                # Auswahl Dialog
                elif select == '0' or select == '1':
                    url = self.sourcesDialog(items)
                # Autoplay
                else:
                    url = self.sourcesDirect(items)

            if url == None or url == 'close://': return self.errorForSources()

            try: meta = json.loads(meta)
            except: pass

            from resources.lib.player import player
            player().run(title, url, meta)
        except Exception as e:
            log_utils.log('Error %s' % str(e), log_utils.LOGERROR)


# Liste gefundene Streams Indexseite|Hoster
    def addItem(self, title):
        control.playlist.clear()

        items = control.window.getProperty(self.itemsProperty)
        items = json.loads(items)
        if items == None or len(items) == 0: control.idle() ; sys.exit()

        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])
        systitle = sysname = quote_plus(title)

        downloads = True if control.getSetting('downloads') == 'true' and not (control.getSetting('download.movie.path') == '' or control.getSetting('download.tv.path') == '') else False

        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart, settingFanart = control.addonFanart(), control.getSetting('fanart')

        meta = control.window.getProperty(self.metaProperty)
        meta = json.loads(meta)

        if 'backdrop_url' in meta and 'http' in meta['backdrop_url']: fanart = meta['backdrop_url']
        elif 'fanart' in meta and 'http' in meta['fanart']: fanart = meta['fanart']
        else: fanart = addonFanart

        if 'cover_url' in meta and 'http' in meta['cover_url']: poster = meta['cover_url']
        elif 'poster' in meta and 'http' in meta['poster']: poster = meta['poster']
        else:  poster = addonPoster
        sysimage = poster

        if 'season' in meta and 'episode' in meta:
            sysname += quote_plus(' S%02dE%02d' % (int(meta['season']), int(meta['episode'])))
        elif 'year' in meta:
            sysname += quote_plus(' (%s)' % meta['year'])

        for i in range(len(items)):
            try:
                label = items[i]['label']
                syssource = quote_plus(json.dumps([items[i]]))
                item = control.item(label=label, offscreen=True)

                cm = []
                if downloads:
                    cm.append(("Download", 'RunPlugin(%s?action=download&name=%s&image=%s&source=%s)' % (sysaddon, sysname, sysimage, syssource)))
                item.addContextMenuItems(cm)

                ## Quality Video Stream from source.append quality - items[i]['quality']
                video_streaminfo ={}
                if "4k" in items[i]['quality'].lower():
                    video_streaminfo.update({'width': 3840, 'height': 2160})
                elif "1080p" in items[i]['quality'].lower():
                    video_streaminfo.update({'width': 1920, 'height': 1080})
                elif "hd" in items[i]['quality'].lower() or "720p" in items[i]['quality'].lower():
                    video_streaminfo.update({'width': 1280,'height': 720})
                else:
                    video_streaminfo.update({"width": 720, "height": 576})

                ## Codec for Video Stream from extra info - items[i]['info']
                if 'hevc' in items[i]['label'].lower():
                    video_streaminfo.update({'codec': 'hevc'})
                elif '265' in items[i]['label'].lower():
                    video_streaminfo.update({'codec': 'h265'})
                elif 'mkv' in items[i]['label'].lower():
                    video_streaminfo.update({'codec': 'mkv'})
                elif 'mp4' in items[i]['label'].lower():
                    video_streaminfo.update({'codec': 'mp4'})
                else:
                    video_streaminfo.update({'codec': 'h264'})

                item.addStreamInfo('video', video_streaminfo)

                ## Quality & Channels Audio Stream from extra info - items[i]['info']
                audio_streaminfo = {}
                if 'dts' in items[i]['label'].lower():
                    audio_streaminfo.update({'codec': 'dts'})                
                elif 'plus' in items[i]['label'].lower() or 'e-ac3' in items[i]['label'].lower():
                    audio_streaminfo.update({'codec': 'eac3'})
                elif 'dolby' in items[i]['label'].lower() or 'ac3' in items[i]['label'].lower():
                    audio_streaminfo.update({'codec': 'ac3'})                
                else:
                    audio_streaminfo.update({'codec': 'aac'})

                ## Channel update ##
                if '7.1' in items[i].get('info','').lower():
                    audio_streaminfo.update({'channels': 8})
                elif '5.1' in items[i].get('info','').lower():
                    audio_streaminfo.update({'channels': 6})
                else:
                    audio_streaminfo.update({'channels': 2})
                    
                item.addStreamInfo('audio', audio_streaminfo)

                # TODO
                # if 'cast' in meta and meta['cast']: item.setCast(meta['cast'])
                # meta.pop('cast', None)  # ersetzt durch item.setCast(i['cast'])

                item.setArt({'poster': poster, 'banner': addonBanner})
                if settingFanart: item.setProperty('Fanart_Image', fanart)

                ##https: // codedocs.xyz / AlwinEsch / kodi / group__python__xbmcgui__listitem.html  # ga0b71166869bda87ad744942888fb5f14

                name = '%s%sStaffel: %s   Episode: %s' % (title, "\n", meta['season'], meta['episode']) if 'season' in meta else title
                plot = meta['plot'] if 'plot' in meta and len(meta['plot'].strip()) >= 1 else ''
                plot = '[COLOR blue]%s[/COLOR]%s%s' % (name, "\n\n", py2_encode(plot))

                # # # remove unsupported InfoLabels
                meta.pop('number_of_seasons', None)
                meta.pop('imdb_id', None)
                meta.pop('tvdb_id', None)
                meta.pop('tmdb_id', None)

                if 'duration' in meta:
                    infolable = {'plot': plot,'duration': meta['duration']}
                else:
                    infolable = {'plot': plot}

                item.setInfo(type='Video', infoLabels=infolable)
                item.setProperty('IsPlayable', 'true')

                url = "%s?action=playItem&title=%s&source=%s" % (sysaddon, systitle, syssource)

                ## Notwendig fÃ¼r Library Exporte ##
                ## Amazon Scraper Details ##
                if "amazon" in label.lower():
                    aid = re.search(r'asin%3D(.*?)%22%2C', url)
                    url = "plugin://plugin.video.amazon-test/?mode=PlayVideo&asin=" + aid.group(1)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=False)
            except:
                pass

        control.content(syshandle, 'videos')
        control.directory(syshandle, cacheToDisc=True)


    def playItem(self, title, source):
        isDebug = False
        if isDebug: log_utils.log('start playItem', log_utils.LOGWARNING)
        try:
            meta = control.window.getProperty(self.metaProperty)
            meta = json.loads(meta)

            header = control.addonInfo('name')
            control.idle() #ok
            progressDialog = control.progressDialog if control.getSetting('progress.dialog') == '0' else control.progressDialogBG
            progressDialog.create(header, '')
            progressDialog.update(0)

            item = json.loads(source)[0]
            #if isDebug: log_utils.log('playItem 237', log_utils.LOGWARNING)
            if item['source'] == None: raise Exception()
            w = workers.Thread(self.sourcesResolve, item)
            w.start()
            waiting_time = 30
            while waiting_time > 0:
                try:
                    if control.abortRequested: return sys.exit()
                    if progressDialog.iscanceled(): return progressDialog.close()
                except:
                    pass
                if not w.is_alive(): break
                time.sleep(0.5)
                waiting_time = waiting_time - 0.5
                progressDialog.update(int(100 - 100. / 30 * waiting_time), str(item['label']))
                #if isDebug: log_utils.log('playItem 252', log_utils.LOGWARNING)
                if control.condVisibility('Window.IsActive(virtualkeyboard)') or \
                        control.condVisibility('Window.IsActive(yesnoDialog)'):
                        # or control.condVisibility('Window.IsActive(PopupRecapInfoWindow)'):
                    waiting_time = waiting_time + 0.5  # dont count down while dialog is presented
                if not w.is_alive(): break

            try: progressDialog.close()
            except: pass
            if isDebug: log_utils.log('playItem 261', log_utils.LOGWARNING)
            control.execute('Dialog.Close(virtualkeyboard)')
            control.execute('Dialog.Close(yesnoDialog)')

            if isDebug: log_utils.log('playItem url: %s' % self.url, log_utils.LOGWARNING)
            if self.url == None:
                #self.errorForSources()
                return

            from resources.lib.player import player
            player().run(title, self.url, meta)
            return self.url
        except Exception as e:
            log_utils.log('Error %s' % str(e), log_utils.LOGERROR)


    def getSources(self, title, year, imdb, season, episode, originaltitle, premiered, quality='HD', timeout=30):
        control.idle() #ok
        progressDialog = control.progressDialog if control.getSetting('progress.dialog') == '0' else control.progressDialogBG
        progressDialog.create(control.addonInfo('name'), '')
        progressDialog.update(0)
        progressDialog.update(0, "Quellen werden vorbereitet")

        sourceDict = self.sourceDict
        sourceDict = [(i[0], i[1], i[1].priority) for i in sourceDict]
        random.shuffle(sourceDict)
        sourceDict = sorted(sourceDict, key=lambda i: i[2])

        content = 'movies' if season == 0 or season == '' or season == None else 'shows'
        aliases, localtitle = utils.getAliases(imdb, content)
        if localtitle and title != localtitle and originaltitle != localtitle:
            if not title in aliases: aliases.append(title)
            title = localtitle
        for i in self.aliases: aliases.append(i)
        titles = utils.get_titles_for_search(title, originaltitle, aliases)

        threads = []
        for i in sourceDict: threads.append(
            workers.Thread(self._getSource, titles, year, season, episode, imdb, i[0], i[1]))

        s = [i[0] + (i[1],) for i in zip(sourceDict, threads)]
        s = [(i[3].getName(), i[0], i[2]) for i in s]
        sourcelabelDict = dict([(i[0], i[1].upper()) for i in s])

        [i.start() for i in threads]

        string4 = "Total"

        try: timeout = int(control.getSetting('scrapers.timeout'))
        except: pass
        
        quality = control.getSetting('hosts.quality')
        if quality == '': quality = '0'

        source_4k = 0
        source_1080 = 0
        source_720 = 0
        source_sd = 0
        total = d_total = 0
        total_format = '[COLOR %s][B]%s[/B][/COLOR]'
        pdiag_format = ' 4K: %s | 1080p: %s | 720p: %s | SD: %s | %s: %s                                         '.split('|')

        for i in range(0, 4 * timeout):
            try:
                if control.abortRequested: return sys.exit()
                try:
                    if progressDialog.iscanceled(): break
                except:
                    pass

                if len(self.sources) > 0:
                    if quality in ['0']:
                        source_4k = len([e for e in self.sources if e['quality'] == '4K'])
                        source_1080 = len([e for e in self.sources if e['quality'] in ['1440p','1080p']])
                        source_720 = len([e for e in self.sources if e['quality'] in ['720p','HD']])
                        source_sd = len([e for e in self.sources if e['quality'] not in ['4K','1440p','1080p','720p','HD']])
                    elif quality in ['1']:
                        source_1080 = len([e for e in self.sources if e['quality'] in ['1440p','1080p']])
                        source_720 = len([e for e in self.sources if e['quality'] in ['720p','HD']])
                        source_sd = len([e for e in self.sources if e['quality'] not in ['4K','1440p','1080p','720p','HD']])
                    elif quality in ['2']:
                        source_1080 = len([e for e in self.sources if e['quality'] in ['1080p']])
                        source_720 = len([e for e in self.sources if e['quality'] in ['720p','HD']])
                        source_sd = len([e for e in self.sources if e['quality'] not in ['4K','1440p','1080p','720p','HD']])
                    elif quality in ['3']:
                        source_720 = len([e for e in self.sources if e['quality'] in ['720p','HD']])
                        source_sd = len([e for e in self.sources if e['quality'] not in ['4K','1440p','1080p','720p','HD']])
                    else:
                        source_sd = len([e for e in self.sources if e['quality'] not in ['4K','1440p','1080p','720p','HD']])
                    
                    total = source_4k + source_1080 + source_720 + source_sd

                source_4k_label = total_format % ('red', source_4k) if source_4k == 0 else total_format % ('lime', source_4k)
                source_1080_label = total_format % ('red', source_1080) if source_1080 == 0 else total_format % ('lime', source_1080)
                source_720_label = total_format % ('red', source_720) if source_720 == 0 else total_format % ('lime', source_720)
                source_sd_label = total_format % ('red', source_sd) if source_sd == 0 else total_format % ('lime', source_sd)
                source_total_label = total_format % ('red', total) if total == 0 else total_format % ('lime', total)

                try:
                    info = [sourcelabelDict[x.getName()] for x in threads if x.is_alive() == True]

                    percent = int(100 * float(i) / (2 * timeout) + 0.5)

                    if quality in ['0']:
                        line1 = '|'.join(pdiag_format) % (source_4k_label, source_1080_label, source_720_label, source_sd_label, str(string4), source_total_label)
                    elif quality in ['1']:
                        line1 = '|'.join(pdiag_format[1:]) % (source_1080_label, source_720_label, source_sd_label, str(string4), source_total_label)
                    elif quality in ['2']:
                        line1 = '|'.join(pdiag_format[1:]) % (source_1080_label, source_720_label, source_sd_label, str(string4), source_total_label)
                    elif quality in ['3']:
                        line1 = '|'.join(pdiag_format[2:]) % (source_720_label, source_sd_label, str(string4), source_total_label)
                    else:
                        line1 = '|'.join(pdiag_format[3:]) % (source_sd_label, str(string4), source_total_label)

                    if (i / 2) < timeout:
                        string = "Verbleibende Indexseiten: %s"
                    else:
                        string = 'Waiting for: %s'

                    if len(info) > 6: line = line1 + string % (str(len(info)))
                    elif len(info) > 1: line = line1 + string % (', '.join(info))
                    elif len(info) == 1: line = line1 + string % (''.join(info))
                    else: line = line1 + 'Suche beendet!'

                    progressDialog.update(max(1, percent), line)
                    if len(info) == 0: break

                except Exception as e:
                    log_utils.log('Exception Raised: %s' % str(e), log_utils.LOGERROR)

                time.sleep(0.5)
            except:
                pass

        time.sleep(1)

        try: progressDialog.close()
        except: pass

        self.sourcesFilter()
        return self.sources


    def _getSource(self, titles, year, season, episode, imdb, source, call):
        try:
            sources = call.run(titles, year, season, episode, imdb, self.hostDict)
            if sources == None or sources == []: raise Exception()
            sources = [json.loads(t) for t in set(json.dumps(d, sort_keys=True) for d in sources)]
            for i in sources:
                i.update({'provider': source})
                if not 'priority' in i: i.update({'priority': 1})
            self.sources.extend(sources)
        except:
            pass


    def sourcesFilter(self):
        self.sources = [i for i in self.sources if i['source'].split('.')[0] not in str(self.hostblockDict)] # Hoster ausschließen (Liste)

        quality = control.getSetting('hosts.quality')
        if quality == '': quality = '0'

        random.shuffle(self.sources)

        for i in range(len(self.sources)):
            q = self.sources[i]['quality']            
            if q.lower() == 'hd': self.sources[i].update({'quality': '720p'})

        filter = []
        if quality in ['0']: filter += [i for i in self.sources if i['quality'] == '4K']
        if quality in ['0', '1']: filter += [i for i in self.sources if i['quality'] == '1440p']
        if quality in ['0', '1', '2']: filter += [i for i in self.sources if i['quality'] == '1080p']
        if quality in ['0', '1', '2', '3']: filter += [i for i in self.sources if i['quality'] == '720p']
        #filter += [i for i in self.sources if i['quality'] in ['SD', 'SCR', 'CAM']]
        filter += [i for i in self.sources if i['quality'] not in ['4k', '1440p', '1080p', '720p']]
        self.sources = filter

        provider = 'true' if control.getSetting('hosts.sort.provider') == 'true' else 'false'
        if provider == 'true':
            self.sources = sorted(self.sources, key=lambda k: k['provider'])

        if control.getSetting('hosts.sort.priority') == 'true' and self.mediatype == 'tvshow': self.sources = sorted(self.sources, key=lambda k: k['priority'], reverse=True)

        if str(control.getSetting('hosts.limit')) == 'true':
            self.sources = self.sources[:int(control.getSetting('hosts.limit.num'))]
        else:
            self.sources = self.sources[:100]

        for i in range(len(self.sources)):
            p = self.sources[i]['provider']
            q = self.sources[i]['quality']
            s = self.sources[i]['source']
            s = s.rsplit('.', 1)[0]
            l = self.sources[i]['language']

            try: f = (' | '.join(['[I]%s [/I]' % info.strip() for info in self.sources[i]['info'].split('|')]))
            except: f = ''

            label = '%02d | [B]%s[/B] | ' % (int(i + 1), p)
            if q in ['4K', '1440p', '1080p', '720p']: label += '%s | [B][I]%s [/I][/B] | %s' % (s, q, f)
            elif q == 'SD': label += '%s | %s' % (s, f)
            else: label += '%s | %s | [I]%s [/I]' % (s, f, q)
            label = label.replace('| 0 |', '|').replace(' | [I]0 [/I]', '')
            label = re.sub('\[I\]\s+\[/I\]', ' ', label)
            label = re.sub('\|\s+\|', '|', label)
            label = re.sub('\|(?:\s+|)$', '', label)

            self.sources[i]['label'] = label.upper()

            # ## EMBY shown as premium link ##
            # if self.sources[i]['provider']=="emby" or self.sources[i]['provider']=="amazon" or self.sources[i]['provider']=="netflix" or self.sources[i]['provider']=="maxdome":
            #     prem_identify = 'blue'
            #     self.sources[i]['label'] = ('[COLOR %s]' % (prem_identify)) + label.upper() + '[/COLOR]'

        self.sources = [i for i in self.sources if 'label' in i]
        return self.sources


    def sourcesResolve(self, item, info=False):
        try:
            self.url = None
            url = item['url']
            #d = item['debrid']
            direct = item['direct']
            local = item.get('local', False)
            provider = item['provider']
            call = [i[1] for i in self.sourceDict if i[0] == provider][0]
            url = call.resolve(url)

            if url == None or (not '://' in str(url) and not local):
                log_utils.log('Kein Video Link gefunden: Provider %s / %s / %s ' % (item['provider'], item['source'] , str(item['source'])), log_utils.LOGERROR)
                raise Exception()

            if not direct == True:
                hmf = resolver.HostedMediaFile(url=url, include_disabled=True, include_universal=False)
                if hmf.valid_url():
                    url = hmf.resolve()
                    if url == False or url == None: raise Exception()

            if not utils.test_stream(url):
                log_utils.log('URL Test Error: %s' % url, log_utils.LOGERROR)
                raise Exception()

            url = utils.m3u8_check(url)

            if url:
                self.url = url
                return url
            else:
                raise Exception()
        except:
            if info: self.errorForSources()
            return


    def sourcesDialog(self, items):
        labels = [i['label'] for i in items]

        select = control.selectDialog(labels)
        if select == -1: return 'close://'

        next = [y for x,y in enumerate(items) if x >= select]
        prev = [y for x,y in enumerate(items) if x < select][::-1]

        items = [items[select]]
        items = [i for i in items+next+prev][:40]

        header = control.addonInfo('name')
        header2 = header.upper()

        progressDialog = control.progressDialog if control.getSetting('progress.dialog') == '0' else control.progressDialogBG
        progressDialog.create(header, '')
        progressDialog.update(0)

        block = None

        try:
            for i in range(len(items)):
                try:
                    if items[i]['source'] == block: raise Exception()

                    w = workers.Thread(self.sourcesResolve, items[i])
                    w.start()

                    try:
                        if progressDialog.iscanceled(): break
                        progressDialog.update(int((100 / float(len(items))) * i), str(items[i]['label']))
                    except:
                        progressDialog.update(int((100 / float(len(items))) * i), str(header2) + str(items[i]['label']))

                    waiting_time = 30
                    while waiting_time > 0:
                        try:
                            if control.abortRequested: return sys.exit() #xbmc.Monitor().abortRequested()
                            if progressDialog.iscanceled(): return progressDialog.close()
                        except:
                            pass

                        if not w.is_alive(): break
                        time.sleep(0.5)

                        waiting_time = waiting_time - 0.5

                        if control.condVisibility('Window.IsActive(virtualkeyboard)') or \
                                control.condVisibility('Window.IsActive(yesnoDialog)') or \
                                control.condVisibility('Window.IsActive(ProgressDialog)'):
                            waiting_time = waiting_time + 0.5 #dont count down while dialog is presented ## control.condVisibility('Window.IsActive(PopupRecapInfoWindow)') or \

                    if w.is_alive(): block = items[i]['source']

                    if self.url == None: raise Exception()

                    self.selectedSource = items[i]['label']

                    try: progressDialog.close()
                    except: pass

                    control.execute('Dialog.Close(virtualkeyboard)')
                    control.execute('Dialog.Close(yesnoDialog)')
                    return self.url
                except:
                    pass

            try: progressDialog.close()
            except: pass

        except Exception as e:
            try: progressDialog.close()
            except: pass
            log_utils.log('Error %s' % str(e), log_utils.LOGINFO)


    def sourcesDirect(self, items):
        filter = [i for i in items if i['source'].lower() in self.hostcapDict and i['debrid'] == '']
        items = [i for i in items if not i in filter]

        items = [i for i in items if ('autoplay' in i and i['autoplay'] == True) or not 'autoplay' in i]

        u = None

        header = control.addonInfo('name')
        header2 = header.upper()

        try:
            control.sleep(1000)

            progressDialog = control.progressDialog if control.getSetting('progress.dialog') == '0' else control.progressDialogBG
            progressDialog.create(header, '')
            progressDialog.update(0)
        except:
            pass

        for i in range(len(items)):
            try:
                if progressDialog.iscanceled(): break
                progressDialog.update(int((100 / float(len(items))) * i), str(items[i]['label']))
            except:
                progressDialog.update(int((100 / float(len(items))) * i), str(header2) + str(items[i]['label']))

            try:
                if control.abortRequested: return sys.exit()

                url = self.sourcesResolve(items[i])
                if u == None: u = url
                if not url == None: break
            except:
                pass

        try: progressDialog.close()
        except: pass

        return u

    def errorForSources(self):
        control.infoDialog("Keine Streams verfügbar oder ausgewählt", sound=False, icon='INFO')
  
    def getTitle(self, title):
        title = utils.normalize(title)
        return title

    def getConstants(self):
        self.itemsProperty = '%s.container.items' % control.Addon.getAddonInfo('id')
        self.metaProperty = '%s.container.meta'  % control.Addon.getAddonInfo('id')
        from scrapers import sources
        self.sourceDict = sources()

        self.hostblockDict = ['gounlimited.to, playtube.ws'] # permanent
        filterHoster = control.getSetting('hosts.filter').split(',')
        if len(filterHoster) <= 1: filterHoster = control.getSetting('hosts.filter').split()
        for i in filterHoster: self.hostblockDict.append(i.lower())

        try:
            self.hostDict = resolver.relevant_resolvers(order_matters=True)
            self.hostDict = [i.domains for i in self.hostDict if not '*' in i.domains]
            self.hostDict = [i.lower() for i in reduce(lambda x, y: x+y, self.hostDict)]
            self.hostDict = [x for y,x in enumerate(self.hostDict) if x not in self.hostDict[:y]]
            self.hostDict = [i for i in self.hostDict if i.split('.')[0] not in str(self.hostblockDict)]
        except:
            self.hostDict = []
#TODO
        #self.hostprDict = ['1fichier.com', 'filefactory.com', 'filefreak.com', 'multiup.org', 'nitroflare.com', 'oboom.com', 'rapidgator.net', 'rg.to', 'turbobit.net', 'uploaded.net', 'uploaded.to', 'uploadgig.com', 'ul.to', 'filefactory.com', 'nitroflare.com', 'turbobit.net', 'uploadrocket.net']
        self.hostprDict = []
        self.hostcapDict = ['flashx.tv', 'flashx.to', 'flashx.sx', 'flashx.bz', 'flashx.cc', 'vshare.eu', 'hugefiles.net', 'kingfiles.net', 'vidup.me', 'streamin.to', 'torba.se', 'jetload.net', 'vev.io', 'vev.red', 'thevideos.ga', 'thevideo.me', 'uptobox.com', 'uptostream.com']

