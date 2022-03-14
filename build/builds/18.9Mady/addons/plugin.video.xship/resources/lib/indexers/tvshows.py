# -*- coding: UTF-8 -*-

#2021-07-15

import sys
from six import iteritems
import datetime, time, json
from resources.lib.tmdb import cTMDB
from resources.lib.indexers import navigator
from resources.lib import searchDB, playcountDB, art, workers, control

_params = dict(control.parse_qsl(sys.argv[2].replace('?',''))) if len(sys.argv) > 1 else dict()

class tvshows:
    def __init__(self):
        self.list = []
        self.meta = []
        self.total_pages = 0
        self.next_pages = 0
        self.query = ''
        self.activeSearchDB = 'TMDB'
        #self.setSearchDB() # TODO different search providers
        self.playcount = 0

    def get(self, params):
        try:
            self.next_pages = int(params.get('page')) + 1
            self.query = params.get('query')
            self.list, self.total_pages = cTMDB().search_term('tvshow', params.get('query'), params.get('page'))
            if self.list == None or len(self.list) == 0:  # nichts gefunden
                return control.infoDialog("Nichts gefunden1", time=2000)
            self.getDirectory(params)
        except:
            return

    def getDirectory(self, params):
        try:
            if params.get('next_pages'): self.next_pages = params.get('next_pages')
            if params.get('total_pages'): self.total_pages = params.get('total_pages')
            if params.get('list'): self.list = params.get('list')
            self.worker()
            if self.list == None or len(self.list) == 0:    #nichts gefunden
                return control.infoDialog("Nichts gefunden", time=2000)
            self.Directory(self.list)
            return self.list
        except:
            return

    def search(self):
        # TODO different search providers
        #navigator.navigator().addDirectoryItem("DB für Suche auswählen", 'tvChangeSearchDB', self.activeSearchDB + '.png', 'DefaultTVShows.png', isFolder=False)
        navigator.navigator().addDirectoryItem("[B]Serien - neue Suche %s[/B]" % self.activeSearchDB, 'searchNew&table=tvshows', self.activeSearchDB + '_search.png', 'DefaultTVShows.png', isFolder=False)
        match = searchDB.getSearchTerms('tvshows')
        lst = []
        delete_option = False
        for i in match:
            term = control.py2_encode(i['term'])
            if term not in lst:
                delete_option = True
                navigator.navigator().addDirectoryItem(term, 'tvshows&page=1&query=%s' % control.quote_plus(term), '_search.png',
                                                       'DefaultTVShows.png', isFolder=True,
                                                       context=("Suchanfrage löschen", 'searchDelTerm&table=tvshows&name=%s' % term))
                lst += [(term)]

        if delete_option:
            navigator.navigator().addDirectoryItem("[B]Suchverlauf löschen[/B]", 'searchClear&table=tvshows', 'tools.png', 'DefaultAddonProgram.png', isFolder=False)
        navigator.navigator()._endDirectory('', False) # addons  videos  files

