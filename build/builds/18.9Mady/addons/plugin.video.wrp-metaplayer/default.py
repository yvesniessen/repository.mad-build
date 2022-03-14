# -*- coding: utf-8 -*-

#############################
# White Rabbit Productions  #
# WRP-MetaPlayer German MOD #
# Mod created by DWH        #
#############################


import os
import sys
import time
import shutil
import xbmcaddon
import xbmc
import xbmcplugin
from resources.lib import updater
from resources.lib import menu_items
from resources.lib import lib_movies
from resources.lib import lib_tvshows
from resources.lib.xswift2 import plugin
from resources.lib import meta_players
from resources.lib import play_base
from language import get_string as _


addonid = 'plugin.video.wrp-metaplayer'

@plugin.route('/devUpdates()')
def Updates():
    from resources.lib import updateManager
    updateManager.devUpdates()

@plugin.route('/defaultplayer')
def setdefaultplayers():
	media = ['movies', 'tvshows']
	none = {'name': _("None default Player")}
	for i in media:
		play_plugin = meta_players.ADDON_SELECTOR.id
		players = meta_players.get_players(i)
		players = [p for p in players if p.id == play_plugin] or players
		players.append(meta_players.AddonPlayer('', '', none))
		if not players or len(players) == 0:
			xbmc.executebuiltin('Action(Info)')
			play_base.action_cancel()
			return
		index = plugin.select( 'Player  %s'  %i, [player.title for player in players])
		if index >= 0:
			plugin.set_setting(i + 'default', players[index].title)

@plugin.route('/clear_cache')
def clear_cache():
	for filename in os.listdir(plugin.storage_path):
		file_path = os.path.join(plugin.storage_path, filename)
		if os.path.isfile(file_path):
			os.unlink(file_path)
		elif os.path.isdir(file_path):
			shutil.rmtree(file_path)
	plugin.notify( _("Cache"), _("cleared"), plugin.get_addon_icon(), 3000)

@plugin.route('/settings')
def open_settings():
	plugin.open_settings()

@plugin.route('/update_library')
def update_library():
	now = time.time()
	is_syncing = plugin.getProperty('wrpmetaplayer_syncing_library')
	is_updating = plugin.getProperty('wrpmetaplayer_updating_library')
	if is_syncing and now - int(is_syncing) < 120:
		plugin.log.debug('Skipping library sync')
	else:
		if plugin.get_setting('library_sync_collection', bool) == True:
			try:
				plugin.setProperty('wrpmetaplayer_syncing_library', int(now))
				plugin.notify('WRP-MetaPlayer', _("Synchronize library"), plugin.get_addon_icon(), 1000)
				lib_tvshows.sync_trakt_collection()
				lib_movies.sync_trakt_collection()
			finally:
				plugin.clearProperty('wrpmetaplayer_syncing_library')
	if is_updating and now - int(is_updating) < 120:
		plugin.log.debug( _("Updating the library is skipped"))
		return
	else:
		if plugin.get_setting('library_updates', bool) == True:
			try:
				plugin.setProperty('wrpmetaplayer_updating_library', int(now))
				plugin.notify('WRP-MetaPlayer', _("Update library"), plugin.get_addon_icon(), 1000)
				lib_tvshows.update_library()
			finally:
				plugin.clearProperty('wrpmetaplayer_updating_library')

@plugin.route('/update_library_from_settings')
def update_library_from_settings():
	now = time.time()
	if plugin.yesno('WRP-MetaPlayer', _("Do you want to update the library now?"), yeslabel= _("Update") , nolabel= _("Cancel")):
		try:
			plugin.setProperty('wrpmetaplayer_updating_library', int(now))
			plugin.notify('WRP-MetaPlayer', _("Update library"), plugin.get_addon_icon(), 500)
			lib_tvshows.update_library()
		finally:
			plugin.clearProperty('wrpmetaplayer_updating_library')

@plugin.route('/update_players')
@plugin.route('/update_players/<url>', name='players_update_url')
def update_players(url=None):
	url = plugin.get_setting('players_update_url', unicode)
	if updater.update_players(url):
		plugin.notify( _("WRP-MetaPlayer Player update"), _("Done"), plugin.get_addon_icon(), 3000)
	else:
		plugin.notify( _("WRP-MetaPlayer Player update"), _("Failed"), plugin.get_addon_icon(), 3000)

@plugin.route('/setup/total')
def total_setup():
	plugin.notify( _("Total Setup"), _("started"), plugin.get_addon_icon(), 2000)
	if sources_setup() == True:
		pass
	if players_setup() == True:
		pass
	plugin.notify( _("Total Setup"), _("completed"), plugin.get_addon_icon(), 3000)

@plugin.route('/setup/silent')
def silent_setup():
	plugin.setProperty('totalwrpmetaplayer', 'true')
	movielibraryfolder = plugin.get_setting('movies_library_folder', unicode)
	tvlibraryfolder = plugin.get_setting('tv_library_folder', unicode)
	try:
		lib_movies.auto_movie_setup(movielibraryfolder)
		lib_tvshows.auto_tvshows_setup(tvlibraryfolder)
	except:
		pass
	plugin.clearProperty('totalwrpmetaplayer')


@plugin.route('/setup/players')
def players_setup():
	plugin.setProperty('wrpmetaplayer_players_setup', 'true')
	url = plugin.get_setting('players_update_url', unicode)
	if url == '':
		if plugin.yesno( _("WRP-MetaPlayer Player Setup"), _("Would you like to set a URL for the player download now?"), yeslabel= _("Set URL"), nolabel= _("Cancel")):
			plugin.open_settings()
		else:
			plugin.notify( _("WRP-MetaPlayer Player Setup"), _("Failed"), plugin.get_addon_icon(), 3000)
	elif updater.update_players(url):
		plugin.notify( _("WRP-MetaPlayer Player Setup"), _("Done"), plugin.get_addon_icon(), 3000)
	else:
		plugin.notify( _("WRP-MetaPlayer Player Setup"), _("Failed"), plugin.get_addon_icon(), 3000)
	plugin.clearProperty('wrpmetaplayer_players_setup')
	return True

@plugin.route('/setup/sources')
def sources_setup():
	movielibraryfolder = plugin.get_setting('movies_library_folder', unicode)
	tvlibraryfolder = plugin.get_setting('tv_library_folder', unicode)
	try:
		lib_movies.auto_movie_setup(movielibraryfolder)
		lib_tvshows.auto_tvshows_setup(tvlibraryfolder)
		plugin.notify( _("WRP-MetaPlayer Sources Setup"), _("Done"), plugin.get_addon_icon(), 3000)
	except:
		plugin.notify( _("WRP-MetaPlayer Sources Setup"), _("Failed"), plugin.get_addon_icon(), 3000)
	return True

if __name__ == '__main__':
	arg = sys.argv[0]
	handle = int(sys.argv[1])
	if '/movies/' in arg:
		xbmcplugin.setContent(handle, 'movies')
	elif '/tv/' in arg:
		xbmcplugin.setContent(handle, 'tvshows')
	elif '/lists/show' in arg:
		xbmcplugin.setContent(handle, 'videos')
	elif '/tv_episodes_' in arg:
		xbmcplugin.setContent(handle, 'episodes')
	elif '/movies_genres' in arg or '/tv_genres' in arg:
		xbmcplugin.setContent(handle, 'genres')
	else:
		xbmcplugin.setContent(handle, 'addons')
	plugin.run()
