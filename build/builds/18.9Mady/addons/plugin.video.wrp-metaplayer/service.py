# -*- coding: UTF-8 -*-

import os
import xbmc
import xbmcaddon
import xbmcgui
import datetime

from default import update_library
from resources.lib.xswift2 import plugin
from resources.lib.video_player import PLAYER


AddonID = xbmcaddon.Addon().getAddonInfo('id')
AddonName = xbmcaddon.Addon().getAddonInfo('name')
NIGHTLY_VERSION_CONTROL = os.path.join(xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')).decode('utf-8'), "update_sha")

def infoDialog(message, heading=AddonName, icon='', time=5000, sound=False):
    if icon == '': icon = xbmcaddon.Addon().getAddonInfo('icon')
    elif icon == 'INFO': icon = xbmcgui.NOTIFICATION_INFO
    elif icon == 'WARNING': icon = xbmcgui.NOTIFICATION_WARNING
    elif icon == 'ERROR': icon = xbmcgui.NOTIFICATION_ERROR
    xbmcgui.Dialog().notification(heading, message, icon, time, sound=sound)

##ka - remove parent directory (..) in lists
#if not 'false' in xbmc.executeJSONRPC('{"jsonrpc":"2.0", "id":1, "method":"Settings.GetSettingValue", "params":{"setting":"filelists.showparentdiritems"}}'):
#    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"filelists.showparentdiritems","value":false}}')
#    xbmc.executebuiltin("ReloadSkin()")

#if os.path.isfile(NIGHTLY_VERSION_CONTROL)== False or xbmcaddon.Addon().getSetting('DevUpdateAuto') == 'true':
from resources.lib import updateManager
status = updateManager.devAutoUpdates(True)
if status == True: infoDialog("Auto Update abgeschlossen", sound=False, icon='INFO', time=3000)
if status == False: infoDialog("Auto Update mit Fehler beendet", sound=True, icon='ERROR')
if status == None: infoDialog("Keine neuen Updates gefunden", sound=False, icon='INFO', time=3000)

 

def go_idle(duration):
	while not xbmc.Monitor().abortRequested() and duration > 0:
		if PLAYER.isPlayingVideo():
			PLAYER.currentTime = PLAYER.getTime()
		xbmc.sleep(1000)
		duration -= 1

def future(seconds):
	return datetime.datetime.now() + datetime.timedelta(seconds=seconds)

if __name__ == '__main__':
	go_idle(5)
	if plugin.get_setting('total_setup_done', bool) == False:
		xbmc.executebuiltin('RunPlugin(plugin://plugin.video.wrp-metaplayer/setup/total)')
		plugin.set_setting('total_setup_done', 'true')
	next_update = future(0)
	while not xbmc.Monitor().abortRequested():
		if next_update <= future(0):
			next_update = future(8*60*60)
			update_library()
		go_idle(30*60)
        
      