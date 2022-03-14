# -*- coding: UTF-8 -*-

#2021-07-15

import sys, re
import datetime, time, json
from resources.lib.tmdb import cTMDB
from resources.lib import control, workers, playcountDB, log_utils

_params = dict(control.parse_qsl(sys.argv[2].replace('?',''))) if len(sys.argv) > 1 else dict()

class seasons:
    def __init__(self):
        self.list = []
        self.lang = "de"
        self.sysmeta = _params['sysmeta']
        #self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours=5))
        #self.systime = (self.datetime).strftime('%Y%m%d%H%M%S%f')


    def get(self, params):
        try:
            data = json.loads(params['sysmeta'])
            self.title = data['title']
            if not 'number_of_seasons' in data or not data['number_of_seasons']: return
            number_of_seasons = data['number_of_seasons']

            tmdb_id = data['tmdb_id']
            tvdb_id = data['tvdb_id'] if 'tvdb_id' in data else None
            imdb_id = data['imdb_id'] if 'imdb_id' in data else None
            title = data['title']

            playcount = playcountDB.getPlaycount('tvshow', 'title', title, None, None)
            if playcount is None:
                #playcountDB.createEntry('tvshow', title, title, imdb_id, number_of_seasons, None, None, None)
                playcount = 0
            self.sysmeta = re.sub('"playcount": \d', '"playcount": %s' % playcount, self.sysmeta)

            for i in range(1, number_of_seasons+1):
                self.list.append({'tmdb_id': tmdb_id, 'tvdb_id': tvdb_id, 'season': i})
            self.worker()
            if self.list == None or len(self.list) == 0:    # nichts gefunden
                control.infoDialog("Nichts gefunden", time=8000)
            self.Directory(self.list)
            return self.list
        except:
            pass


    def worker(self):
        self.meta = []
        threads = []
        for i in range(0, len(self.list)):
            threads.append(workers.Thread(self.super_meta, i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        self.meta = sorted(self.meta, key=lambda k: k['season'])
        self.list = [i for i in self.meta] # falls noch eine Filterfunktion kommt


    def super_meta(self, i):
        try:
            meta = cTMDB().get_meta_seasons(self.list[i]['tmdb_id'] , self.list[i]['season'], advanced='true')
            try:
                playcount = playcountDB.getPlaycount('season', 'title', self.title, meta['season'], None)
                playcount = playcount if playcount else 0
                overlay = 7 if playcount > 0 else 6
                meta.update({'playcount': playcount, 'overlay': overlay})
            except:
                pass
            self.meta.append(meta)
        except:
            pass


    def Directory(self, items):
        if items == None or len(items) == 0:
            control.idle()
            sys.exit()
        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])

        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart = control.addonFanart()

        watchedMenu = "In %s [I]Gesehen[/I]" % control.addonName
        unwatchedMenu = "In %s [I]Ungesehen[/I]" % control.addonName
        pos = 0
        for i in items:
            try:
                meta = json.loads(self.sysmeta)
                sysmeta = json.loads(self.sysmeta)
                season = i['season']

                systitle = sysmeta['systitle']
                sysname = systitle + ' S%02d' % season
                sysmeta.update({'sysname': sysname})
                sysmeta.update({'season': season})
                sysmeta.update({'number_of_episodes': i['number_of_episodes']})
                sysmeta.update({'episodes': i['episodes']})

                _sysmeta = {k: v for k, v in sysmeta.items()}
                _sysmeta.pop('cast', None)
                _sysmeta.pop('episodes', None)
                _sysmeta = control.quote_plus(json.dumps(_sysmeta))

                label = 'Staffel %s - %s' % (season, sysmeta['title'])
                if datetime.datetime(*(time.strptime(i['premiered'], "%Y-%m-%d")[0:6])) > datetime.datetime.now():
                    label = '[COLOR=red][I]{}[/I][/COLOR]'.format(label) # ffcc0000

                poster = i['poster'] if 'poster' in i and 'http' in i['poster'] else sysmeta['poster']
                fanart = sysmeta['fanart'] if 'fanart' in sysmeta else addonFanart
                plot = i['plot'] if 'plot' in i and len(i['plot']) > 50 else sysmeta['plot']

                meta.update({'poster': poster})
                meta.update({'fanart': fanart})
                meta.update({'plot': plot})
                #if 'air_date' in i and i['air_date']: meta.update({'air_date': i['air_date']})
                if 'premiered' in i and i['premiered']: meta.update({'premiered': i['premiered']})

                item = control.item(label=label, offscreen=True)

                if sysmeta['playcount'] == 0: playcount = i['playcount']
                else: playcount = 1

                cm = []
                try:
                    if playcount == 1:
                        cm.append((unwatchedMenu, 'RunPlugin(%s?action=UpdatePlayCount&meta=%s&playCount=0)' % (sysaddon, _sysmeta)))
                        meta.update({'playcount': 1, 'overlay': 7})
                        sysmeta.update({'playcount': 1, 'overlay': 7})
                        pos = season +1
                        if len(items) == season: pos = season
                    else:
                        cm.append((watchedMenu, 'RunPlugin(%s?action=UpdatePlayCount&meta=%s&playCount=1)' % (sysaddon, _sysmeta)))
                        meta.update({'playcount': 0, 'overlay': 6})
                        sysmeta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass
                item.addContextMenuItems(cm)

                if 'cast' in meta and meta['cast']: item.setCast(meta['cast'])
                meta.pop('cast', None) # ersetzt durch item.setCast(i['cast'])
                item.setArt({'poster': poster, 'banner': addonBanner})
                item.setProperty('Fanart_Image', fanart)

                ## supported infolabels: https://codedocs.xyz/AlwinEsch/kodi/group__python__xbmcgui__listitem.html#ga0b71166869bda87ad744942888fb5f14
                # # # remove unsupported InfoLabels
                meta.pop('fanart', None)
                meta.pop('poster', None)
                meta.pop('imdb_id', None)
                meta.pop('tvdb_id', None)
                meta.pop('tmdb_id', None)
                meta.pop('number_of_seasons', None)
                meta.pop('number_of_episodes', None)
                meta.pop('originallanguage', None)
                meta.pop('sysname', None)
                meta.pop('systitle', None)
                meta.pop('year', None)
                # for test only
                #meta.pop('genre', None)
                #meta.pop('genres', None)

                item.setInfo(type='Video', infoLabels=meta)

                # gefakte Video/Audio Infos
                video_streaminfo = {'codec': 'h264', "width": 1920, "height": 1080}
                item.addStreamInfo('video', video_streaminfo)
                audio_streaminfo = {'codec': 'dts', 'channels': 6, 'language': 'de'}
                item.addStreamInfo('audio', audio_streaminfo)

                sysmeta = control.quote_plus(json.dumps(sysmeta))
                url = '%s?action=episodes&sysmeta=%s' % (sysaddon, sysmeta)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except Exception as e:
                #print(e) #TODO LOG
                pass

        control.content(syshandle, 'movies')
        control.directory(syshandle, cacheToDisc=True)

        # setzt Auswahl nach letzte als gesehen markierte Staffel -> Content: 'movies'
        if control.getSetting('status.position') == 'true':
            from resources.lib.utils import setPosition
            setPosition(pos, __name__, 'movies')
