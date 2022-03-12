 #! /usr/bin/python

_strings = {}

if __name__ == "__main__":
    import polib
    po = polib.pofile("resources/language/resource.language.en_gb/strings.po")
    try:
        import re, subprocess
        r = subprocess.check_output(["grep", "-hnr", "_([\'\"]", "."])
        strings = re.compile("_\([\"'](.*?)[\"']\)", re.IGNORECASE).findall(r)
        translated = [m.msgid.replace("'", "\\'") for m in po]
        missing = set([s for s in strings if s not in translated])
        if missing:
            ids_range = range(30000, 31000)
            ids_reserved = [int(m.msgctxt[1:]) for m in po]
            ids_available = [x for x in ids_range if x not in ids_reserved]
            print "WARNING: missing translation for '%s'" % missing
            for text in missing:
                id = ids_available.pop(0)
                entry = polib.POEntry(msgid=text, msgstr=u'', msgctxt="#{0}".format(id))
                po.append(entry)
            po.save("resources/language/resource.language.en_gb/strings.po")
    except: pass
    content = []
    with open(__file__, "r") as me:
        content = me.readlines()
        content = content[:content.index("#GENERATED\n")+1]
    with open(__file__, "w") as f:
        f.writelines(content)
        for m in po:
            line = "_strings['{0}'] = {1}\n".format(m.msgid.replace("'", "\\'"), m.msgctxt.replace("#", "").strip())
            f.write(line)
else:
    def get_string(t):
        import xbmc, xbmcaddon
        ADDON = xbmcaddon.Addon()
        ADDON_ID = ADDON.getAddonInfo("id")
        id = _strings.get(t)
        if not id:
            xbmc.log("LANGUAGE: missing translation for '%s'" % t)
            return t
        elif id in range(30000, 31000) and ADDON_ID.startswith("plugin"): return xbmcaddon.Addon().getLocalizedString(id).encode('utf-8')
        elif id in range(31000, 32000) and ADDON_ID.startswith("skin"): return xbmcaddon.Addon().getLocalizedString(id).encode('utf-8')
        elif id in range(32000, 33000) and ADDON_ID.startswith("script"): return xbmcaddon.Addon().getLocalizedString(id).encode('utf-8')
        elif not id in range(30000, 33000): return xbmc.getLocalizedString(id).encode('utf-8')
    #setattr(__builtin__, "_", get_string)

# <!----- Menu Translations ----->
_strings['Movies'] = 30100
_strings['TV Shows'] = 30101
_strings['Trakt Account'] = 30102
_strings['Search ...'] = 30103
_strings['Addon Settings'] = 30104
_strings['Blockbuster (TMDB)'] = 30105
_strings['In theatres (TMDB)'] = 30106
#Todo kasi
_strings['Popular Movies (TMDB)'] = 30107
#_strings['Popular (TMDB)'] = 30107
_strings['Top rated (TMDB)'] = 30108
_strings['Most watched (Trakt)'] = 30109
_strings['Most collected (Trakt)'] = 30110
_strings['Popular (Trakt)'] = 30111
_strings['Trending Movies (Trakt)'] = 30112
_strings['Latest releases (Trakt)'] = 30113
_strings['Top 250 (IMDB)'] = 30114
_strings['Movie Genres'] = 30115
_strings['Currently Airing (TMDB)'] = 30116
_strings['Popular (TMDB)'] = 30117
_strings['Most Watched (Trakt)'] = 30118
_strings['Most Collected (Trakt)'] = 30119
_strings['Most Collected Netflix (Trakt)'] = 30120
_strings['Most Popular (Trakt)'] = 30121
_strings['Trending TV Shows (Trakt)'] = 30122
_strings['TV Shows Genres'] = 30123
_strings['Lists (Movies & TV Shows)'] = 30124
_strings['Collection'] = 30125
_strings['Recommendations'] = 30126
_strings['Watchlist'] = 30127
_strings['My Lists'] = 30128
_strings['Liked Lists'] = 30129
_strings['Next Episodes'] = 30130
_strings['Upcoming Episodes'] = 30131
_strings['Enter search string'] = 30132
_strings['Movies (TMDB) search - '] = 30133
_strings['Movies (Trakt) search - '] = 30134
_strings['TV shows (TVDB) search - '] = 30135
_strings['TV shows (Trakt) search - '] = 30136
_strings['Lists (Trakt) search - '] = 30137
# <!----- lib_movies.py Translation ----->
_strings['Do you want to automatically set the WRP MetaPlayer as a video source for movies?'] = 30138
_strings['WRP-MetaPlayer Movies'] = 30139
# <!----- default.py Translation ----->
_strings['None default Player'] = 30140
_strings['Play with %s'] = 30141
_strings['Cache'] = 30142
_strings['cleared'] = 30143
_strings['Synchronize library'] = 30144
_strings['Updating the library is skipped'] = 30145
_strings['Update library'] = 30146
_strings['Do you want to update the library now?'] = 30147
_strings['Update'] = 30148
_strings['Cancel'] = 30149
_strings['WRP-MetaPlayer Player update'] = 30150
_strings['Done'] = 30151
_strings['Failed'] = 30152
_strings['Total Setup'] = 30153
_strings['started'] = 30154
_strings['completed'] = 30155
_strings['WRP-MetaPlayer Player Setup'] = 30156
_strings['Would you like to set a URL for the player download now?'] = 30157
_strings['Set URL'] = 30158
_strings['WRP-MetaPlayer Sources Setup'] = 30159
# <!----- lib_tvshows.py Translation ----->
_strings['Do you want to automatically set the WRP MetaPlayer as the source for TV shows?'] = 30160
_strings['WRP-MetaPlayer TV Shows'] = 30161
# <!----- nav_movies.py Translation ----->
_strings['Not found'] = 30162
_strings['Movie not found'] = 30163
_strings['No information found for '] = 30164
# <!----- nav_tvshows.py Translation ----->
_strings['TV show not found. No show information found for '] = 30165
_strings['Choose TV Show'] = 30166
_strings['Failed to add'] = 30167
# <!----- play_base.py Translation ----->
_strings['Choose Player'] = 30168
_strings['Error'] = 30169
_strings['Video not found'] = 30170
# <!----- meta_players.py Translation ----->
_strings['Invalid player: Player'] = 30171
# <!----- play_tvshows.py Translation ----->
_strings['Information not found for:'] = 30172
_strings['Episode information not found'] = 30173
# <!----- trakt.py Translation ----->
_strings['Authenticate Trakt'] = 30174
_strings['Do you want to authenticate with Trakt now?'] = 30175
_strings['Please go to  https://trakt.tv/activate  and enter this code: '] = 30176
_strings['WRP-MetaPlayer: Clear Trakt account settings'] = 30177
_strings['Reauthorizing Trakt will be required to access My Trakt.[CR][CR]Are you sure?'] = 30178
# <!----- updater.py Translation ----->
_strings['WRP-MetaPlayer: Update players'] = 30179
_strings['Do you want to remove the existing players first? When removing, the contents of the player folder will be deleted and the new players will be installed.'] = 30180
_strings['[B][COLOR springgreen]Delete[/COLOR][/B]'] = 30181
_strings['[B][COLOR red]Continue[/COLOR][/B]'] = 30182













#GENERATED