# TODO different search providers
    # def setSearchDB(self, new=''):
    #     if control.getSetting('active.SearchDB.tvshow'):
    #         _searchDB = control.getSetting('active.SearchDB.tvshow')
    #         if new != '':
    #             control.setSetting('active.SearchDB.tvshow', new)
    #             _searchDB = new
    #         self.activeSearchDB  = _searchDB
    #     else:
    #         control.setSetting('active.SearchDB.tvshow', 'tmdb')
    #         self.activeSearchDB = 'tmdb'
    #
    # def changeSearchDB(self):
    #     active = control.getSetting('active.SearchDB.tvshow')
    #     data = []
    #     for i in ['tmdb', 'trakt']:
    #         if i == active: continue
    #         data.append('wechseln zu ' + i.upper())
    #     index = control.dialog.contextmenu(data)
    #     if index == -1:
    #         return
    #     term = data[index].lower().split()[-1]
    #     self.setSearchDB(term)
    #     url = '%s?action=tvSearch' % sys.argv[0]
    #     control.execute('Container.Update(%s)' % url)


    def Directory(self, items):
        if items is None or len(items) == 0:
            control.idle()
            sys.exit()
        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])

        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart, settingFanart = control.addonFanart(), control.getSetting('fanart')

        watchedMenu = "In %s [I]Gesehen[/I]" % control.addonName
        unwatchedMenu = "In %s [I]Ungesehen[/I]" % control.addonName
        for i in items:
            try:
                meta = dict((k, v) for k, v in iteritems(i))

                title = i['title'] if 'title' in i else i['originaltitle']
                try:
                    label = '%s (%s)' % (title, i['year'])  # show in list
                except:
                    label = title

                if 'premiered' in i:
                    if datetime.datetime(*(time.strptime(i['premiered'], "%Y-%m-%d")[0:6])) > datetime.datetime.now():
                        label = '[COLOR=red][I]{}[/I][/COLOR]'.format(label) # ffcc0000
                else:
                    label = '[COLOR=red][I]{}[/I][/COLOR]'.format(label)

                poster = i['poster'] if 'poster' in i and 'http' in i['poster'] else addonPoster
                fanart = i['fanart'] if 'fanart' in i and 'http' in i['fanart'] else addonFanart
                meta.update({'poster': poster})
                meta.update({'fanart': fanart})

                sysmeta = dict((k, v) for k, v in iteritems(meta))
                systitle = sysname = title
                sysmeta.update({'systitle': systitle})
                sysmeta.update({'sysname': sysname})

                _sysmeta = control.quote_plus(json.dumps(sysmeta))

                item = control.item(label=label, offscreen=True)

                if sysmeta['playcount'] == 0:
                    playcount = i['playcount']
                else:
                    playcount = 1

                cm = []
                try:
                    if playcount == 1:
                        cm.append((unwatchedMenu, 'RunPlugin(%s?action=UpdatePlayCount&meta=%s&playCount=0)' % (sysaddon, _sysmeta)))
                        meta.update({'playcount': 1, 'overlay': 7})
                        sysmeta.update({'playcount': 1, 'overlay': 7})
                    else:
                        cm.append((watchedMenu, 'RunPlugin(%s?action=UpdatePlayCount&meta=%s&playCount=1)' % (sysaddon, _sysmeta)))
                        meta.update({'playcount': 0, 'overlay': 6})
                        sysmeta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass
                cm.append(('Einstellungen', 'RunPlugin(%s?action=addonSettings)' % sysaddon))
                item.addContextMenuItems(cm)

                sysmeta = control.quote_plus(json.dumps(sysmeta))
                url = '%s?action=seasons&sysmeta=%s' % (sysaddon, sysmeta)

                if 'plot' in i: plot = i['plot']
                else: plot = ''

                votes = ''
                if 'rating' in i and i['rating'] != '':
                    if 'votes' in i: votes = '(%s)' % str(i['votes']).replace(',', '')
                    plot = '[COLOR blue]Bewertung :  %.1f  %s[/COLOR]%s%s' % (float(i['rating']), votes, "\n\n", plot)
                meta.update({'plot': plot})
                if 'cast' in i and i['cast']:
                    item.setCast(i['cast'])
                    meta.pop('cast', None)  # ersetzt durch item.setCast(i['cast'])
                item.setArt({'poster': poster, 'banner': addonBanner})
                item.setProperty('Fanart_Image', fanart)

                ## supported infolabels: https://codedocs.xyz/AlwinEsch/kodi/group__python__xbmcgui__listitem.html#ga0b71166869bda87ad744942888fb5f14
                # remove unsupported infolabels
                meta.pop('fanart', None)
                meta.pop('poster', None)
                meta.pop('imdb_id', None)
                meta.pop('tvdb_id', None)
                meta.pop('tmdb_id', None)
                meta.pop('number_of_seasons', None)
                meta.pop('originallanguage', None)
                meta.pop('budget', None)
                meta.pop('revenue', None)

                # for test only
                #meta.pop('genre', None)
                #meta.pop('genres', None)

                item.setInfo(type='Video', infoLabels=meta)

                # gefakte Video/Audio Infos
                video_streaminfo = {'codec': 'h264', "width": 1920, "height": 1080}
                item.addStreamInfo('video', video_streaminfo)
                audio_streaminfo = {'codec': 'dts', 'channels': 6, 'language': 'de'}
                item.addStreamInfo('audio', audio_streaminfo)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except Exception as e:
                print(e)
                pass

        # nächste Seite
        try:
            self.next_pages = self.next_pages + 1
            if self.next_pages <= self.total_pages:
                if self.query:
                    url = '%s?action=tvshows&url=&page=%s&query=%s' % (sys.argv[0], self.next_pages, self.query )
                else:
                    url = '%s?action=listings' % sys.argv[0]
                    url += '&media_type=%s' % _params.get('media_type')
                    url += '&next_pages=%s' % self.next_pages
                    url += '&url=%s' % control.quote_plus(_params.get('url'))
                item = control.item(label="Nächste Seite")
                icon = control.addonNext()
                item.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': icon})
                if not addonFanart is None: item.setProperty('Fanart_Image', addonFanart)
                # gesehen/ungesehen im cm und "Keine Informationen verfügbar" ausblenden (abhängig vom Skin)
                item.setInfo('video', {'overlay': 4, 'plot': ' '}) # alt255
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
        except:
            pass

        control.content(syshandle, 'tvshows') # movies tvshows
        control.directory(syshandle, cacheToDisc=False) # False -> wegen Playcount

    def worker(self):
        self.meta = []
        threads = []
        for i in range(0, len(self.list)):
            threads.append(workers.Thread(self.super_meta, i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        self.meta = sorted(self.meta, key=lambda k: k['title'])
        self.list = [i for i in self.meta] # falls noch eine Filterfunktion kommt
        self.list = [i for i in self.list if not i['plot'].strip() == '' and not i['poster'] == control.addonPoster()]  # - Filter


    def super_meta(self, i, id=''):
        try:
            if id == '': id = self.list[i]
            meta = cTMDB().get_meta('tvshow', '', '', id, advanced='true')
            if not 'poster' in meta or meta['poster'] == '':
                if meta['tvdb_id']:
                    poster = art.getTvShows_art(meta['tmdb_id'], meta['tvdb_id'])
                    meta.update({'poster': poster})

            try:
                playcount = playcountDB.getPlaycount('tvshow', 'title', meta['title'], None, None)
                playcount = playcount if playcount else 0
                overlay = 7 if playcount > 0 else 6
                meta.update({'playcount': playcount, 'overlay': overlay})
            except:
                pass
            self.meta.append(meta)
            return meta
        except:
            pass

